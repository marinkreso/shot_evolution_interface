"""Clips tab data: lists per-match video clips from the gsa-operations blob.

Clips live at custom-clips/{PLAYER}/{timestamp}/{match_id}-{player}-{title}.mp4.
When the same title exists in several timestamp folders (regenerated batches),
the newest folder wins.
"""
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ACCOUNT_URL = 'https://operationslakedb.blob.core.windows.net'
CONTAINER = 'gsa-operations'
# read+list SAS for the gsa-operations container; set GSA_OPERATIONS_SAS in the
# environment. Without it clip listing just returns nothing (the CLIPS tab is
# hidden by default anyway) — never hardcode the token, this repo is public.
SAS_TOKEN = os.environ.get('GSA_OPERATIONS_SAS', '')

# first keyword match wins, so more specific sections come first
_SECTIONS = [
    ('SERVES', ('serve', 'double fault', 'ace')),
    ('RETURNS', ('return',)),
    ('NET PLAY', ('approach', 'net', 'volley', 'drop shot', 'passing')),
    ('GROUNDSTROKES', ('winners', 'unforced', 'forcing', 'fh', 'bh', 'forehand', 'backhand')),
    ('RALLIES & POINTS', ('point', 'rally', 'shots', 'pressure', 'break')),
]
_SECTION_ORDER = [name for name, _ in _SECTIONS] + ['OTHER']


def _section_for(title):
    t = title.lower()
    for name, keywords in _SECTIONS:
        if any(k in t for k in keywords):
            return name
    return 'OTHER'


def list_match_clips(player, match_id):
    """Return {section: [(title, url), ...]} for this match's clips, {} if none."""
    if not SAS_TOKEN:
        return {}
    prefix = f'custom-clips/{player}/'
    names, marker = [], ''
    try:
        while True:
            qs = urllib.parse.urlencode({'restype': 'container', 'comp': 'list',
                                         'prefix': prefix, 'maxresults': '5000', 'marker': marker})
            with urllib.request.urlopen(f'{ACCOUNT_URL}/{CONTAINER}?{qs}&{SAS_TOKEN}', timeout=20) as r:
                root = ET.fromstring(r.read())
            names += [b.findtext('Name') for b in root.iter('Blob')
                      if (b.findtext('Name') or '').lower().endswith('.mp4')]
            marker = root.findtext('NextMarker') or ''
            if not marker:
                break
    except Exception as e:
        print(f'clip listing failed for {player}: {e}')
        return {}

    match_prefix = f'{match_id.lower()}-'
    by_title = {}
    for name in sorted(names):  # sorted so the newest timestamp folder wins
        base = name.rsplit('/', 1)[-1][:-len('.mp4')]
        if not base.lower().startswith(match_prefix):
            continue
        rest = base[len(match_prefix):]
        title = rest.split('-', 1)[1] if '-' in rest else rest
        by_title[title] = f'{ACCOUNT_URL}/{CONTAINER}/{urllib.parse.quote(name)}?{SAS_TOKEN}'

    sections = {}
    for title in sorted(by_title):
        sections.setdefault(_section_for(title), []).append((title, by_title[title]))
    return {s: sections[s] for s in _SECTION_ORDER if s in sections}
