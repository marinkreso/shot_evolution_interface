"""Generate serve/return court PNGs for CV matches and upload them to the
gsa-post-match Azure container under <PLAYER>_<match_id>/ — the exact URLs the
post-match page already requests (first_serve.png, second_serve.png,
first_return.png, second_return.png).

Visual logic mirrors the CV notebook's create_serve_visual_win_cv /
create_return_visual_win_cv. Only hard-court template assets exist on the
assets blob, so every court renders on the hard template for now.

Usage: python cv_generate_court_images.py
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from azure.storage.blob import BlobServiceClient

from pdf_generator.visuals.templates import ColorPreset, good_returns_template, serve_location_template
from pdf_generator.models.enums import SurfaceCode

from cv_build_post_match import make_match_id, parse_title

SAS_TOKEN = 'sp=racwdlmeop&st=2026-04-02T11:11:58Z&se=2026-10-31T20:26:58Z&spr=https&sv=2024-11-04&sr=c&sig=wtpzevJxs5tgD%2BXsfF2L3hv%2FHgwQUc06zNX5sbhprxg%3D'
ACCOUNT_URL = 'https://operationslakedb.blob.core.windows.net'
CONTAINER = 'gsa-post-match'


def get_container():
    return BlobServiceClient(account_url=ACCOUNT_URL, credential=SAS_TOKEN).get_container_client(CONTAINER)


def _ratio(x, y):
    if not y or (isinstance(y, float) and np.isnan(y)):
        return 0
    return int(round(100.0 * x / y))


def _serve_populations(df, server, serve_number, returning):
    """Six (placement x court-side) populations ordered for the template."""
    op = (df.impact_player != server) if returning else (df.impact_player == server)
    serves = df[(df.shot == 1) & (df.serve == df.serve_number) & op & (df.serve_number == serve_number)]
    ad = serves[serves.deuce_or_ad == 'ad']
    deuce = serves[serves.deuce_or_ad == 'deuce']
    d_t, d_w, d_b = (deuce[deuce.placement_gsa == p] for p in ('T', 'Wide', 'Body'))
    a_t, a_w, a_b = (ad[ad.placement_gsa == p] for p in ('T', 'Wide', 'Body'))
    all_d = len(d_t) + len(d_b) + len(d_w)
    all_a = len(a_t) + len(a_b) + len(a_w)
    if returning:
        groups = [d_w, d_b, d_t, a_t, a_b, a_w]
        widths = [_ratio(len(d_w), all_d), _ratio(len(d_b), all_d), _ratio(len(d_t), all_d),
                  _ratio(len(a_t), all_a), _ratio(len(a_b), all_a), _ratio(len(a_w), all_a)]
    else:
        groups = [a_w, a_b, a_t, d_t, d_b, d_w]
        widths = [_ratio(len(a_w), all_a), _ratio(len(a_b), all_a), _ratio(len(a_t), all_a),
                  _ratio(len(d_t), all_d), _ratio(len(d_b), all_d), _ratio(len(d_w), all_d)]
    return groups, widths


def serve_visual(df, server, serve_number, player_label, opponent_label):
    groups, widths = _serve_populations(df, server, serve_number, returning=False)
    pies = [_ratio(len(g[g.impact_player == g.point_winner]), len(g)) for g in groups]
    return serve_location_template(
        player_name=player_label, opponent_name=opponent_label,
        serve_no='1st' if serve_number == 1 else '2nd',
        arrows_widths=widths, arrows_numbers=[f'{w}%' for w in widths],
        surface=SurfaceCode.HARD, numbers=[len(g) for g in groups],
        pies_percentages=pies, preset=ColorPreset.ORANGE)


def return_visual(df, server, serve_number, player_label, opponent_label):
    groups, widths = _serve_populations(df, server, serve_number, returning=True)
    pies = [_ratio(len(g[g.impact_player != g.point_winner]), len(g)) for g in groups]
    return good_returns_template(
        player_name=player_label, opponent_name=opponent_label,
        serve_no='1st' if serve_number == 1 else '2nd',
        arrows_widths=widths, arrows_numbers=[f'{w}%' for w in widths],
        surface=SurfaceCode.HARD, numbers=[len(g) for g in groups],
        pies_percentages=pies, preset=ColorPreset.ORANGE)


def process_one(task):
    """Render + upload the 4 court images for one (match, player). Skips
    folders whose images are already on the blob, so reruns are cheap."""
    parquet, match_id, me, opp = task
    folder = f'{str(me).upper()}_{match_id}/'
    try:
        container = get_container()
        if container.get_blob_client(folder + 'second_return.png').exists():
            return f'skip {folder}'
        df = pd.read_parquet(parquet)
        images = {
            'first_serve.png': serve_visual(df, me, 1, str(me).upper(), str(opp).upper()),
            'second_serve.png': serve_visual(df, me, 2, str(me).upper(), str(opp).upper()),
            'first_return.png': return_visual(df, me, 1, str(me).upper(), str(opp).upper()),
            'second_return.png': return_visual(df, me, 2, str(me).upper(), str(opp).upper()),
        }
        tmp = Path(tempfile.mkdtemp(prefix='cv_courts_'))
        for name, img in images.items():
            path = tmp / name
            img.save(path, optimize=True)
            with open(path, 'rb') as fh:
                container.get_blob_client(folder + name).upload_blob(fh, overwrite=True)
        return f'uploaded {folder}'
    except Exception as e:
        return f'FAILED {folder}: {str(e)[:120]}'


def main():
    from concurrent.futures import ProcessPoolExecutor
    with open(HERE / 'cv_match_candidates.json') as f:
        candidates = json.load(f)
    tasks = []
    for player_label, info in candidates.items():
        for m in info['picked']:
            if m.get('duplicate_of_previous'):
                continue
            tournament, year, name_a, name_b = parse_title(m['title'], m['date'])
            match_id = make_match_id(tournament, year, name_a.split()[-1], name_b.split()[-1])
            df = pd.read_parquet(m['parquet'])
            players = [p for p in df.impact_player.dropna().unique()]
            if len(players) != 2:
                continue
            for me in players:
                opp = [p for p in players if p != me][0]
                tasks.append((m['parquet'], match_id, me, opp))
    print(f'tasks: {len(tasks)}', flush=True)
    done = failed = 0
    with ProcessPoolExecutor(max_workers=6) as ex:
        for result in ex.map(process_one, tasks):
            print(result, flush=True)
            failed += result.startswith('FAILED')
            done += not result.startswith('FAILED')
    print(f'DONE ok: {done} | failed: {failed}', flush=True)


if __name__ == '__main__':
    main()
