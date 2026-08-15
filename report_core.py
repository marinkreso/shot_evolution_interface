"""Compute the stats for each report column from the local leaderboard parquet.

Each column is a dict: {'players': [...], 'matches': [...], 'name': '...'}.
When a column has several players, their matches are pooled and every stat is
computed as a weighted average over the pooled shots/rallies — i.e. the players
are treated as if they were a single player.
"""
from pathlib import Path

import pandas as pd

from card import funcs, get_data_for_matches, not_by_100

APP_DIR = Path(__file__).parent
LEADERBOARD_PATH = APP_DIR / 'leaderboard_haddad_new_wta_with_sets_clean.parquet'

_leaderboard = None


def load_leaderboard():
    """Prepare the shot-evolution view of the leaderboard once and cache it."""
    global _leaderboard
    if _leaderboard is None:
        # report_util_new owns the single on-disk read; reuse it instead of
        # loading the parquet a second time.
        from report_util_new import leaderboard3
        # Keep whole-match rows only; the per-set rows would double-count matches.
        leaderboard = leaderboard3[leaderboard3.sets == 'ALL'].copy()
        # This leaderboard stores percentages on a 0-100 scale; card.py expects
        # 0-1 fractions (it multiplies by 100 when formatting).
        pct_cols = [k for k in set(funcs) - set(not_by_100) if k in leaderboard.columns]
        leaderboard[pct_cols] = leaderboard[pct_cols] / 100
        # Stats missing from this leaderboard degrade to 'NO SHOTS/RALLIES'.
        for k in funcs:
            if k not in leaderboard.columns:
                leaderboard[k] = float('nan')
            if f'{k}_total' not in leaderboard.columns:
                leaderboard[f'{k}_total'] = 0
        _leaderboard = leaderboard
    return _leaderboard


def compute_columns(columns):
    leaderboard = load_leaderboard()
    datas = []
    for col in columns:
        players = col['players']
        # Pre-filter to the column's players: get_data_for_matches deep-copies its
        # input once per stat, so handing it the full leaderboard blows up memory.
        pool = leaderboard[(leaderboard.player_name.isin(players)) & (leaderboard.match_id != 'ALL')]
        match_ids = list(pool.match_id.unique())
        if col.get('matches'):
            match_ids = [m for m in match_ids if m in col['matches']]
        stats = get_data_for_matches(players, pool, match_ids)
        datas.append((stats, ' + '.join(players), col['name']))
    return datas
