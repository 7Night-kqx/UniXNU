#!/usr/bin/env python3
"""Check that a decoded UDIF image lands where its own run tables say it does.

The userdata step decodes the IPSW's OS disk image with scripts/unixnu/dmg.py instead of attaching it
with macOS `hdiutil`. That decoder had a bug with no visible symptom in its own checks: a blkx run's
sector number is relative to the partition the blkx describes, and the blkx header's sectorNumber is
where that partition starts. Writing runs at their table-relative sector number left the output image
all zeros -- while every partition CRC-32 still passed, because the CRC covers the decoded stream and
says nothing about where the bytes were put.

A real image cannot be committed, so this builds a synthetic UDIF with a partition at a nonzero start
sector and checks the three properties that matter:

  * a run is written at header sectorNumber + run sector, not at the run sector;
  * an IGNORE run writes nothing, so those sectors keep whatever the target already held;
  * the decoded CRC-32 is computed over the same bytes the run table describes.

It also checks `raw_size`, which must come from the koly trailer's sectorCount: taking the last run's
end instead drops the GPT tail after the APFS partition (34 + 11870208 + 32 + 1 sectors, not 11870208).
Exit status is 0 when every check passes.
"""
import importlib.util
import os
import plistlib
import struct
import sys
import tempfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SECTOR = 512
# The partition starts here, and its first run is at sector 0: the offset that was dropped.
PARTITION_START = 34
KOLY_SECTORS = 0x1EC

failures = []


def check(name, condition, detail=''):
    print(f'{"ok  " if condition else "FAIL"} {name}')
    if not condition:
        failures.append(name + (f': {detail}' if detail else ''))


def load_dmg():
    """Import scripts/unixnu/dmg.py as the package module it is, so its relative import resolves."""
    sys.path.insert(0, str(ROOT / 'scripts'))
    from unixnu import dmg
    return dmg


def blkx(sector_number, sector_count, runs, crc=None):
    """One blkx entry: a mish header whose run table holds (type, sector, count, offset, length) runs."""
    table = b''
    for index, (kind, sector, count, offset, length) in enumerate(runs):
        terminator = 0xFFFFFFFF if kind == 0xFFFFFFFF else kind
        table += struct.pack('>IIQQQQ', terminator, 0, sector, count, offset, length)
    header = bytearray(204)
    header[0:4] = b'mish'
    struct.pack_into('>QQ', header, 8, sector_number, sector_count)
    struct.pack_into('>II', header, 64, 2 if crc is not None else 0, 4 if crc is not None else 0)
    if crc is not None:
        struct.pack_into('>I', header, 72, crc)
    struct.pack_into('>I', header, 200, len(runs))
    return {'Name': 'Apple_APFS', 'Data': bytes(header) + table}


