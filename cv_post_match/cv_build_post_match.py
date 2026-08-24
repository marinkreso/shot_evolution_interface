"""Build post-match report artifacts from CV match parquets.

For every picked match in cv_match_candidates.json this produces, for BOTH
players of the match:

  * leaderboard rows (ALL + per set) in the clean-leaderboard scale, written
    to leaderboard_cv.parquet (kept separate from the Hawk-Eye parquet; the
    app concatenates them at load time)
  * matches_new2/<PLAYER>_<match_id>/movement.json + haddad_games.csv
  * an entry (with hash id) in post_match_metadata_with_hash.json

Usage: python cv_build_post_match.py
"""
import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

import cv_pipeline as pipe

HERE = Path(__file__).parent
APP = HERE.parent
HASH_SALT = 'gHts'

# tournament keyword -> surface (edit freely; default is hard)
SURFACES = {
    'colsanitas': 'clay', 'rabat': 'clay', 'tanger': 'clay', 'gandia': 'clay',
    'trieste': 'clay', 'sion': 'clay', 'zug': 'clay', 'klosters': 'clay',
    'hamburg': 'clay', 'hechingen': 'clay', 'darmstadt': 'clay',
    'stuttgart-vaihingen': 'clay', 'santa margherita': 'clay',
    'kursumlijska': 'clay', 'petits as': 'hard', 'goyang': 'hard',
    'columbus': 'hard', 'chihuahua': 'hard', 'arcadia': 'hard',
    'croissy': 'hard', 'dc open': 'hard',
}


def _slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s.strip()).strip('_')


def parse_title(title, date_str):
    """-> (tournament, year, name_a, name_b) from either title format."""
    if date_str:
        year = date_str.split('/')[-1]
    else:  # some API entries carry no matchDate; fall back to the title
        m = re.search(r'(20\d\d)', title)
        year = m.group(1) if m else '2026'
    if '|' in title:
        parts = [p.strip() for p in title.split('|')]
        tournament = parts[0]
        vs_part = parts[-1].split(' - ')[0]
    else:
        segs = title.split(' - ')
        vs_part, tournament = segs[0], segs[1]
    names = re.split(r'\s+vs\.?\s+', vs_part, flags=re.I)
    return tournament, year, names[0].strip(), names[1].strip()


def surface_for(tournament):
    t = tournament.lower()
    for key, surf in SURFACES.items():
        if key in t:
            return surf
    return 'hard'


def make_match_id(tournament, year, last_a, last_b):
    t = _slug(tournament)
    if not re.search(r'20\d\d', t):
        t = f'{t}_{year}'
    return f'{t}_CV_{_slug(last_a)}_{_slug(last_b)}'


def _fmt_pct_times(counts, total):
    return {k: f'{(0 if not total else round(100 * v / total))}% ({v} times)' for k, v in counts.items()}


def _bucketize(values, edges, labels):
    counts = OrderedDict((lab, 0) for lab in labels)
    vals = [v for v in values if v is not None and not np.isnan(v)]
    for v in vals:
        for (lo, hi), lab in zip(edges, labels):
            if lo <= v < hi:
                counts[lab] += 1
                break
    return counts, len(vals)


def _ts_minutes(a, b):
    try:
        return (pd.to_timedelta(b) - pd.to_timedelta(a)).total_seconds() / 60.0
    except Exception:
        return None


