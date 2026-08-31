"""Additively merge a Hawk-Eye archive zip into the app's data.

Adds new leaderboard rows, all_data2 entries, metadata entries and
matches_new2 folders. NEVER overwrites or removes existing data.

Usage: python merge_hawkeye_archive.py "/path/to/Archive.zip"
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

APP = Path(__file__).parent


def main(zip_path):
    arch = Path(tempfile.mkdtemp(prefix='he_archive_'))
    subprocess.run(['unzip', '-oq', zip_path, '-d', str(arch)], check=True)

    ours = pd.read_parquet(APP / 'leaderboard_haddad_new_wta_with_sets_clean.parquet')
    theirs = pd.read_parquet(arch / 'leaderboard_haddad_new_wta_with_sets_clean.parquet')
    key = lambda d: list(zip(d.player_name, d.match_id, d.sets.astype(str)))
    have = set(key(ours))
    new_rows = theirs[[k not in have for k in key(theirs)]]
    pd.concat([ours, new_rows], ignore_index=True).to_parquet(
        APP / 'leaderboard_haddad_new_wta_with_sets_clean.parquet', index=False)
    print(f'leaderboard: +{len(new_rows)} rows ({new_rows.match_id.nunique()} new matches)')

    ours2 = json.load(open(APP / 'all_data2.json'))
    theirs2 = json.load(open(arch / 'all_data2.json'))
    have2 = {(m['PLAYER'], m['match_id']) for m in ours2}
    added2 = [m for m in theirs2 if (m['PLAYER'], m['match_id']) not in have2]
    json.dump(ours2 + added2, open(APP / 'all_data2.json', 'w'))
    print(f'all_data2: +{len(added2)}')

    oursm = json.load(open(APP / 'post_match_metadata_with_hash.json'))
    theirsm = json.load(open(arch / 'post_match_metadata_with_hash.json'))
    added3 = 0
    for player, entries in theirsm.items():
        bucket = oursm.setdefault(player, [])
        havem = {e['match_id'] for e in bucket}
        for e in entries:
            if e['match_id'] not in havem:
                bucket.append(e)
                added3 += 1
    json.dump(oursm, open(APP / 'post_match_metadata_with_hash.json', 'w'), indent=4)
    print(f'metadata: +{added3}')

    copied = 0
    for d in (arch / 'matches_new2').iterdir():
        if d.is_dir() and not d.name.startswith('_') and not (APP / 'matches_new2' / d.name).exists():
            shutil.copytree(d, APP / 'matches_new2' / d.name)
            copied += 1
    for junk in (APP / 'matches_new2').rglob('._*'):
        junk.unlink()
    print(f'matches_new2: +{copied} dirs')

    if (arch / 'post_match_links.json').exists():
        oursl = json.load(open(APP / 'post_match_links.json'))
        theirsl = json.load(open(arch / 'post_match_links.json'))
        newl = {k: v for k, v in theirsl.items() if k not in oursl}
        oursl.update(newl)
        json.dump(oursl, open(APP / 'post_match_links.json', 'w'), indent=2)
        print(f'portal links: +{len(newl)}')


if __name__ == '__main__':
    main(sys.argv[1])
