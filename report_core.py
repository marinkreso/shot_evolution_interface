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
LEADERBOARD_PATH = APP_DIR / 'leaderboard_haddad_new.parquet'

_leaderboard = None


def load_leaderboard():
    """Load the leaderboard once and keep it cached (memory is tight on Render)."""
    global _leaderboard
    if _leaderboard is None:
        leaderboard = pd.read_parquet(LEADERBOARD_PATH)
        # A handful of rows store percentage stats on a 0-100 scale instead of 0-1;
        # bring them back to fractions so the weighted averages stay correct.
        for k in set(funcs) - set(not_by_100):
            if k in leaderboard.columns:
                mis_scaled = leaderboard[k] > 1.5
                leaderboard.loc[mis_scaled, k] = leaderboard.loc[mis_scaled, k] / 100
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