def build_movement_json(df, player, opponent, sets):
    """df: adapter frame for one match. player/opponent: frame-form names."""
    mine = df[df.impact_player == player]
    dist = (mine.get('move_spd_avg') * mine.get('time_passed')).dropna()

    start, end = df.start_time.iloc[0], df.end_time.iloc[-1]
    total_min = _ts_minutes(start, end)
    pts = df.drop_duplicates('point_id')
    eff_min = sum(filter(None, (_ts_minutes(a, b) for a, b in zip(pts.start_time, pts.end_time))))

    movement_data = {
        'Total Match Duration': f'{round(total_min)} minute(s)' if total_min else 'NA',
        'Effective Playing Time': f'{round(eff_min)} minute(s)',
        'Effective Time / Total Match Duration': f'{round(100 * eff_min / total_min)}%' if total_min else 'NA',
        'Total Distance Covered': f'{round(dist.sum(), 1)} m',
        'Avg Speed': f"{round(mine.move_spd_avg.dropna().mean(), 2)} m/s" if mine.move_spd_avg.notna().any() else 'NA',
        'Sum of All Strokes': int(len(mine)),
    }

    ev = mine['events.shot'].astype(str)
    shots_numbers = {
        'First Serve': int(((mine.shot_no == 1) & (mine.serve_attempt == 1)).sum()),
        'Second Serve': int(((mine.shot_no == 1) & (mine.serve_attempt == 2)).sum()),
        'Forehand': int(((mine.shot_no > 2) & (mine.stroke == 'forehand')).sum()),
        'Backhand': int(((mine.shot_no > 2) & (mine.stroke == 'backhand')).sum()),
        'Forehand Return': int(((mine.shot_no == 2) & (mine.stroke == 'forehand')).sum()),
        'Backhand Return': int(((mine.shot_no == 2) & (mine.stroke == 'backhand')).sum()),
        'Volleys': int(ev.str.contains('volley').sum()),
        'Slices': int((ev == 'slice').sum()),
        'Dropshots': int((ev == 'dropshot').sum()),
    }

    dm_counts, dm_n = _bucketize(dist.tolist(),
                                 [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 99)],
                                 ['0-1 m', '1-2 m', '2-3 m', '3-4 m', '4-5 m', '5-10 m', '10+ m'])
    per_point = (mine.assign(_d=mine.get('move_spd_avg') * mine.get('time_passed'))
                     .groupby('point_id')['_d'].sum(min_count=1).dropna())
    dp_counts, dp_n = _bucketize(per_point.tolist(),
                                 [(0, 10), (10.0001, 25), (25.0001, 50), (50.0001, 75), (75.0001, 100), (100.0001, 500)],
                                 ['0-10 m', '11-25 m', '26-50 m', '51-75 m', '76-100 m', '101-500 m'])
    sp_counts, sp_n = _bucketize(mine.get('move_spd_max').tolist(),
                                 [(0, 1), (1, 1.5), (1.5, 2), (2, 2.5), (2.5, 3), (3, 3.5), (3.5, 99)],
                                 ['0 - 1 m/s', '1 - 1.5 m/s', '1.5 - 2 m/s', '2 - 2.5 m/s', '2.5 - 3 m/s', '3 - 3.5 m/s', '3.5+ m/s'])

    def placements(attempt):
        serves = df[(df.shot_no == 1) & (df.impact_player == player) & (df.serve_attempt == attempt)]
        label_no = '1st' if attempt == 1 else '2nd'
        out = {}
        for side in ('DEUCE', 'AD'):
            sub = serves[serves.serve_deuce_or_ad == side.lower()]
            total = len(sub[sub.placement_gsa.isin(['Wide', 'Body', 'T'])])
            for code, place in (('W', 'Wide'), ('B', 'Body'), ('T', 'T')):
                s = sub[sub.placement_gsa == place]
                pct = 0 if not total else round(100 * len(s) / total)
                win = round(100 * (s.PLAYER_WIN_NAME == player).mean()) if len(s) else float('nan')
                out[f'{label_no} {side} {code}'] = f'{pct}% ({len(s)} serves), {win} win%'
        return out

    p1 = placements(1)
    first_serve_placement = ', '.join(
        f'{k}: {v.split("%")[0]}%' for k, v in p1.items() if not k.split()[-1] == 'B')

    dropshot_runs = int(((mine.shot_no > 1) &
                         (df['events.shot'].shift(1) == 'dropshot').reindex(mine.index, fill_value=False)).sum())

    return {
        'selected_player_name': player.upper(),
        'opponent_name': opponent.upper(),
        'Movement_data': movement_data,
        '1st_serve_placement': first_serve_placement,
        'Number of runs to reach dropshots': dropshot_runs,
        'path_to_games': 'haddad_games.csv',
        'shots_data_numbers': shots_numbers,
        'distance_moved': _fmt_pct_times(dm_counts, dm_n),
        'distance_moved_per_point': _fmt_pct_times(dp_counts, dp_n),
        'number_of_sprints': _fmt_pct_times(sp_counts, sp_n),
        'placement_first': p1,
        'placement_second': placements(2),
        'sets': ['ALL'] + [str(s) for s in sets],
        'source': 'cv',
    }


