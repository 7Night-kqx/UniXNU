"""XNU kernel: build from the patched Apple source, then prelink against the original kernelcache."""
import os
import shlex
from pathlib import Path

from . import ipsw
from .util import Error, expand, log, run, sha256_file, tool


def xnu_env(ctx):
    """CONFIG_XNU_* of the defconfig become XNU_* variables of the legacy kernel build script."""
    env = {}
    for key, value in ctx.need_config().items():
        if not key.startswith('XNU_'):
            continue
        if isinstance(value, str):
            value = value.replace('{tree}', str(ctx.tree))
        env[key] = '1' if value is True else '0' if value is False else str(value)
    return env


def version_env(modules):
    """Source versions of the Apple references, from feeds.toml, for the kernel scripts."""
    env = {}
    for name, prefix in (('xnu', 'XNU'), ('libplatform', 'LIBPLATFORM'), ('libdispatch', 'LIBDISPATCH'), ('AvailabilityVersions', 'AVAILABILITYVERSIONS')):
        module = modules.get(('refer', name))
        entry = module.source if module and module.source else {}
        if entry.get('ref'):
            env[f'UNIXNU_{prefix}_TAG'] = entry['ref']
        if entry.get('commit'):
            env[f'UNIXNU_{prefix}_COMMIT'] = entry['commit']
    xnu = (modules.get(('refer', 'xnu')) or None) and modules[('refer', 'xnu')].source or {}
    for key, variable in (('darwin', 'UNIXNU_XNU_DARWIN'), ('version', 'UNIXNU_XNU_VERSION'),
                          ('driverkit_tag', 'UNIXNU_DRIVERKIT_TAG'), ('trustcache_tag', 'UNIXNU_TRUSTCACHE_TAG')):
        if xnu.get(key):
            env[variable] = xnu[key]
    return env


def toolchain_path():
    """PATH with the Homebrew LLVM and LLD first, as the archive builders expect."""
    extra = [d for d in ('/opt/homebrew/opt/llvm/bin', '/opt/homebrew/opt/lld/bin', '/usr/local/opt/llvm/bin', '/usr/local/opt/lld/bin')
             if Path(d).is_dir()]
    return os.pathsep.join(extra + [os.environ.get('PATH', '')])


def kernelcache(ctx):
    """The original kernelcache this board is qualified against, from the option, the board pin, or the IPSW."""
    spec = ctx.board.get('kernel', {}).get('prelink') or {}
    cache = ctx.option('kernelcache', 'UNIXNU_KERNELCACHE') or (expand(ctx.tree / spec['kernelcache']) if spec.get('kernelcache') else None)
    if not cache:
        # Not given: take it from the IPSW (--ipsw PATH_OR_URL, or the url of board.toml [ipsw]).
        cache = ipsw.kernelcache(ctx, ipsw.Ipsw(ctx))
    if not cache.is_file():
        raise Error(f'kernelcache not found: {cache}')
    wanted = spec.get('kernelcache_sha256')
    if wanted and sha256_file(cache) != wanted:
        raise Error(f'{cache} does not match the kernelcache this board was qualified against (sha256 {wanted})')
    return cache


