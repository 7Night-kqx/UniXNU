#!/usr/bin/env python3
"""Restore omitted DriverKit headers from Apple's earlier Darwin 23 source."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

# Tags of the Apple sources that still carry the headers newer xnu omits; feeds.toml sets them for the unixnu driver.
TAG = os.environ.get('UNIXNU_DRIVERKIT_TAG', 'xnu-10063.121.3')
TRUST_TAG = os.environ.get('UNIXNU_TRUSTCACHE_TAG', 'xnu-8796.101.5')
DESTINATION = Path('.cache/xnu-work/iokit/DriverKit')
CACHE = Path(f'.cache/sources/xnu-driverkit-{TAG.removeprefix("xnu-")}.json')
URL = f'https://api.github.com/repos/apple-oss-distributions/xnu/contents/iokit/DriverKit?ref={TAG}'
# The contents listings go to api.github.com, which serves an unauthenticated caller only 60 requests per
# hour per egress IP. A CI runner shares that IP with every other job on the host, so the first listing can
# already return 403. GITHUB_TOKEN raises the budget to 5000 requests per hour; the retries cover the
# secondary "abuse detection" 403 that a burst can still produce.
TOKEN = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
RETRY_STATUS = (403, 429, 500, 502, 503, 504)


def fetch(url):
    """Fetch one URL with the token of the job and a bounded exponential backoff."""
    request = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'unixnu'})
    # Only the API host gets the token: download_url points at raw.githubusercontent.com, which needs none and
    # must not receive a credential.
    if TOKEN and urllib.parse.urlsplit(url).hostname == 'api.github.com':
        request.add_header('Authorization', 'Bearer ' + TOKEN)
    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code not in RETRY_STATUS:
                raise SystemExit(f'{url}: HTTP {error.code}') from error
            if attempt == 5:
                hint = (' (API rate limit: GITHUB_TOKEN raises 60 to 5000 requests per hour; is it set for this step?)'
                        if error.code == 403 else '')
                raise SystemExit(f'{url}: HTTP {error.code} after {attempt} attempts{hint}') from error
            time.sleep(int(error.headers.get('Retry-After') or 2 ** attempt))
    raise AssertionError('unreachable')


def restore(entry, destination=DESTINATION, tag=TAG):
    if entry['type'] != 'file' or not entry['name'].endswith('.h'):
        return None
    name = entry.get('relative', entry['name'])
    target = destination / name
    if target.exists():
        return None
    data = fetch(entry['download_url'])
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if digest != entry['sha']:
        raise ValueError(f'Git blob hash mismatch: {entry["name"]}')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'name': name, 'source_tag': tag, 'git_blob': digest,
            'sha256': hashlib.sha256(data).hexdigest()}


if __name__ == '__main__':
    if not DESTINATION.is_dir():
        raise SystemExit('Create the local XNU work source before preparing headers')
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_bytes(fetch(URL))
    entries = json.loads(CACHE.read_text())
    crypto_cache = CACHE.with_name(f'xnu-driverkit-crypto-{TAG.removeprefix("xnu-")}.json')
    if not crypto_cache.exists():
        crypto_url = URL.replace('/DriverKit?', '/DriverKit/crypto?')
        crypto_cache.write_bytes(fetch(crypto_url))
    for entry in json.loads(crypto_cache.read_text()):
        entry['relative'] = 'crypto/' + entry['name']
        entries.append(entry)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        restored = [entry for entry in executor.map(restore, entries) if entry]
        trust_tag = TRUST_TAG
        trust_cache = CACHE.with_name(f'xnu-trustcache-{TRUST_TAG.removeprefix("xnu-")}.json')
        if not trust_cache.exists():
            url = ('https://api.github.com/repos/apple-oss-distributions/xnu/'
                   f'contents/EXTERNAL_HEADERS/TrustCache?ref={trust_tag}')
            trust_cache.write_bytes(fetch(url))
        trust_destination = Path('.cache/xnu-work/EXTERNAL_HEADERS/TrustCache')
        def restore_trust(entry):
            return restore(entry, trust_destination, trust_tag)
        restored.extend(entry for entry in executor.map(
            restore_trust, json.loads(trust_cache.read_text())) if entry)
    previous = Path('.cache/sources/xnu-restored-headers.json')
    existing = json.loads(previous.read_text()) if previous.exists() else []
    by_name = {entry['name']: entry for entry in existing + restored}
    previous.write_text(json.dumps(list(by_name.values()), indent=2) + '\n')
    print(f'Restored {len(restored)} omitted public headers from Apple; blob hashes verified')
