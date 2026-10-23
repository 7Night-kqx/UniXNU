"""Read a UDIF disk image (`.dmg`) as its raw disk, without hdiutil.

The IPSW carries the OS and SystemOS disk images as UDIF containers: a `koly` trailer pointing at a
plist whose `blkx` entries describe, per partition, a run table of chunks. Each chunk is stored either
raw (0x00000001) or compressed; the images this port restores are LZFSE (0x80000007). macOS reads them
with `hdiutil attach`, which is a tool a Linux build host does not have, so the same bytes are decoded
here instead.

Two properties make the result trustworthy without a macOS reference to compare against:

  - every blkx run table carries a CRC-32 of the raw bytes it describes (`blkx' header, offset 72 for
    the 40-byte run entries these images use). Decoding a partition and failing that checksum means the
    decoder is wrong, not that the image is unusual;
  - the decoded image is a GPT disk, so its own header and entry-array CRCs must also hold.

Nothing here writes to the source. See `userdata.py` for what is built from the decoded images.
"""
import hashlib
import plistlib
import struct
import zlib

from .util import Error

# The UDIF resource-fork checksum types, per Apple's `checksumType` field.
CHECKSUM_CRC32 = 2
# blkx chunk types.
ZERO = 0x00000000
RAW = 0x00000001
IGNORE = 0x00000002
ADC = 0x80000004
ZLIB = 0x80000005
BZIP2 = 0x80000006
LZFSE = 0x80000007
LZMA = 0x80000008

SECTOR = 512
# The trailer is the last 512 bytes of the image and starts with this magic.
KOLY = b'koly'
# Offset of the run table inside a blkx entry, and the size of one run for these images. The older
# 32-byte layout has no `comment` field; this one does, which is why the size is checked, not assumed.
RUNS_AT = 204
RUN = 40
def koly_trailer(stream, size, plist=True):
    """Read and parse the 512-byte koly trailer at the end of a UDIF image.

    Returns the trailer bytes, or (dataForkOffset, parsed plist) when `plist` is set.
    """
    stream.seek(size - 512)
    trailer = stream.read(512)
    if len(trailer) != 512 or trailer[:4] != KOLY:
        raise Error('not a UDIF image: the last 512 bytes do not start with "koly"')
    version = struct.unpack_from('>I', trailer, 4)[0]
    if version != 4:
        raise Error(f'unsupported UDIF version {version}')
    if not plist:
        return trailer
    # dataForkOffset is 0 for these single-fork images; xmlOffset/xmlLength point at the plist.
    data_offset = struct.unpack_from('>Q', trailer, 0x18)[0]
    xml_offset, xml_length = struct.unpack_from('>QQ', trailer, 0xD8)
    if xml_length == 0 or xml_length > 16 << 20:
        raise Error('UDIF plist length out of range')
    stream.seek(data_offset + xml_offset)
    body = stream.read(xml_length)
    if len(body) != xml_length:
        raise Error('short read of the UDIF plist')
    return data_offset, plistlib.loads(body)


def chunks(blkx):
    """The (type, sector, sector_count, compressed_offset, compressed_length) runs of one blkx entry."""
    entry = blkx['Data']
    if len(entry) < RUNS_AT or entry[:4] != b'mish':
        raise Error('not a blkx entry')
    count = struct.unpack_from('>I', entry, 200)[0]
    if count == 0:
        return []
    if RUNS_AT + count * RUN != len(entry):
        raise Error(f'blkx run table is {len(entry) - RUNS_AT} bytes for {count} runs, '
                    f'not {count * RUN}')
    runs = []
    for index in range(count):
        at = RUNS_AT + index * RUN
        kind, _comment = struct.unpack_from('>II', entry, at)
        first, sectors, offset, length = struct.unpack_from('>QQQQ', entry, at + 8)
        if kind == 0xFFFFFFFF:
            break
        runs.append((kind, first, sectors, offset, length))
    return runs