def build_games_csv(df, player):
    mine = df[df.impact_player == player].copy()
    games = df[['set_no', 'game_no']].drop_duplicates().reset_index(drop=True)
    games['ordinal'] = games.index + 1
    key = df.set_no.astype(str) + '_' + df.game_no.astype(str)
    ordinal = dict(zip(games.set_no.astype(str) + '_' + games.game_no.astype(str), games.ordinal))
    mine['_g'] = (mine.set_no.astype(str) + '_' + mine.game_no.astype(str)).map(ordinal)
    mine['_split'] = ((mine['_g'] - 1) // 6).astype(int)
    mine['_dist'] = mine.get('move_spd_avg') * mine.get('time_passed')
    rows = []
    for split, grp in mine.groupby('_split'):
        lo, hi = split * 6 + 1, split * 6 + 6
        per_point = grp.groupby('point_id')['_dist'].sum(min_count=1).dropna()
        serves = grp[grp.shot_no == 1]
        fh = grp[(grp.shot_no > 2) & (grp.stroke == 'forehand') & (grp.is_shot_in == 1)]
        bh_all = grp[(grp.shot_no > 2) & (grp.stroke == 'backhand') & (grp.is_shot_in == 1)]
        bh_no_slice = bh_all[bh_all['events.shot'] != 'slice']
        rows.append({
            'Game Description': f'{lo}-{hi} game split',
            'Distance covered per point': round(per_point.mean(), 2) if len(per_point) else np.nan,
            'Average movement speed': round(grp.move_spd_avg.dropna().mean(), 2) if grp.move_spd_avg.notna().any() else np.nan,
            'Average acceleration': round(grp.move_acc_max.dropna().mean(), 2) if 'move_acc_max' in grp and grp.move_acc_max.notna().any() else np.nan,
            'Average deceleration': round(grp.move_dec_max.dropna().mean(), 2) if 'move_dec_max' in grp and grp.move_dec_max.notna().any() else np.nan,
            'Serve Speed Avg': round(serves.SPEED.dropna().mean(), 2) if len(serves) else np.nan,
            'Forehand Speed Avg': round(fh.SPEED.dropna().mean(), 2) if len(fh) else np.nan,
            'Backhand Speed Avg (without slices)': round(bh_no_slice.SPEED.dropna().mean(), 2) if len(bh_no_slice) else np.nan,
            'Backhand Speed Avg (with slices)': round(bh_all.SPEED.dropna().mean(), 2) if len(bh_all) else np.nan,
        })
    return pd.DataFrame(rows)


def compute_scale_map(raw_rows, he_clean):
    """Which metric columns must be x100 to match the clean-leaderboard scale."""
    scale = {}
    for col in pipe.FUNCTIONS:
        if col not in raw_rows.columns or col not in he_clean.columns:
            continue
        cv_vals = pd.to_numeric(raw_rows[col], errors='coerce').abs().dropna()
        he_vals = pd.to_numeric(he_clean[col], errors='coerce').dropna()
        if not len(cv_vals) or not len(he_vals):
            continue
        he_med = he_vals.abs().median()
        if cv_vals.max() <= 1.001 and 2 <= he_med <= 100:
            scale[col] = 100
    return scale


def main():
    with open(HERE / 'cv_match_candidates.json') as f:
        candidates = json.load(f)

    all_raw = []           # (rows_df) raw-scale leaderboard rows
    match_meta = []        # metadata entries
    built_dirs = []

    for player_label, info in candidates.items():
        for m in info['picked']:
            if m.get('duplicate_of_previous'):
                continue
            tournament, year, name_a, name_b = parse_title(m['title'], m['date'])
            last_a, last_b = name_a.split()[-1], name_b.split()[-1]
            match_id = make_match_id(tournament, year, last_a, last_b)
            surface = surface_for(tournament)

            cvdf = pd.read_parquet(m['parquet'])
            cvdf['match_id'] = match_id
            # older CV versions carry None objects in numeric columns
            for col in ('ON_NET_Y', 'ON_NET_Z', 'CONTACT_Z', 'SPEED', 'SPEED_3D',
                        'bounce_x', 'bounce_y', 'hit_x', 'hit_y',
                        'player_location_x', 'player_location_y',
                        'receiver_location_x', 'receiver_location_y'):
                if col in cvdf.columns:
                    cvdf[col] = pd.to_numeric(cvdf[col], errors='coerce')
            df = pipe.cv_adapter.add_he_features(cvdf)
            df = pipe.joschka.resolve_serve_attempts(df)
            df['surface'] = surface
            sets = sorted(int(s) for s in df.set_no.unique())

            frame_players = list(df.PLAYER_HIT.dropna().unique())
            if len(frame_players) != 2:
                print(f'  SKIP {match_id}: players={frame_players}')
                continue
            for me in frame_players:
                opp = [p for p in frame_players if p != me][0]
                rows, _ = pipe.run_metrics(df, me, sets_list=['ALL'] + sets)
                # Calculations writes an aggregate row with match_id='ALL'
                # next to the per-match row; keep the per-match rows only
                rows = rows[rows.match_id != 'ALL'].copy()
                rows['player_name'] = str(me).upper()
                rows['opponent_name'] = str(opp).upper()
                rows['surface'] = surface
                rows['sets'] = rows['sets'].astype(str)
                all_raw.append(rows)

                pdir = APP / 'matches_new2' / f'{str(me).upper()}_{match_id}'
                pdir.mkdir(parents=True, exist_ok=True)
                mv = build_movement_json(df, me, opp, sets)
                with open(pdir / 'movement.json', 'w') as f:
                    json.dump(mv, f, indent=4)
                build_games_csv(df, me).to_csv(pdir / 'haddad_games.csv', index=False)
                built_dirs.append(str(pdir.name))

                entry = {'PLAYER': str(me).upper(), 'OPPONENT': str(opp).upper(),
                         'TOURNAMENT': tournament.upper(), 'YEAR': year, 'ROUND': 'CV',
                         'SURFACE': surface, 'FORMAT': 'CV', 'match_id': match_id,
                         'DATE': (datetime.strptime(m['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                                  if m.get('date') else f'{year}-01-01')}
                base = f"{entry['PLAYER']}_{match_id}_{HASH_SALT}"
                entry['hash_id'] = hashlib.sha256(base.encode()).hexdigest()[:16]
                match_meta.append(entry)
            print(f'  built {match_id} ({surface})')

    raw = pd.concat(all_raw, ignore_index=True).drop_duplicates(subset=['player_name', 'match_id', 'sets'])
    he_clean = pd.read_parquet(APP / 'leaderboard_haddad_new_wta_with_sets_clean.parquet')
    scale = compute_scale_map(raw, he_clean)
    with open(HERE / 'cv_scale_map.json', 'w') as f:
        json.dump(scale, f, indent=2, sort_keys=True)
    for col, factor in scale.items():
        raw[col] = pd.to_numeric(raw[col], errors='coerce') * factor
    # round like the HE clean pipeline does (the page shows values verbatim)
    for col in raw.columns:
        if raw[col].dtype.kind == 'f':
            raw[col] = raw[col].round(2)
    # keep only columns the app's leaderboard knows
    keep = [c for c in raw.columns if c in he_clean.columns]
    raw = raw[keep]
    raw.to_parquet(HERE / 'leaderboard_cv.parquet', index=False)
    print(f'\nleaderboard_cv.parquet: {raw.shape}, scaled columns: {len(scale)}')

    # merge metadata (idempotent by (PLAYER, match_id))
    meta_path = APP / 'post_match_metadata_with_hash.json'
    with open(meta_path) as f:
        meta = json.load(f)
    added = 0
    for e in match_meta:
        bucket = meta.setdefault(e['PLAYER'], [])
        if not any(x['match_id'] == e['match_id'] for x in bucket):
            bucket.append(e)
            added += 1
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=4)
    print(f'metadata entries added: {added} | dirs built: {len(built_dirs)}')


if __name__ == '__main__':
    main()
