"""Find recent CV-complete matches per player and convert them to parquets.

Usage: python fetch_cv_matches.py
Writes cv_matches/<PLAYER>/<match>.parquet and cv_match_candidates.json
"""
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).parent
OUT = HERE / 'cv_matches'
API = 'https://api.goldensetanalytics.com'
MIN_MEANINGFUL_POINTS = 50
WANTED = 20

PLAYERS = ['Julieta Pareja', 'Henry Bernet', 'Julia Stusek', 'Yeri Hong', 'Reda Bennani', 'Elizaveta Anikina']

def magnitude(x):
    if x:
        return (x['x']**2 + x['y']**2 + x['z']**2)**0.5*3.6
    else:
        return None

# %% cell 2
# CV PROCESSING
import json
import pandas as pd
import numpy as np
import requests
import os

point_number_dict = {
    '0': 0,
    '15': 1,
    '30': 2,
    '40': 3,
    'Ad': 4
}

def define_point_number(x, y):
    return point_number_dict[x] + point_number_dict[y] + 1

# %% cell 3
import numpy as np
try:
    from scipy.signal import savgol_filter
    _HAVE_SCIPY = True
except Exception:
    _HAVE_SCIPY = False

# ---- per-frame movement extraction (from cv_data['players_positions']) ------ #
MOVE_SMOOTH_WIN = 9          # Savitzky-Golay window (frames) for position/speed smoothing (tune me)
MOVE_MIN_FRAMES = 5          # need at least this many tracked frames in a run
MOVE_DT_DEFAULT = 0.04       # seconds/frame (25 fps); overridden from the data when possible


def _ts_seconds(ts):
    try:
        h, m, s = str(ts).split(":")
        return float(h) * 3600 + float(m) * 60 + float(s)
    except Exception:
        return None


def _estimate_dt(positions):
    """Seconds per frame from the players_positions timestamps (fallback 0.04)."""
    valid = [r for r in positions if r and r.get("time") and r["time"].get("frame") is not None]
    try:
        a, b = valid[0], valid[min(200, len(valid) - 1)]
        fa, fb = a["time"]["frame"], b["time"]["frame"]
        ta, tb = _ts_seconds(a["time"]["timestamp"]), _ts_seconds(b["time"]["timestamp"])
        if fb > fa and ta is not None and tb is not None and tb > ta:
            return (tb - ta) / (fb - fa)
    except Exception:
        pass
    return MOVE_DT_DEFAULT


def _sg(a, win, deriv, dt):
    """Smoothed derivative: Savitzky-Golay if available, else finite differences."""
    a = np.asarray(a, float)
    n = len(a)
    if not _HAVE_SCIPY or n < 5:
        if deriv == 0:
            return a
        g = np.gradient(a, dt)
        return g if deriv == 1 else np.gradient(g, dt)
    w = min(win, n)
    w = w if w % 2 == 1 else w - 1
    if w < 5:
        w = 5
    return savgol_filter(a, w, 2, deriv=deriv, delta=dt)


def _clean_series(vals):
    """List possibly containing None -> float array with interior gaps interpolated."""
    a = np.array([np.nan if v is None else v for v in vals], float)
    good = ~np.isnan(a)
    if good.sum() < 3:
        return None
    return np.interp(np.arange(len(a)), np.flatnonzero(good), a[good])