def build_archives(ctx, env):
    """Run the board's archive builders ([kernel] archives of board.toml), in order, then check the prebuilt archives.

    Each entry is a script of the build tree with its arguments. The kernel link needs their archives, and some of
    them read the compile records that an XNU pass leaves behind.
    """
    entries = ctx.board.get('kernel', {}).get('archives', [])
    env = dict(env, PATH=toolchain_path())
    # A builder that resolves symbols against the original kernelcache needs it before the link, not only in the
    # prelink step that runs after it. Resolve it here once (the IPSW read is cached) and hand it over the way the
    # prelink step resolves it, so both use the same file and the same pin.
    if any('build-storage-kext-bindings.py' in entry for entry in entries):
        env['UNIXNU_KERNELCACHE'] = str(kernelcache(ctx))
        # ...and the rebase the prelink step will apply to that image. The bindings are absolute
        # addresses copied out of the original layout, so a kext-owned one must move with the
        # component; kernel exports are resolved against the new kernel and must not.
        env['UNIXNU_PRELINK_SLIDE'] = str(ctx.board.get('kernel', {}).get('prelink', {}).get('slide', '0'))
    # The storage transports include <IOKit/storage/IOBlockStorageDevice.h>, which is not in the xnu tree: the
    # classes live in Apple's separate IOStorageFamily project, fetched as a reference. The builders add
    # build/storage-abi/include to their command line, so stage it (idempotently) before the first of them
    # runs; staging also rewrites a header whose source changed, which a presence test would miss.
    transports = ('NativeUfs', 'NativeVirtioBlock', 'NativeRamBlock')
    if any(name in entry for entry in entries for name in transports):
        log('kernel: stage the IOStorageFamily headers the storage transports compile against')
        run(['python3', ctx.tree / 'scripts/storage_abi_headers.py'], cwd=ctx.tree, env=env,
            log_file=ctx.logs / 'storage-abi-headers.log')
    for index, entry in enumerate(entries, 1):
        parts = shlex.split(entry)
        script = ctx.tree / 'scripts' / parts[0]
        if not script.is_file():
            raise Error(f'[kernel] archives: {script} missing')
        log(f'kernel: archive {index}/{len(entries)}: {entry}')
        run(['python3', script, *parts[1:]], cwd=ctx.tree, env=env, log_file=ctx.logs / f'archive-{index:02d}-{Path(parts[0]).stem}.log')
    # Archives that no builder produces (they need inputs outside the repositories) must be supplied.
    for key, value in sorted(xnu_env(ctx).items()):
        if key.endswith('_ARCHIVE') and value.endswith('.a') and not Path(value).is_file():
            raise Error(f'{key}: {value} not found; no builder makes it, supply the archive')


def build(ctx, modules):
    log('kernel: XNU')
    for name in ('git', 'make', 'clang', 'cmake', 'ninja', 'unifdef'):
        tool(name, 'brew install ' + name)
    tool('xcodebuild', 'the kernel step builds with the Xcode iphoneos SDK')
    script = ctx.tree / 'scripts/build-xnu-4k-baseline.sh'
    if not script.is_file():
        raise Error(f'{script} missing')
    env = dict(os.environ)
    env.update(xnu_env(ctx))
    env.update(version_env(modules))
    env['JOBS'] = str(ctx.jobs)
    record = ctx.tree / 'build/xnu/ios-obj/DEVELOPMENT_ARM64_BCM2837/osfmk/DEVELOPMENT/startup.o.json'
    if not record.is_file():
        # The archive builders and the boot progress layer read compile records of the XNU build, which only a
        # compiled tree leaves behind. A first build from scratch runs one pass in bootstrap mode: the archive
        # section of the script is skipped (its output does not exist yet) and make is allowed to fail at the
        # link, which needs those archives. Only the records are required of that pass.
        log('kernel: bootstrap pass for the compile records')
        subprocess_env = {**env, 'XNU_BOOT_PROGRESS': '0', 'XNU_BOOTSTRAP': '1'}
        run(['bash', script], cwd=ctx.tree, env=subprocess_env, log_file=ctx.logs / 'kernel-bootstrap.log')
    build_archives(ctx, env)
    run(['bash', script], cwd=ctx.tree, env=env, log_file=ctx.logs / 'kernel.log')


def prelink(ctx):
    """Produce out/<device>/kernel/kernel.macho from the XNU build and the original kernelcache."""
    log('kernel: prelink')
    spec = ctx.board.get('kernel', {}).get('prelink')
    if not spec:
        raise Error('board.toml has no [kernel.prelink]')
    cache = kernelcache(ctx)
    kernel = ctx.tree / spec['kernel']
    if not kernel.is_file():
        raise Error(f'{kernel} not found; run "unixnu build kernel" first')
    output = ctx.work / 'kernel/kernel.macho'
    output.parent.mkdir(parents=True, exist_ok=True)
    # emit_prelink refuses to overwrite; a rebuild replaces the previous candidate and its record.
    for stale in (output, output.with_suffix('.json')):
        stale.unlink(missing_ok=True)
    command = ['python3', ctx.tree / spec['tool'], '--kernel', kernel, '--prelinked', cache,
               f'--slide={spec["slide"]}', '--output', output]
    for root in spec.get('roots', []):
        command += ['--root', root]
    if spec.get('early_security_init'):
        command += ['--early-security-init', spec['early_security_init']]
    command += spec.get('extra_args', [])
    run(command, cwd=ctx.tree, log_file=ctx.logs / 'prelink.log')
    log(f'kernel: {output} sha256 {sha256_file(output)}')
    return output