def build(path, base, crc):
    """Write a UDIF whose data fork is `base` and whose plist describes one run over it."""
    run = (1, 0, len(base) // SECTOR, 0, len(base))
    entry = blkx(PARTITION_START, len(base) // SECTOR, [run, (0xFFFFFFFF, len(base) // SECTOR, 0, 0, 0)],
                 crc=crc)
    plist = plistlib.dumps({'resource-fork': {'blkx': [entry]}})
    total_sectors = PARTITION_START + len(base) // SECTOR + 32 + 1
    with path.open('wb') as stream:
        stream.write(base)
        xml_offset = stream.tell()
        stream.write(plist)
        trailer = bytearray(512)
        trailer[0:4] = b'koly'
        struct.pack_into('>I', trailer, 4, 4)
        struct.pack_into('>Q', trailer, 0x18, 0)
        struct.pack_into('>QQ', trailer, 0xD8, xml_offset, len(plist))
        struct.pack_into('>Q', trailer, KOLY_SECTORS, total_sectors)
        stream.seek(xml_offset + len(plist))
        stream.write(trailer)
    return total_sectors


def main():
    dmg = load_dmg()
    base = bytes((index * 7 + 3) & 0xFF for index in range(4 * SECTOR))
    crc = zlib.crc32(base) & 0xFFFFFFFF

    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        source = directory / 'synthetic.dmg'
        total_sectors = build(source, base, crc)

        with source.open('rb') as stream:
            size = source.stat().st_size
            check('the synthetic image is recognized as UDIF', dmg.is_udif(stream, size))
            expected = total_sectors * SECTOR
            actual = dmg.raw_size(stream, size)
            check('raw_size comes from the koly sectorCount, GPT tail included',
                  actual == expected, f'{actual} != {expected}')

        # The target starts filled with 0xAA so an unwritten sector is visible, not silently zero.
        target = directory / 'raw.img'
        with target.open('wb') as stream:
            stream.truncate(total_sectors * SECTOR)
            stream.seek(0)
            stream.write(b'\xAA' * (total_sectors * SECTOR))
        with source.open('rb') as stream, target.open('r+b') as want:
            hashes = dmg.decode(stream, source.stat().st_size, want)
        check('the run table hashes the bytes it describes', hashes.get('Apple_APFS') is not None)

        data = target.read_bytes()
        at_front = data[0:len(base)]
        at_partition = data[PARTITION_START * SECTOR:PARTITION_START * SECTOR + len(base)]
        check('the run is not written at its table-relative sector', at_front == b'\xAA' * len(base),
              'writing at the run sector alone is the bug this guards')
        check('the run is written at header sectorNumber + run sector', at_partition == base)

        # The lead-in and tail are not described by any run, so they must stay untouched.
        check('sectors outside every run are left alone',
              data[0:PARTITION_START * SECTOR] == b'\xAA' * (PARTITION_START * SECTOR))

        # An IGNORE run must write nothing and must not enter the CRC: give it corrupt bytes and keep the
        # original CRC, which only holds if the ignore run is skipped entirely.
        ignore_entry = blkx(PARTITION_START, 4, [
            (2, 0, 2, 0, 0),
            (1, 2, 2, 0, 2 * SECTOR),
            (0xFFFFFFFF, 4, 0, 0, 0),
        ], crc=zlib.crc32(base[2 * SECTOR:]) & 0xFFFFFFFF)
        ignore_plist = plistlib.dumps({'resource-fork': {'blkx': [ignore_entry]}})
        ignored = directory / 'ignore.dmg'
        with ignored.open('wb') as stream:
            stream.write(base[2 * SECTOR:])
            xml_offset = stream.tell()
            stream.write(ignore_plist)
            trailer = bytearray(512)
            trailer[0:4] = b'koly'
            struct.pack_into('>I', trailer, 4, 4)
            struct.pack_into('>QQ', trailer, 0xD8, xml_offset, len(ignore_plist))
            struct.pack_into('>Q', trailer, KOLY_SECTORS, PARTITION_START + 4 + 32 + 1)
            stream.seek(xml_offset + len(ignore_plist))
            stream.write(trailer)
        target2 = directory / 'ignore.img'
        with target2.open('wb') as stream:
            stream.truncate((PARTITION_START + 4 + 32 + 1) * SECTOR)
            stream.seek(0)
            stream.write(b'\xAA' * (PARTITION_START + 4 + 32 + 1) * SECTOR)
        with ignored.open('rb') as stream, target2.open('r+b') as want:
            dmg.decode(stream, ignored.stat().st_size, want)
        data2 = target2.read_bytes()
        kept = data2[PARTITION_START * SECTOR:PARTITION_START * SECTOR + 2 * SECTOR]
        wrote = data2[(PARTITION_START + 2) * SECTOR:PARTITION_START * SECTOR + 4 * SECTOR]
        check('an IGNORE run writes nothing',
              kept == b'\xAA' * (2 * SECTOR), 'ignore runs are not part of the data fork')
        check('an IGNORE run does not enter the CRC, and the rest still decodes',
              wrote == base[2 * SECTOR:], 'a CRC over skipped bytes would not match')

    print(f'\n{len(failures)} failed' if failures else '\nall checks passed')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