def _point_movement(point, positions, f2i, dt):
    """For each shot, the HITTER's movement while REACHING the ball: their
    per-frame position track over [previous shot's hit frame, this shot's hit
    frame] (opponent hit -> player reaches ball), smoothed then differentiated.
    Returns a list aligned to point['shots'] (None where not computable). Metric
    units: speed m/s, acceleration m/s^2 (deceleration = the min, i.e. negative)."""
    shots = point.get("shots", [])
    out = [None] * len(shots)
    if len(shots) < 2 or not positions:
        return out
    f0, f1 = shots[0]["time"]["frame"], shots[-1]["time"]["frame"]
    frames = [f for f in range(f0, f1 + 1) if f in f2i]
    if len(frames) < MOVE_MIN_FRAMES:
        return out
    rows = [positions[f2i[f]] for f in frames]
    fidx = {f: i for i, f in enumerate(frames)}
    # smoothed velocity of each tracked player over the whole point (better
    # derivative behaviour at window edges than smoothing each window alone)
    vel = {}
    for key in ("player1", "player2"):
        x = _clean_series([(r[key]["x"] if r.get(key) else None) for r in rows])
        y = _clean_series([(r[key]["y"] if r.get(key) else None) for r in rows])
        vel[key] = None if (x is None or y is None) else (
            _sg(x, MOVE_SMOOTH_WIN, 1, dt), _sg(y, MOVE_SMOOTH_WIN, 1, dt), x, y)
    for k in range(1, len(shots)):
        s, prev = shots[k], shots[k - 1]
        loc = s.get("player_location")
        fk, fk1 = s["time"]["frame"], prev["time"]["frame"]
        if loc is None or fk not in fidx or fk1 not in fidx:
            continue
        a, b = fidx[fk1], fidx[fk]
        if b - a < 3:
            continue
        rk = rows[b]

        def _d(key):
            return ((rk[key]["x"] - loc["x"]) ** 2 + (rk[key]["y"] - loc["y"]) ** 2) if rk.get(key) else 1e18

        key = "player1" if _d("player1") < _d("player2") else "player2"   # which track is the hitter
        if vel[key] is None:
            continue
        vx, vy, px, py = vel[key]
        sx, sy = vx[a:b + 1], vy[a:b + 1]
        speed = np.hypot(sx, sy)
        lon = np.abs(sx)                       # longitudinal (x) speed magnitude
        lat = np.abs(sy)                       # lateral (y) speed magnitude
        f_acc = _sg(speed, MOVE_SMOOTH_WIN, 1, dt)   # d(speed)/dt: >0 accel, <0 decel
        l_acc = _sg(lon, MOVE_SMOOTH_WIN, 1, dt)
        t_acc = _sg(lat, MOVE_SMOOTH_WIN, 1, dt)
        T = (b - a) * dt
        se = float(np.hypot(px[b] - px[a], py[b] - py[a]) / T) if T > 0 else None
        out[k] = {
            "move_n": int(b - a + 1),
            "move_spd_avg": float(speed.mean()), "move_spd_max": float(speed.max()),
            "move_spd_min": float(speed.min()), "move_spd_se": se,
            "move_acc_max": float(f_acc.max()), "move_dec_max": float(f_acc.min()),
            "move_lon_avg": float(lon.mean()), "move_lon_max": float(lon.max()), "move_lon_min": float(lon.min()),
            "move_lon_acc_max": float(l_acc.max()), "move_lon_dec_max": float(l_acc.min()),
            "move_lat_avg": float(lat.mean()), "move_lat_max": float(lat.max()), "move_lat_min": float(lat.min()),
            "move_lat_acc_max": float(t_acc.max()), "move_lat_dec_max": float(t_acc.min()),
        }
    return out


