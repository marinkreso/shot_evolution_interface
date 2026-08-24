"""Generate the matplotlib court figures for CV matches and upload to the
gsa-post-match blob: serve_placement, return_depth, return_dir_deuce/ad and
the contact-point figures (first/second_return_fig, first/second_splus_fig,
rallies_fig) — for the whole match and per set (suffix _<set>), exactly the
files the post-match page requests.

Usage: python cv_generate_fig_images.py
"""
import json
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from azure.storage.blob import BlobServiceClient

import cv_court_figs as figs
import cv_pipeline as pipe
from cv_build_post_match import make_match_id, parse_title
from cv_generate_court_images import SAS_TOKEN, ACCOUNT_URL, CONTAINER


def get_container():
    return BlobServiceClient(account_url=ACCOUNT_URL, credential=SAS_TOKEN).get_container_client(CONTAINER)


def save_fig(function, args, save_path):
    plt.clf()
    if function == figs.plot_serve_placement:
        ax, fig = function(*args)
    else:
        fig = function(*args)
    try:
        fig.set_tight_layout(True)
    except Exception:
        pass
    fig.savefig(save_path)
    plt.close(fig)
    plt.clf()


def render_set(df_set, me, set_suffix, out_dir):
    """The notebook's process_set_visualizations task list, verbatim filters."""
    serve_filter = df_set[(df_set.shot_no == 1) & (df_set.serve_number == 1)
                          & (df_set.is_shot_in == 1) & (df_set.server_name == me)]
    dfc_return = df_set[(df_set.PLAYER_HIT == me) & (df_set.shot_no == 2) & (df_set.serve_number == 1)]
    dfc_return_second = df_set[(df_set.PLAYER_HIT == me) & (df_set.shot_no == 2) & (df_set.serve_number == 2)]
    dfc_splus = df_set[(df_set.PLAYER_HIT == me) & (df_set.shot_no == 3) & (df_set.serve_number == 1)]
    dfc_splus_second = df_set[(df_set.PLAYER_HIT == me) & (df_set.shot_no == 3) & (df_set.serve_number == 2)]
    dfc_rallies = df_set[(df_set.PLAYER_HIT == me) & (df_set.shot_no > 3)]

    tasks = [
        (figs.visualize_return_depth,
         (df_set, df_set.match_id.unique(), '1st_serve', 'all_sides', ['all_directions'], True),
         f'return_depth{set_suffix}.png'),
        (figs.visualize_return_direction,
         (df_set, df_set.match_id.unique(), '2nd_serve', 'deuce', ['all_directions'], True),
         f'return_dir_deuce{set_suffix}.png'),
        (figs.visualize_return_direction,
         (df_set, df_set.match_id.unique(), '2nd_serve', 'ad', ['all_directions'], True),
         f'return_dir_ad{set_suffix}.png'),
        (figs.plot_serve_placement, (serve_filter,), f'serve_placement{set_suffix}.png'),
        (figs.plot_contact_points_percentages, (dfc_return, '1ST RETURN'), f'first_return_fig{set_suffix}.png'),
        (figs.plot_contact_points_percentages, (dfc_return_second, '2ND RETURN'), f'second_return_fig{set_suffix}.png'),
        (figs.plot_contact_points_percentages, (dfc_splus, '1ST SERVE+1'), f'first_splus_fig{set_suffix}.png'),
        (figs.plot_contact_points_percentages, (dfc_splus_second, '2ND SERVE+1'), f'second_splus_fig{set_suffix}.png'),
        (figs.plot_contact_points_percentages, (dfc_rallies, 'RALLIES'), f'rallies_fig{set_suffix}.png'),
    ]
    written = []
    for function, args, name in tasks:
        path = out_dir / name
        try:
            save_fig(function, args, path)
            written.append(path)
        except Exception as e:
            print(f'  fig {name} failed: {str(e)[:90]}', flush=True)
    return written


def process_one(task):
    parquet, match_id, me, opp = task
    folder = f'{str(me).upper()}_{match_id}/'
    try:
        container = get_container()
        if container.get_blob_client(folder + 'rallies_fig.png').exists():
            return f'skip {folder}'
        cvdf = pd.read_parquet(parquet)
        cvdf['match_id'] = match_id
        for col in ('ON_NET_Y', 'ON_NET_Z', 'CONTACT_Z', 'SPEED', 'SPEED_3D',
                    'bounce_x', 'bounce_y', 'hit_x', 'hit_y',
                    'player_location_x', 'player_location_y',
                    'receiver_location_x', 'receiver_location_y'):
            if col in cvdf.columns:
                cvdf[col] = pd.to_numeric(cvdf[col], errors='coerce')
        df = pipe.cv_adapter.add_he_features(cvdf)
        df = pipe.joschka.resolve_serve_attempts(df)
        df['CONTACT_X'] = df['hit_x']
        df['CONTACT_Y'] = df['hit_y']
        df['REBOUND_X'] = df['bounce_x']
        df['REBOUND_Y'] = df['bounce_y']
        df['is_in_the_net'] = df['placement_gsa'].astype(str).str.contains('Net', na=False).astype(int)
        df['NET_COORD_Y'] = pd.to_numeric(df.get('ON_NET_Y'), errors='coerce')
        df['NET_COORD_Z'] = pd.to_numeric(df.get('ON_NET_Z'), errors='coerce')
        figs.selected_player_name = me   # the notebook plot fns read this global
        figs.selected_player_initials = str(me)[:2].upper()
        out_dir = Path(tempfile.mkdtemp(prefix='cv_figs_'))
        uploaded = 0
        sets = [None] + sorted(int(s) for s in df.set_no.unique())
        for set_no in sets:
            df_set = df[df.set_no == set_no] if set_no is not None else df
            suffix = f'_{set_no}' if set_no is not None else ''
            for path in render_set(df_set, me, suffix, out_dir):
                with open(path, 'rb') as fh:
                    container.get_blob_client(folder + path.name).upload_blob(fh, overwrite=True)
                uploaded += 1
        return f'uploaded {folder} ({uploaded} figs)'
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
    # same match may appear under two titles; keep one task per folder
    seen, unique = set(), []
    for t in tasks:
        key = (str(t[2]).upper(), t[1])
        if key not in seen:
            seen.add(key)
            unique.append(t)
    print(f'tasks: {len(unique)}', flush=True)
    done = failed = 0
    with ProcessPoolExecutor(max_workers=6) as ex:
        for result in ex.map(process_one, unique):
            print(result, flush=True)
            failed += result.startswith('FAILED')
            done += not result.startswith('FAILED')
    print(f'DONE ok: {done} | failed: {failed}', flush=True)


if __name__ == '__main__':
    main()
