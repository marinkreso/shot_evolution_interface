"""Seed best_matches.json: per player, their wins against top opponents.

Approximation: a match counts as a best win when the opponent is in the
TOP_OPPONENTS list for the tour and the player won more SETS than the
opponent, where a set's winner is the player with more total points in it
(own serve points won + opponent's serve points lost, per set). Points-per-set
tracks the real set winner far better than whole-match points, which tiebreak
matches routinely invert.

The output file best_matches.json is meant to be EDITED BY HAND afterwards —
add or remove match ids freely; the app only reads the file. Re-running this
script overwrites manual edits, so keep a copy if you re-seed.
"""
import json
from pathlib import Path

import pandas as pd

APP_DIR = Path(__file__).parent

# EDIT HERE: opponents that make a win a "best win", per tour
TOP_OPPONENTS = {
    'ATP': ['SINNER', 'ALCARAZ', 'ZVEREV', 'DJOKOVIC', 'FRITZ', 'SHELTON',
            'RUUD', 'MEDVEDEV', 'DE MINAUR', 'RUNE', 'DRAPER', 'MUSETTI', 'PAUL'],
    'WTA': ['SABALENKA', 'SWIATEK', 'GAUFF', 'PEGULA', 'ZHENG', 'KEYS',
            'RYBAKINA', 'NAVARRO', 'PAOLINI', 'ANDREEVA'],
}

with open(APP_DIR / 'wta_players.json') as f:
    WTA_PLAYERS = set(json.load(f))


def main():
    lb = pd.read_parquet(APP_DIR / 'leaderboard_haddad_new_wta_with_sets_clean.parquet')
    lb = lb[lb.sets != 'ALL']
    serve_pts = {}
    for row in lb.itertuples():
        pct, total = row.percent_serve_points_won, row.percent_serve_points_won_total
        if pd.notna(pct) and pd.notna(total) and total > 0:
            serve_pts[(row.player_name, row.match_id, row.sets)] = (pct / 100 * total, total)

    match_sets = {}
    for player, match_id, set_no in serve_pts:
        match_sets.setdefault(match_id, set()).add(set_no)

    def won_match(player, opponent, match_id):
        p_sets = o_sets = 0
        for set_no in match_sets.get(match_id, ()):
            mine = serve_pts.get((player, match_id, set_no))
            theirs = serve_pts.get((opponent, match_id, set_no))
            if not mine or not theirs:
                continue
            my_points = mine[0] + (theirs[1] - theirs[0])
            their_points = theirs[0] + (mine[1] - mine[0])
            if my_points > their_points:
                p_sets += 1
            elif their_points > my_points:
                o_sets += 1
        if p_sets == o_sets:
            return None  # cannot judge
        return p_sets > o_sets

    with open(APP_DIR / 'all_data2.json') as f:
        all_matches = json.load(f)
    with open(APP_DIR / 'post_match_metadata_with_hash.json') as f:
        report_players = set(json.load(f).keys())

    best = {}
    undecided = 0
    for m in all_matches:
        player, opponent = m['PLAYER'], m['OPPONENT']
        if player.replace('-', ' ') not in report_players and player not in report_players:
            continue
        tour = 'WTA' if player in WTA_PLAYERS else 'ATP'
        if opponent not in TOP_OPPONENTS[tour]:
            continue
        result = won_match(player, opponent, m['match_id'])
        if result is None:
            undecided += 1
            continue
        if result:
            best.setdefault(player, []).append(m['match_id'])

    best = {p: sorted(set(ids)) for p, ids in sorted(best.items())}
    with open(APP_DIR / 'best_matches.json', 'w') as f:
        json.dump(best, f, indent=2)
    print(f'players with best wins: {len(best)} | undecided (missing points data): {undecided}')
    for p in ('LEHECKA', 'TSITSIPAS'):
        print(p, '->', best.get(p, []))


if __name__ == '__main__':
    main()