def cv_json_to_df(cv_data):
    if int(cv_data['version']['major']) < 4:
        print('Version must be higher >= 4')
        raise Exception
    #with open('cv_data_EX.json', 'w') as f:
    #    json.dump(cv_data, f, indent=4)
    camera_info = cv_data['camera_info']
    metadata = cv_data['metadata']
    data = []
    version_cv = cv_data['version']['major'] + '.' + cv_data['version']['minor'] + '.' + cv_data['version']['patch']
    # per-frame player positions for movement (accel/decel/min-max, lon/lat)
    _positions = cv_data.get('players_positions') or []
    _f2i = {r['time']['frame']: i for i, r in enumerate(_positions)
            if r and r.get('time') and r['time'].get('frame') is not None}
    _dt = _estimate_dt(_positions) if _f2i else MOVE_DT_DEFAULT
    print('DATA', len(cv_data['points']))

    for i, point in enumerate(cv_data['points']):

        shot_number = 1
        movement = _point_movement(point, _positions, _f2i, _dt)
        first_serve_time = point['first_serve_time']
        second_serve_time = point['second_serve_time']
        set_number = int(point['score']['p1_set']) + int(point['score']['p2_set']) + 1
        game_number = int(point['score']['p1_game']) + int(point['score']['p2_game']) + 1
        if game_number == 13:
            try:
                point_number = int(point['score']['p1_point']) + int(point['score']['p2_point']) + 1
            except:
                point_number = 0
        else:
            try:
                point_number = define_point_number(point['score']['p1_point'], point['score']['p2_point'])
            except:
                point_number = 0
                continue
        
        for _si, shot in enumerate(point['shots']):
            if shot['type'] == 'serve':
                shot_number = 1
            elif shot['type'] == 'return':
                shot_number = 2
            #elif shot['type'] == 'groundstroke' and shot_number < 3:
            #    shot_number = 3
            h, m, s = shot['time']['timestamp'].split(':')
            seconds = float(h)*3600 + float(m.lstrip(''))*60 + float(s)
            outcome = 'unknown'
            if 'outcome' in shot:
                outcome = shot['outcome']
            trajectory_3d_column = 'trajectory_3d'
            if 'trajectory_3d_beta' in shot:
                trajectory_3d_column = 'trajectory_3d_beta'
            zs = []
            if shot.get('toss_trajectory_3d') and shot['toss_trajectory_3d'].get('positions'):
                for position in shot['toss_trajectory_3d'].get('positions'):
                    zs.append(position.get('position').get('z'))
            if shot.get('bounce_location'):
                data.append({
                    'z_toss': zs,
                    'match_id': cv_data['match_id'],
                    'server': point['server'],
                    'point_winner': point['point_winner'],
                    'top_player': point['top_player'],
                    'start_time': point['start_time']['timestamp'],
                    'end_time': point['end_time']['timestamp'],
                    'Hit_frame':  shot['time']['frame'],
                    'Bounce_frame': shot.get('bounce_time', {})['frame'],
                    'Hit_time': shot['time']['timestamp'],
                    'Bounce_time': shot.get('bounce_time', {})['timestamp'],
                    'bounce_x': shot.get('bounce_location')['x'],
                    'bounce_y': shot.get('bounce_location')['y'],
                    'hit_x': shot.get('player_location')['x'] if shot.get('player_location') else None,
                    'hit_y': shot.get('player_location')['y'] if shot.get('player_location') else None,
                    'Player1_score_points': point['score']['p1_point'],
                    'Player2_score_points': point['score']['p2_point'],
                    'Player1_score_set': point['score']['p1_set'],
                    'Player2_score_set': point['score']['p2_set'],
                    'Player1_score_game': point['score']['p1_game'],
                    'Player2_score_game': point['score']['p2_game'],
                    'player_location_x': shot.get('player_location')['x'] if shot.get('player_location') else None,
                    'player_location_y': shot.get('player_location')['y'] if shot.get('player_location') else None,
                    'receiver_location_x': shot.get('receiving_player_location')['x'] if shot.get('receiving_player_location') else None,
                    'receiver_location_y': shot.get('receiving_player_location')['y'] if shot.get('receiving_player_location') else None,
                    'set': set_number,
                    'game': game_number,
                    'point': point_number,
                    'shot': shot_number,
                    'events.shot': shot['type'],
                    'placement_gsa': shot['placement_gsa'],
                    'stroke': shot['stroke'],
                    'serve_type': shot.get('serve_subtype'),
                    'outcome': outcome,
                    'SPEED': shot['speed'],
                    'SPEED_3D': shot['speed'] if not shot.get(trajectory_3d_column) or 'speed' not in shot[trajectory_3d_column] else magnitude(shot[trajectory_3d_column]['speed']),
                    'player_jump_height': shot.get('player_jump_height', 0) / 10.0,
                    'CONTACT_Z': shot[trajectory_3d_column]['positions'][0]['position']['z'] if trajectory_3d_column in shot and shot[trajectory_3d_column] and shot[trajectory_3d_column]['positions']  else shot['hit_location'].get('z', None) if shot.get('hit_location') else None,
                    'ON_NET_Z': shot[trajectory_3d_column]['crossing_location'].get('z') if trajectory_3d_column in shot and  shot[trajectory_3d_column] and 'crossing_location' in shot[trajectory_3d_column] and shot[trajectory_3d_column]['crossing_location'] else shot['crossing_location']['z'] if shot.get('crossing_location') else None,
                    'ON_NET_Y': shot[trajectory_3d_column]['crossing_location'].get('y') if trajectory_3d_column in shot and  shot[trajectory_3d_column] and 'crossing_location' in shot[trajectory_3d_column] and shot[trajectory_3d_column]['crossing_location'] else shot['crossing_location']['y'] if shot.get('crossing_location') else None,
                    'version_cv': version_cv,
                    'camera_info': camera_info,
                    'cv_metadata': metadata,
                    'first_serve_time': first_serve_time,
                    'second_serve_time': second_serve_time,
                })
            else:
                data.append({
                    'z_toss': zs,
                    'match_id': cv_data['match_id'],
                    'server': point['server'],
                    'point_winner': point['point_winner'],
                    'top_player': point['top_player'],
                    'distance_bottom_player': point.get('distance_bottom_player'),
                    'distance_top_player': point.get('distance_top_player'),
                    'start_time': point['start_time']['timestamp'],
                    'end_time': point['end_time']['timestamp'],
                    'Hit_frame':  shot['time']['frame'],
                    'Bounce_frame': None,
                    'Hit_time': shot['time']['timestamp'],
                    'Bounce_time': None,
                    'bounce_x': None,
                    'bounce_y': None,
                    'hit_x': shot.get('player_location')['x'] if shot.get('player_location') else None,
                    'hit_y': shot.get('player_location')['y'] if shot.get('player_location') else None,
                    'Player1_score_points': point['score']['p1_point'],
                    'Player2_score_points': point['score']['p2_point'],
                    'Player1_score_set': point['score']['p1_set'],
                    'Player2_score_set': point['score']['p2_set'],
                    'Player1_score_game': point['score']['p1_game'],
                    'Player2_score_game': point['score']['p2_game'],
                    'player_location_x': shot.get('player_location')['x'] if shot.get('player_location') else None,
                    'player_location_y': shot.get('player_location')['y'] if shot.get('player_location') else None,
                    'receiver_location_x': shot.get('receiving_player_location')['x'] if shot.get('receiving_player_location') else None,
                    'receiver_location_y': shot.get('receiving_player_location')['y'] if shot.get('receiving_player_location') else None,
                    'set': set_number,
                    'game': game_number,
                    'point': point_number,
                    'shot': shot_number,
                    'events.shot': shot['type'],
                    'placement_gsa': shot['placement_gsa'],
                    'stroke': shot['stroke'],
                    'serve_type': shot.get('serve_subtype'),
                    'outcome': outcome,
                    'SPEED': shot['speed'],
                    'SPEED_3D': shot['speed'] if not shot.get(trajectory_3d_column) or 'speed' not in shot[trajectory_3d_column] else magnitude(shot[trajectory_3d_column]['speed']),
                    'player_jump_height': shot.get('player_jump_height', 0) / 10.0,
                    'CONTACT_Z': shot[trajectory_3d_column]['positions'][0]['position']['z'] if trajectory_3d_column in shot and shot[trajectory_3d_column] and shot[trajectory_3d_column]['positions']  else shot['hit_location'].get('z', None) if shot.get('hit_location') else None,
                    'ON_NET_Z': shot[trajectory_3d_column]['crossing_location'].get('z') if trajectory_3d_column in shot and  shot[trajectory_3d_column] and 'crossing_location' in shot[trajectory_3d_column] and shot[trajectory_3d_column]['crossing_location'] else shot['crossing_location']['z'] if shot.get('crossing_location') else None,
                    'ON_NET_Y': shot[trajectory_3d_column]['crossing_location'].get('y') if trajectory_3d_column in shot and  shot[trajectory_3d_column] and 'crossing_location' in shot[trajectory_3d_column] and shot[trajectory_3d_column]['crossing_location'] else shot['crossing_location']['y'] if shot.get('crossing_location') else None,
                    'version_cv': version_cv,
                    'camera_info': camera_info,
                    'cv_metadata': metadata,
                    'first_serve_time': first_serve_time,
                    'second_serve_time': second_serve_time,
                })
            if _si < len(movement) and movement[_si]:
                data[-1].update(movement[_si])
            shot_number = shot_number + 1
            
    
    cvdf = pd.DataFrame(data)
    print('DATA', len(data))
    player1 = cv_data['metadata']['player1']
    player2 = cv_data['metadata']['player2']
    cvdf['returner'] = np.where(cvdf.server == player1, player2, player1)
    cvdf['bottom_player'] = np.where(cvdf.top_player == player1, player2, player1)
    cvdf['impact_player'] = np.where(cvdf.shot % 2 == 1, cvdf['server'], cvdf['returner'])
    cvdf['opponent'] = np.where(cvdf.impact_player == player1, player2, player1)
    cvdf['serve_shot'] = np.where(cvdf.shot == 1, 1, 0)
    cvdf['serve'] = cvdf.groupby(['start_time', 'Player1_score_points', 'Player2_score_points',
           'Player1_score_set', 'Player2_score_set', 'Player1_score_game',
           'Player2_score_game'])['serve_shot'].cumsum()
    cvdf['rally'] = cvdf.groupby(['start_time', 'Player1_score_points', 'Player2_score_points',
           'Player1_score_set', 'Player2_score_set', 'Player1_score_game',
           'Player2_score_game'])['serve_shot'].cumsum()
    cvdf.loc[(cvdf.serve >= 3), 'serve'] = 2

    cvdf['point_rank'] = cvdf.groupby(['set', 'game', 'point'])['start_time'].rank(method='dense')
    cvdf['point_new'] = cvdf['point'] + 2*(cvdf['point_rank']-1)
    cvdf['point'] = (cvdf['point'] + 2*(cvdf['point_rank']-1)).astype(int)
    cvdf['Bounce_frame'] = cvdf['Bounce_frame'].astype('Int64')
    cvdf[(cvdf.point != cvdf.point_new)][['set', 'game', 'point', 'point_new']].drop_duplicates()
    cvdf['placement_gsa_previous'] = cvdf.groupby(['set', 'game', 'point'])['placement_gsa'].shift(1)
    cvdf['serve_previous'] = cvdf.groupby(['set', 'game', 'point'])['serve'].shift(1)
    cvdf['events.shot_previous'] = cvdf.groupby(['set', 'game', 'point'])['events.shot'].shift(1)
    cvdf.loc[(cvdf.serve_previous == 1) & (cvdf.placement_gsa_previous != 'Out') & (cvdf.serve == 2) & (cvdf['events.shot_previous'] == 'serve') & (cvdf['events.shot'] == 'serve'), 'serve'] = 1
    cvdf[['impact_player', 'bounce_x', 'bounce_y', 'start_time', 'end_time', 'Hit_frame', 'Bounce_frame', 'Hit_time', 'Bounce_time', 'Player1_score_points', 'Player2_score_points',
       'Player1_score_set', 'Player2_score_set', 'Player1_score_game',
       'Player2_score_game', 'opponent', 'events.shot', 'shot', 'set', 'game', 'point', 'serve', 'rally']]
    cvdf['serve_number'] = cvdf.groupby(['set', 'game', 'point']).serve.transform(max)
    cvdf['rally_length'] = cvdf.groupby(['set', 'game', 'point', 'serve']).shot.transform(max)
    cvdf['last_shot'] = cvdf.groupby(['set', 'game', 'point', 'serve']).Hit_time.transform('last')
    df = cvdf
    df['player_location_y_mirrored'] = np.where(df['player_location_x'] > 0, df['player_location_y']*-1, df['player_location_y']) #dft['CONTACT_Y_mirrored'] = np.where(dft['CONTACT_X'] > 0, dft['CONTACT_Y']*-1, dft['CONTACT_Y'])
    df['video_id'] = df['match_id']
    
    alldeucead = ['1500', '1515', '3015', '4015', '4030', '0000', '0015', '0030',
       '1530', '3030', '3000', '4040', '40Ad', 'Ad40', '1540', '3040',
       '4000', '0040']
    deuce = ['1515', '4015',  '0000',  '0030',
            '3030', '3000', '4040', '1540', 
           ]
    ad = [x for x in alldeucead if x not in deuce]
    deuce_pressure_break = ['3030', '4040', '4015']
    ad_pressure_break = ['4000', '4030', 'Ad40', '40A', 'AD40', '3015']
    ad_pressure_break_reversed = ['0040', '3040', '40Ad', '1530']
    deuce_pressure_break_reversed = ['3030', '4040', '1540']
    df['gamescore'] = df['Player1_score_points'].astype(str).apply(lambda x: '00' if x == '0' else x) + df['Player2_score_points'].astype(str).apply(lambda x: '00' if x == '0' else x)
    df['deuce_or_ad'] = np.where(df.gamescore.isin(deuce), 'deuce', 'ad')
    df['placement_gsa_original'] = df['placement_gsa']

    def replace_to_zone(x):
        if x == 'A':
            return 'D'
        elif x == 'B':
            return 'C'
        elif x == 'C':
            return 'B'
        elif x == 'D':
            return 'A'
        else:
            return x
    df['placement_gsa'] = df['placement_gsa'].apply(lambda x:  x.split('-')[0] + '-' + replace_to_zone(x.split('-')[1]) if x and len(x.split('-')) == 2 else x)

    return df



