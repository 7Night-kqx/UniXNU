#!/usr/bin/env python3
"""Exercise the bootstrap path of build-xnu-4k-baseline.sh without XNU or Xcode.

The first build of a board from scratch cannot compile the archive builders before make has walked the
tree, and make cannot link before the archives exist. The script therefore has a bootstrap mode: the
archive section is skipped and make is allowed to fail, and only the compile records are required of it.
That contract is what this checks.

The real script is run in a sandbox with the host tools stubbed. Every archive-producing section of the
real script is reached, so a regression in the guards or in the record check fails here instead of after a
twenty-minute CI build.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/build-xnu-4k-baseline.sh'
failures = []


def check(name, condition, detail=''):
    print(f'{"ok  " if condition else "FAIL"} {name}')
    if not condition:
        failures.append(name + (f': {detail}' if detail else ''))


def sandbox(tmp, make_body, records=True):
    """A tree shaped like the build tree, with the tools the script calls replaced by stubs."""
    tree = Path(tmp) / 'tree'
    (tree / 'scripts').mkdir(parents=True)
    shutil.copyfile(SCRIPT, tree / 'scripts/build-xnu-4k-baseline.sh')
    shutil.copymode(SCRIPT, tree / 'scripts/build-xnu-4k-baseline.sh')
    (tree / 'scripts/prepare-xnu-source.py').write_text('pass\n')
    (tree / 'scripts/build-firehose.sh').write_text('exit 0\n')
    (tree / 'scripts/build-boot-progress.py').write_text('pass\n')
    # The script clones from the network and builds Apple sources first; those steps are not what this
    # checks, so they are stubbed to look already done.
    for relative in ('refer/xnu/.git', '.cache/xnu-work/.git', 'refer/libplatform/.git',
                     'refer/libdispatch/.git', '.cache/fakeroot/usr/local/libexec'):
        (tree / relative).mkdir(parents=True)
    (tree / '.cache/fakeroot/usr/local/libexec/availability.pl').write_text('#!/bin/sh\n')
    (tree / '.cache/fakeroot/usr/local/libexec/availability.pl').chmod(0o755)
    (tree / '.cache/fakeroot/.xnu-10063.141.1-headers').write_text('')
    (tree / '.cache/fakeroot/usr/local/lib/kernel').mkdir(parents=True)
    (tree / '.cache/fakeroot/usr/local/lib/kernel/libfirehose_kernel.a').write_text('')
    (tree / 'refer/libdispatch/os').mkdir(parents=True)
    (tree / 'refer/libplatform/include').mkdir(parents=True)
    (tree / 'refer/libplatform/private/platform').mkdir(parents=True)
    object_dir = tree / 'build/xnu/ios-obj/DEVELOPMENT_ARM64_BCM2837'
    (object_dir / 'osfmk/DEVELOPMENT').mkdir(parents=True)
    (object_dir / 'iokit/DEVELOPMENT').mkdir(parents=True)
    if records:
        for relative in ('osfmk/DEVELOPMENT/prng_random.o.json', 'iokit/DEVELOPMENT/IOPlatformExpert.cpo.json'):
            (object_dir / relative).write_text('{}\n')
    # `make` is a stub: it records that it ran and returns the exit code the scenario asks for.
    bindir = Path(tmp) / 'bin'
    bindir.mkdir()
    make = bindir / 'make'
    make.write_text('#!/bin/sh\n' + make_body)
    make.chmod(0o755)
    for name in ('ditto', 'unifdef', 'xcrun', 'clang'):
        stub = bindir / name
        stub.write_text('#!/bin/sh\nexit 0\n')
        stub.chmod(0o755)
    # git answers the one query the script makes before it starts: the pinned XNU revision.
    git = bindir / 'git'
    git.write_text('#!/bin/sh\n'
                   'case "$*" in\n'
                   '  *"rev-parse HEAD"*) echo d8b80295118ef25ac3a784134bcf95cd8e88109f ;;\n'
                   'esac\nexit 0\n')
    git.chmod(0o755)
    env = dict(os.environ, PATH=f'{bindir}:{os.environ["PATH"]}', JOBS='2')
    env.pop('XNU_BOOTSTRAP', None)
    return tree, env, object_dir


def run_script(tree, env, extra_env):
    result = subprocess.run(['bash', str(tree / 'scripts/build-xnu-4k-baseline.sh')],
                            cwd=tree, env={**env, **extra_env}, capture_output=True, text=True)
    return result


def main():
    print(f'sandbox source: {SCRIPT}')

    # 1. Bootstrap with make failing at the link and the records in place: succeeds, says why.
    with tempfile.TemporaryDirectory() as tmp:
        tree, env, _ = sandbox(tmp, 'echo BOOTSTRAP_MAKE_RAN\nexit 2\n')
        result = run_script(tree, env, {'XNU_BOOTSTRAP': '1', 'XNU_BOOT_PROGRESS': '0'})
        check('bootstrap: make was reached at all', 'BOOTSTRAP_MAKE_RAN' in result.stdout, result.stdout[-400:])
        check('bootstrap: a failed link is accepted', result.returncode == 0, result.stderr[-600:])
        check('bootstrap: the expected failure is explained',
              'make exited 2 as expected' in result.stdout, result.stdout[-400:])
        check('bootstrap: no archive is demanded',
              'error: missing archive' not in result.stderr, result.stderr[-400:])

    # 2. Bootstrap with no compile records: fails and names the record, not a bare exit.
    with tempfile.TemporaryDirectory() as tmp:
        tree, env, _ = sandbox(tmp, 'exit 2\n', records=False)
        result = run_script(tree, env, {'XNU_BOOTSTRAP': '1', 'XNU_BOOT_PROGRESS': '0'})
        check('bootstrap without records: fails', result.returncode != 0)
        check('bootstrap without records: names the missing record',
              'left no osfmk/DEVELOPMENT/prng_random.o.json' in result.stderr, result.stderr[-400:])

    # 3. A real build whose archive is missing: the message names the file and how to build it.
    with tempfile.TemporaryDirectory() as tmp:
        tree, env, _ = sandbox(tmp, 'echo REAL_MAKE_RAN\nexit 0\n')
        result = run_script(tree, env, {'XNU_BOOT_PROGRESS': '0', 'XNU_SOURCE_CORECRYPTO14': '1',
                                        'XNU_CRYPTO_BOOTSTRAP': 'prelinked'})
        check('real build: fails on the missing corecrypto archive', result.returncode != 0,
              result.stdout[-400:])
        check('real build: names the archive',
              'missing archive' in result.stderr and 'corecrypto' in result.stderr, result.stderr[-400:])
        check('real build: never reached make', 'REAL_MAKE_RAN' not in result.stdout, result.stdout[-400:])

    # 4. Bootstrap is strict about its own value.
    with tempfile.TemporaryDirectory() as tmp:
        tree, env, _ = sandbox(tmp, 'exit 0\n')
        result = run_script(tree, env, {'XNU_BOOTSTRAP': 'yes'})
        check('bootstrap: rejects a value that is not 0 or 1',
              result.returncode != 0 and 'XNU_BOOTSTRAP must be 0 or 1' in result.stderr,
              result.stderr[-300:])

    print(f'\n{len(failures)} failure(s)')
    for name in failures:
        print(f'  {name}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
