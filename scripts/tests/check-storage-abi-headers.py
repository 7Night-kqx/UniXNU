#!/usr/bin/env python3
"""Exercise the IOStorageFamily header staging the storage transports compile against.

The storage transports include <IOKit/storage/IOBlockStorageDevice.h>, which is not part of the xnu tree: the
classes live in Apple's separate IOStorageFamily project. scripts/storage_abi_headers.py stages those public
headers into build/storage-abi/include, and scripts/unixnu/kernel.py stages them before the archive builders
of a board that selects a transport.

A build that fetched IOStorageFamily but never produced that directory fails only in the archive step, after
the bootstrap pass, with a bare "file not found" from a compile record. These checks run first: they stage the
headers against a fixture source, and they hold the wiring between feeds.toml, the fetch list, the kernel
driver and the audit script to one pinned revision.
"""
import ast
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / 'scripts/storage_abi_headers.py'
sys.path.insert(0, str(ROOT / 'scripts'))
from storage_abi_headers import PINNED_REVISION, stage

failures = []


def check(name, condition, detail=''):
    print(f'{"ok  " if condition else "FAIL"} {name}')
    if not condition:
        failures.append(name + (f': {detail}' if detail else ''))


def fixture(tmp, headers=('IOBlockStorageDevice.h', 'IOStorage.h'), git=True):
    """A stand-in IOStorageFamily source and macOS SDK, so the staging runs without the network."""
    root = Path(tmp) / 'root'
    source = root / 'refer/IOStorageFamily'
    source.mkdir(parents=True)
    for name in headers:
        (source / name).write_text(f'// {name}\n')
    (source / 'IOBlockStorageDevice.cpp').write_text('// not a header\n')
    sdk = Path(tmp) / 'MacOSX.sdk'
    (sdk / 'usr/include').mkdir(parents=True)
    (sdk / 'usr/include/TargetConditionals.h').write_text('// platform selection\n')
    if git:
        subprocess.run(['git', 'init', '-q', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'add', '-A'], check=True)
        subprocess.run(['git', '-C', str(source), '-c', 'user.name=t', '-c', 'user.email=t@t',
                        'commit', '-qm', 'fixture'], check=True)
    return root, source, sdk


def head(source):
    return subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()


def main():
    # 1. Staging copies the family headers where the builders look, plus the platform-selection header.
    with tempfile.TemporaryDirectory() as tmp:
        root, source, sdk = fixture(tmp)
        headers = stage(root, source, expected=head(source), sdk=sdk)
        check('stage: returns the include directory the builders add',
              headers == root / 'build/storage-abi/include/IOKit/storage', str(headers))
        check('stage: copies every family header',
              (headers / 'IOBlockStorageDevice.h').read_text() == '// IOBlockStorageDevice.h\n'
              and (headers / 'IOStorage.h').is_file())
        check('stage: leaves the implementation file out', not (headers / 'IOBlockStorageDevice.cpp').exists())
        check('stage: copies TargetConditionals.h next to IOKit',
              (root / 'build/storage-abi/include/TargetConditionals.h').read_text() == '// platform selection\n')

    # 2. A second staging of an unchanged source rewrites nothing, so the archive step stays incremental.
    with tempfile.TemporaryDirectory() as tmp:
        root, source, sdk = fixture(tmp)
        headers = stage(root, source, expected=head(source), sdk=sdk)
        before = (headers / 'IOBlockStorageDevice.h').stat().st_mtime_ns
        time.sleep(0.01)
        stage(root, source, expected=head(source), sdk=sdk)
        check('stage: keeps an unchanged header untouched',
              (headers / 'IOBlockStorageDevice.h').stat().st_mtime_ns == before)
        (source / 'IOStorage.h').write_text('// changed\n')
        stage(root, source, expected=head(source), sdk=sdk)
        check('stage: rewrites a changed header', (headers / 'IOStorage.h').read_text() == '// changed\n')

    # 3. The qualified revision is enforced.
    with tempfile.TemporaryDirectory() as tmp:
        root, source, sdk = fixture(tmp)
        mismatch = 'not-a-pinned-revision'
        try:
            stage(root, source, expected='0' * 40, sdk=sdk)
            check('stage: rejects a source at another revision', False)
        except SystemExit as error:
            check('stage: rejects a source at another revision', 'qualified IOStorageFamily' in str(error), str(error))
        try:
            stage(root, source, expected=mismatch, sdk=sdk)
            check('stage: names the expected revision', False)
        except SystemExit as error:
            check('stage: names the expected revision', mismatch[:12] in str(error), str(error))

    # 4. A missing source or SDK is reported, not traced back to a compiler.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / 'root'
        try:
            stage(root, expected=None)
            check('stage: reports a missing IOStorageFamily source', False)
        except SystemExit as error:
            check('stage: reports a missing IOStorageFamily source',
                  'refer/IOStorageFamily missing' in str(error) and 'unixnu fetch' in str(error), str(error))

    with tempfile.TemporaryDirectory() as tmp:
        root, source, sdk = fixture(tmp, headers=())
        try:
            stage(root, source, expected=None, sdk=sdk)
            check('stage: reports a source without headers', False)
        except SystemExit as error:
            check('stage: reports a source without headers', 'no IOStorageFamily header' in str(error), str(error))

    with tempfile.TemporaryDirectory() as tmp:
        root, source, sdk = fixture(tmp)
        try:
            stage(root, source, expected=None, sdk=Path(tmp) / 'missing-sdk')
            check('stage: reports a missing TargetConditionals.h', False)
        except SystemExit as error:
            check('stage: reports a missing TargetConditionals.h',
                  'TargetConditionals.h missing' in str(error), str(error))

    # 5. One pinned revision, one producer, and a fetch that brings the source in.
    sources = tomllib.loads((ROOT / 'feeds.toml').read_text()).get('source', [])
    family = [entry for entry in sources if entry.get('name') == 'IOStorageFamily']
    check('feeds: declares IOStorageFamily once', len(family) == 1, str(len(family)))
    if family:
        check('feeds: pins the revision the staging is qualified against',
              family[0].get('commit') == PINNED_REVISION and family[0].get('kind') == 'refer',
              f'{family[0].get("kind")} {family[0].get("commit")}')
        check('feeds: points at the public source',
              family[0].get('git', '').endswith('IOStorageFamily.git'), family[0].get('git', ''))

    cli = ast.parse((ROOT / 'scripts/unixnu/cli.py').read_text())
    references = next(ast.literal_eval(node.value) for node in ast.walk(cli)
                      if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', None) == 'REFERENCES')
    check('cli: the kernel step fetches IOStorageFamily',
          'IOStorageFamily' in references.get('kernel', ()), str(references.get('kernel')))

    kernel = (ROOT / 'scripts/unixnu/kernel.py').read_text()
    check('kernel: stages the headers before the archive builders',
          'scripts/storage_abi_headers.py' in kernel
          and kernel.index('scripts/storage_abi_headers.py') < kernel.index("for index, entry in enumerate(entries, 1)"))
    check('kernel: stages them only for the transports that include them',
          all(name in kernel for name in ('NativeUfs', 'NativeVirtioBlock', 'NativeRamBlock')))

    audit = (ROOT / 'scripts/audit-storage-interface.py').read_text()
    check('audit: stages through the same producer', 'from storage_abi_headers import' in audit)
    check('audit: does not pin a second copy of the revision', PINNED_REVISION not in audit)

    print(f'\n{len(failures)} failure(s)')
    for name in failures:
        print(f'  {name}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