def get_token():
    r = requests.post(API + '/login/token', headers={'Content-Type': 'application/json'},
                      data=json.dumps({"userName": "sw", "password": "K4!Yf*%NY)Kv6@y*"}), timeout=30)
    r.raise_for_status()
    return r.text


def meaningful_points(df):
    """Points that actually carry data: at least one shot with a bounce or placement."""
    ok = df[(df.bounce_x.notna()) | (df.placement_gsa.notna())]
    return ok.groupby(['set', 'game', 'point']).ngroups


def main():
    OUT.mkdir(exist_ok=True)
    results = {}
    for player in PLAYERS:
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'}
        last = player.split()[-1]
        r = requests.get(API + f'/videos/search?searchText={last}', headers=headers, timeout=60)
        vids = r.json() if r.status_code == 200 else []
        name_tokens = [t.lower() for t in player.split()]
        cands = [v for v in vids
                 if all(t in v['title'].lower() for t in name_tokens)
                 and 'cv completed' in v['title'].lower()]
        def dt(v):
            try:
                return datetime.strptime(v['matchDate'], '%m/%d/%Y')
            except Exception:
                return datetime(1970, 1, 1)
        cands.sort(key=dt, reverse=True)
        # dedupe by "X vs Y - Tournament"
        seen, ordered = set(), []
        for v in cands:
            key = ' - '.join(v['title'].split(' - ')[:2])
            if key not in seen:
                seen.add(key)
                ordered.append(v)
        print(f'== {player}: {len(vids)} search hits, {len(ordered)} CV-completed candidates', flush=True)
        picked, tried = [], []
        pdir = OUT / player.replace(' ', '_').upper()
        pdir.mkdir(exist_ok=True)
        for v in ordered:
            if len(picked) >= WANTED:
                break
            title_key = ' - '.join(v['title'].split(' - ')[:2])
            safe = re.sub(r'[^A-Za-z0-9_-]+', '_', title_key)[:120]
            cached = pdir / f'{safe}.parquet'
            if cached.exists():
                df = pd.read_parquet(cached)
                pts = meaningful_points(df)
                picked.append({'player': player, 'title': v['title'], 'date': v['matchDate'],
                               'video_id': v['id'], 'meaningful_points': int(pts), 'shots': int(len(df)),
                               'parquet': str(cached), 'cached': True})
                print(f'  CACHED {v["matchDate"]}  {title_key}  ({pts} pts)', flush=True)
                continue
            try:
                t0 = time.time()
                resp = requests.get(API + f"/cv/download/{v['id']}", headers=headers, timeout=600)
                if resp.status_code != 200:
                    raise RuntimeError(f'http {resp.status_code}')
                cv = resp.json()
                cv['match_id'] = v['id']
                df = cv_json_to_df(cv)
                pts = meaningful_points(df)
                entry = {'player': player, 'title': v['title'], 'date': v['matchDate'],
                         'video_id': v['id'], 'meaningful_points': int(pts), 'shots': int(len(df)),
                         'cv_version': str(df.version_cv.iloc[0]) if len(df) else None,
                         'secs': round(time.time() - t0, 1)}
                if pts >= MIN_MEANINGFUL_POINTS:
                    df.to_parquet(pdir / f'{safe}.parquet')
                    entry['parquet'] = str(pdir / f'{safe}.parquet')
                    picked.append(entry)
                    print(f'  OK  {v["matchDate"]}  {title_key}  ({pts} pts, {len(df)} shots)', flush=True)
                else:
                    entry['rejected'] = 'too few points'
                    print(f'  THIN {v["matchDate"]}  {title_key}  ({pts} pts)', flush=True)
                tried.append(entry)
            except Exception as e:
                tried.append({'player': player, 'title': v['title'], 'video_id': v['id'], 'error': str(e)[:200]})
                print(f'  FAIL {v["matchDate"]}  {title_key}  ({str(e)[:80]})', flush=True)
        results[player] = {'picked': picked, 'tried': tried}
        with open(HERE / 'cv_match_candidates.json', 'w') as f:
            json.dump(results, f, indent=2)
    print('DONE', flush=True)
    for p, r in results.items():
        print(p, '->', len(r['picked']), 'matches', flush=True)


if __name__ == '__main__':
    main()
