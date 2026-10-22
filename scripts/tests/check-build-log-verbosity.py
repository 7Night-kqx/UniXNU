#!/usr/bin/env python3
"""Check that a failing build step shows its whole compiler output, not a fixed tail.

The archive builders compile with -Wall -Wextra -Werror and print the compiler log themselves, because the
per-object .log files live under build/ and are not part of the CI artifact. A truncated diagnostic was the
reason a NativeUfs failure could not be read at all: the console showed the notes of twelve warnings and the
summary "12 warnings and 3 errors generated", while every actual error had been cut off by a
result.stdout[-3500:] slice. The tail of a compiler log is the least useful part of it, since clang prints
the notes of the last warning last and the first error first.

Three places truncated it, and this holds all three to the same contract:

  1. each builder that runs a compiler prints the whole captured output on failure;
  2. the archive driver (scripts/unixnu/util.py run()) shows a failing step's whole log file, not 30 lines;
  3. no builder keeps a short numeric slice of compiler output in its failure path.

The checks are static (the slices are what failed, and reproducing a real compile needs Xcode), except for
run(), which is exercised against a real failing command.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Builders that capture a compiler's output and are run as an archive step.
BUILDERS = (
    'scripts/build-corecrypto-14.py',
    'scripts/build-libpthread-kernel.py',
    'scripts/build-mockfs-fixture.py',
    'scripts/build-verified-root-probe.py',
    'scripts/audit-storage-interface.py',
)

failures = []


def check(name, condition, detail=''):
    print(f'{"ok  " if condition else "FAIL"} {name}')
    if not condition:
        failures.append(name + (f': {detail}' if detail else ''))


def main():
    # 1. A short slice of compiler output must not survive anywhere in a builder's failure path. The
    #    pattern is a numeric end-slice of stdout/stderr, e.g. result.stdout[-3500:] or (out + err)[-3500:].
    for relative in BUILDERS:
        path = ROOT / relative
        text = path.read_text()
        slices = re.findall(r'\[-\d{3,}:\]', text)
        check(f'{relative}: keeps no tail slice of compiler output', not slices, str(slices))
        check(f'{relative}: its failure path is reachable', 'SystemExit' in text or 'sys.exit' in text)

    # 2. The builders that also write a .log next to the object must still print it, because that .log is
    #    under build/ and the artifact only carries out/*/logs/**.
    for relative in ('scripts/build-libpthread-kernel.py',
                     'scripts/build-mockfs-fixture.py',
                     'scripts/build-verified-root-probe.py'):
        text = (ROOT / relative).read_text()
        check(f'{relative}: prints the whole captured output on failure', 'print(result.stdout' in text)

    # 3. run() shows the failing step's log file in full up to a generous limit, and says how much it left
    #    in the file when it truncates. A 30-line tail hid the errors this whole check exists for.
    util = (ROOT / 'scripts/unixnu/util.py').read_text()
    check('util.run: no longer shows a fixed 30-line tail', '[-30:]' not in util)
    check('util.run: shows a generous part of the log', re.search(r'limit = \d{3,}', util) is not None)
    check('util.run: names the file it left earlier lines in',
          'earlier line' in util and 'log_file' in util)

    sys.path.insert(0, str(ROOT / 'scripts'))
    from unixnu.util import Error, run

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / 'step.log'
        script = 'import sys\nfor i in range(120): print("line %d" % i)\nprint("the first error", file=sys.stderr)\nsys.exit(3)\n'
        try:
            run([sys.executable, '-c', script], log_file=log)
            check('run: a failing command raises', False)
        except Error as error:
            check('run: a failing command raises', 'failed (3)' in str(error), str(error))
        check('run: the log file keeps the whole output',
              len(log.read_text().splitlines()) == 121, str(len(log.read_text().splitlines())))

    print(f'\n{len(failures)} failure(s)')
    for name in failures:
        print(f'  {name}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