def decompress(kind, payload, sectors):
    """The raw bytes of one chunk. Raises when the format needs a decoder this build does not have."""
    if kind == ZERO:
        # A zero run stores no bytes at all; its length is implied by the sector count.
        return bytes(sectors * SECTOR)
    if kind == RAW:
        return payload
    if kind == IGNORE:
        # An "ignore" run is not part of the data fork at all: the reader must leave those sectors
        # untouched, not write zeros. On a fresh image they stay zero; promising bytes here would
        # corrupt a partition whose checksum covers them.
        return None
    if kind == LZFSE:
        import lzfse
        return lzfse.decompress(payload)
    if kind == ZLIB:
        return zlib.decompress(payload)
    if kind == ADC:
        raise Error('ADC-compressed UDIF chunks are not supported')
    if kind == BZIP2:
        import bz2
        return bz2.decompress(payload)
    if kind == LZMA:
        import lzma
        return lzma.decompress(payload)
    raise Error(f'unknown UDIF chunk type {kind:#010x}')


def checksum(blkx):
    """(type, bytes) of the checksum stored in a blkx header, or (None, b'') when absent."""
    kind, size = struct.unpack_from('>II', blkx['Data'], 64)
    return kind, blkx['Data'][72:72 + size]


def blkx_entries(plist):
    """The named partition entries of the resource fork, in image order."""
    fork = plist.get('resource-fork')
    if not fork or 'blkx' not in fork:
        raise Error('the UDIF plist has no resource-fork blkx table')
    return [entry for entry in fork['blkx'] if chunks(entry)]


def is_udif(stream, size):
    """True when the file is a UDIF container, recognized by the koly trailer at its end."""
    if size < 512:
        return False
    stream.seek(size - 512)
    return stream.read(4) == KOLY


def raw_size(stream, size):
    """The size of the raw disk the image describes, from the koly trailer."""
    trailer = koly_trailer(stream, size, plist=False)
    sectors = struct.unpack_from('>Q', trailer, 0x1EC)[0]
    if not sectors:
        raise Error('the UDIF trailer records no sectors')
    return sectors * SECTOR


def decode(stream, size, want=None, base=0, progress=None):
    """Write the raw disk of a UDIF image to a seekable binary `want`, checking every blkx checksum.

    `want` must already be truncated to `base + raw_size`. Each partition is written at `base` plus its
    place in the disk. Returns {partition name: sha256 of its stored bytes}, in table order.

    A run's sector number is relative to its own blkx partition, and the blkx header's sectorNumber says
    where that partition starts: a run at sector 0 of Apple_APFS is disk sector 34, not sector 0. Writing
    runs at their table-relative sector number would leave the whole image zero while every checksum
    still passed, because the checksum covers the decoded stream and says nothing about placement.
    """
    data_offset, plist = koly_trailer(stream, size)
    result = {}
    for entry in blkx_entries(plist):
        name = entry.get('Name', '')
        start = struct.unpack_from('>Q', entry['Data'], 8)[0]
        digest = hashlib.sha256()
        crc = 0
        for kind, sector, sectors, offset, length in chunks(entry):
            if kind == IGNORE:
                # Not stored and not checksummed: the run table simply skips these sectors.
                continue
            stream.seek(data_offset + offset)
            payload = stream.read(length)
            if len(payload) != length:
                raise Error(f'short read of {name} at {offset}')
            raw = decompress(kind, payload, sectors)
            expected = sectors * SECTOR
            if len(raw) != expected:
                raise Error(f'{name}: chunk at sector {sector} decoded to {len(raw)} bytes, '
                            f'not {expected}')
            if want is not None and sectors:
                want.seek(base + (start + sector) * SECTOR)
                want.write(raw)
            crc = zlib.crc32(raw, crc)
            digest.update(raw)
        kind, stored = checksum(entry)
        if kind == CHECKSUM_CRC32 and stored:
            if struct.unpack('>I', stored[:4])[0] != crc & 0xFFFFFFFF:
                raise Error(f'{name}: CRC-32 {crc & 0xFFFFFFFF:08x} does not match the image\'s '
                            f'{struct.unpack(">I", stored[:4])[0]:08x}; the decode is wrong')
        result[name] = digest.hexdigest()
        if progress:
            progress(name, start, digest.hexdigest())
    return result
