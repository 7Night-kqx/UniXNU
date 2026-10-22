#!/usr/bin/env python3
"""Check that the boot-progress probes accept either form of alignment padding.

patch-xnu-entry-probe.py carves its stage caves, and the panic screen, out of the
gap ld64 leaves after _start in __text. That gap is bytes nothing executes, but
which bytes they are is a toolchain decision:

  * the source kernel this port started from has zero words there, and
  * the prelinked kernel this board builds fills the same gap with arm64 `nop`s.

The patcher used to test "any nonzero byte", which rejected the second kernel with
"Padding at 0x... is not empty" even though the region was pure padding -- the
payload step had already succeeded at every earlier stage by then, so the failure
surfaced only in CI, after the kernel and userdata builds. This holds the check to
the semantics that matter: a word is usable padding when it is either zero or a
nop, and anything else is still refused.

The probe is assembled through scripts/xnu-panic-screen.c, so a real kernel is
needed to exercise the whole patcher; these checks call the module's own predicate
directly, which is the rule the caves are validated against.
"""
import importlib.util
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOP = struct.pack('<I', 0xD503201F)

failures = []


def check(name, condition, detail=''):
    print(f'{"ok  " if condition else "FAIL"} {name}')
    if not condition:
        failures.append(name + (f': {detail}' if detail else ''))


def load_patcher():
    path = ROOT / 'scripts/patch-xnu-entry-probe.py'
    spec = importlib.util.spec_from_file_location('patch_xnu_entry_probe', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    module = load_patcher()
    is_padding = getattr(module, 'is_padding', None)
    check('the patcher defines an is_padding predicate', callable(is_padding),
          'a bare "any(nonzero bytes)" test rejects nop-filled kernels')
    if not callable(is_padding):
        print(f'\n{len(failures)} failed')
        return 1

    check('nop is the expected padding word', getattr(module, 'NOP', None) == NOP,
          repr(getattr(module, 'NOP', None)))

    # Both padding forms, alone and interleaved, are accepted.
    check('zero words are padding', is_padding(b'\0' * 0x60))
    check('nop words are padding', is_padding(NOP * 0x18))
    check('mixed zero and nop words are padding', is_padding(b'\0' * 4 + NOP * 4 + b'\0' * 8))

    # The panic screen is not a multiple of four bytes long, so the check is also
    # asked about a region whose length ends inside a nop. A partial word is padding
    # only when it matches the bytes that word would start with.
    check('a run ending inside a nop is padding', is_padding(NOP * 3 + NOP[:3]))
    check('a run ending inside a zero word is padding', is_padding(b'\0' * 13))

    # Real code is still refused: this is the guard that protects the kernel.
    check('a branch is not padding', not is_padding(struct.pack('<I', 0x14000000) + NOP * 4),
          'a branch in the gap means the cave would overwrite code')
    check('an arbitrary instruction is not padding', not is_padding(NOP + struct.pack('<I', 0xD5181000)),
          'msr SCTLR_EL1 is not padding')
    check('a nonzero ragged tail is not padding', not is_padding(NOP * 2 + b'\x01\x02'))
    check('data is not padding', not is_padding(b'text' * 4))

    # The two call sites must go through the predicate, not repeat the old test.
    source = (ROOT / 'scripts/patch-xnu-entry-probe.py').read_text()
    check('the cave check uses is_padding', 'not is_padding(data[file_offset(va):' in source,
          'the stage caves are still compared against zero bytes')
    check('the panic screen check uses is_padding', 'not is_padding(data[file_offset(load):' in source,
          'the panic screen is still compared against zero bytes')
    check('no raw nonzero-byte padding test remains',
          'any(data[file_offset(' not in source,
          'a padding site still uses any(...) and rejects nop-filled kernels')

    # Homebrew split ld.lld out of llvm, so the patcher must name the right package when a tool is
    # missing instead of raising FileNotFoundError from inside subprocess.
    tool_fn = getattr(module, 'tool', None)
    check('the patcher resolves host tools through one helper', callable(tool_fn),
          'a missing ld.lld surfaces as FileNotFoundError instead of an install hint')
    if callable(tool_fn):
        module.shutil.which = lambda name: None
        module.os.access = lambda *args: False
        for name, package in (('ld.lld', 'lld'), ('llvm-objcopy', 'llvm')):
            try:
                tool_fn(name)
            except SystemExit as error:
                check(f'a missing {name} names its package', package in str(error), str(error))
            else:
                check(f'a missing {name} names its package', False, 'tool() returned a path anyway')
    check('no bare homebrew fallback path remains',
          "shutil.which('clang') or" not in source and "shutil.which('ld.lld') or" not in source,
          'a fallback path string hides which package is missing')

    # The panic screen needs a glyph table. DarwinBoot carries a byte-identical DiagFont.h and is a
    # submodule of this repository, while the Mu-Silicium Font.h is an optional input: the payload
    # step must not require a Mu-Silicium checkout to place the panic screen.
    darwinboot = ROOT / 'drivers/DarwinBoot/DarwinBootPkg/Driver'
    check('DarwinBoot carries the glyph table',
          (darwinboot / 'DiagFont.h').is_file(),
          'DiagFont.h is the font the payload patch falls back to')
    if (darwinboot / 'DiagFont.h').is_file():
        header = (darwinboot / 'DiagFont.h').read_text()
        check('the fallback header defines the glyph font', 'GLYPH_FONT' in header)
        check('the payload patch prefers the in-repo font', "ROOT / 'drivers/DarwinBoot/DarwinBootPkg/Driver'" in source,
              'the patcher still only looks in the optional Mu-Silicium checkout')
        panic_c = (ROOT / 'scripts/xnu-panic-screen.c').read_text()
        check('the panic screen accepts either font header',
              '__has_include("Font.h")' in panic_c and 'include "DiagFont.h"' in panic_c,
              'xnu-panic-screen.c still includes Font.h unconditionally')

    if failures:
        print(f'\n{len(failures)} failed')
        return 1
    print('\nall checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
