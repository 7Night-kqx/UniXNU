"""Userdata payload: the raw image for the device's root partition.

It holds the unchanged OS and SystemOS disk images of the IPSW, byte for byte, behind a small manifest
(the SHNGROOT layout the native UFS root driver reads):

    0x000000  manifest block (4096 bytes), zero padding to 1 MiB
    0x100000  window "OS"        the whole OS disk image, 1 MiB aligned
    ....      window "SystemOS"  the whole SystemOS disk image, 1 MiB aligned

Manifest (little endian): "SHNGROOT", u32 version=1, u32 count, u64 image_bytes, then `count` 128-byte entries
{char name[32], u64 offset, u64 size, u32 block_size=512, u32 flags(1=read-only), u8 sha256[32], 40 reserved},
and at byte 4064 the SHA-256 of bytes 0..4063.

The images come from the IPSW (a local file or a remote URL, see ipsw.py) and are checked against the pins of
board.toml. They are decoded from UDIF by dmg.py, not by attaching them with macOS `hdiutil`, so the step runs
on any host that has the `lzfse` module: the OS image of this IPSW is LZFSE throughout, and hdiutil is a macOS
tool. Every partition's CRC-32 is verified, so a decode that is wrong fails here instead of on the phone.
Nothing is flashed: the report prints the command, to be run by the user.
"""
import hashlib
import json
import struct

from . import dmg
from .ipsw import Ipsw
from .util import Error, log, sha256_file

MIB = 1 << 20
CHUNK = 8 * MIB


def paths(ctx):
    out = ctx.work / 'userdata'
    return out, out / 'userdata-root.img', out / 'userdata-root.json'


def partition(spec):
    """The GPT partition the root image is flashed to; sheng uses "userdata" and this is its default."""
    return spec.get('partition', 'userdata')


def member(source, component):
    """(name, path) for an IPSW component, extracted once into the cache and checked against its pin."""
    name = source.member(component)
    return name, source.extract(component)


def window_size(path):
    """The size of the disk content a window contributes.

    A UDIF image holds a disk image that has to be decoded; a raw APFS container (which is what the
    Cryptex1,SystemOS component is in this IPSW) is already that image. Both are copied whole, so the
    caller never has to know which it got.
    """
    with path.open('rb') as stream:
        return dmg.raw_size(stream, path.stat().st_size) if dmg.is_udif(stream, path.stat().st_size) \
            else path.stat().st_size


def build(ctx, dry_run=False):
    log('userdata payload')
    spec = ctx.board.get('userdata')
    if not spec:
        raise Error('board.toml has no [userdata]')
    source = Ipsw(ctx)
    capacity = (spec['last_lba'] - spec['first_lba'] + 1) * spec.get('lba_bytes', 4096)
    handles = [(window['name'], *member(source, window['component'])) for window in spec['windows']]
    sizes = {}
    for label, name, path in handles:
        sizes[label] = window_size(path)
        log(f'userdata: {label} from {name} ({sizes[label] >> 20} MiB raw)')
    if dry_run:
        total = MIB + sum((sizes[label] + MIB - 1) // MIB * MIB for label, _, _ in handles)
        log(f'userdata: dry run, {total} bytes ({total / 2**30:.2f} GiB) in {partition(spec)}, nothing written')
        return None
    layout, cursor = [], MIB
    for label, _, _ in handles:
        layout.append((label, cursor, sizes[label]))
        cursor += (sizes[label] + MIB - 1) // MIB * MIB
    total = cursor
    log(f'userdata: image {total} bytes ({total / 2**30:.2f} GiB) in {partition(spec)} of {capacity} bytes')
    if total > capacity:
        raise Error('the image is larger than the root partition')
    out, image, report = paths(ctx)
    out.mkdir(parents=True, exist_ok=True)
    entries = []
    # "w+b": the window hashes are read back out of the image, so it has to be open for reading too.
    with image.open('w+b') as target:
        target.truncate(total)
        for (label, offset, size), (_, name, path) in zip(layout, handles):
            length = path.stat().st_size
            with path.open('rb') as stream:
                if dmg.is_udif(stream, length):
                    dmg.decode(stream, length, target, base=offset)
                else:
                    # A raw container: copy it whole, which is what hdiutil's raw disk would have been.
                    stream.seek(0)
                    target.seek(offset)
                    copied = 0
                    while copied < length:
                        block = stream.read(min(CHUNK, length - copied))
                        if not block:
                            raise Error(f'{name}: ended at {copied} of {length} bytes')
                        target.write(block)
                        copied += len(block)
            target.flush()
            # Hash exactly the window bytes that landed in the image; that is what the driver hands the
            # kernel, and what the manifest promises.
            digest = hashlib.sha256()
            target.seek(offset)
            done = 0
            while done < size:
                block = target.read(min(CHUNK, size - done))
                if not block:
                    raise Error(f'{image}: window {label} ended early at {done}')
                digest.update(block)
                done += len(block)
            entries.append((label, offset, size, digest.digest()))
            log(f'userdata: {label} {size} bytes at {offset:#x} sha256 {digest.hexdigest()}')
        header = bytearray(4096)
        header[0:8] = b'SHNGROOT'
        struct.pack_into('<IIQ', header, 8, 1, len(entries), total)
        for index, (label, offset, size, digest) in enumerate(entries):
            struct.pack_into('<32sQQII32s40s', header, 24 + 128 * index, label.encode(), offset, size,
                             512, 1, digest, bytes(40))
        header[4064:4096] = hashlib.sha256(bytes(header[:4064])).digest()
        target.seek(0)
        target.write(header)
    data = {'image_bytes': total, 'image_sha256': sha256_file(image),
            'manifest_sha256': hashlib.sha256(bytes(header)).hexdigest(),
            'windows': [{'name': n, 'offset': o, 'size': s, 'sha256': d.hex()} for n, o, s, d in entries],
            'partition': partition(spec), 'userdata_bytes': capacity,
            'flash_command': f'fastboot flash {partition(spec)} {image}',
            'source': 'remote' if source.remote else 'local', 'hardware_tested': False}
    report.write_text(json.dumps(data, indent=2) + '\n')
    log(f'userdata: {image}')
    log(f'flash it yourself with: {data["flash_command"]}')
    return image
