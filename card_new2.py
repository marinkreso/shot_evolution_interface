"""Row lookup for the post-match report (per-set leaderboard rows).

Trimmed to the single function the app uses; the original file carried ~640
lines of dead code including a stat registry that had diverged from card.py's.
"""


def get_data_for_matches_new2(selected_player_name, leaderboard_clean, match_ids=[]):
    l1 = leaderboard_clean[(leaderboard_clean.match_id.isin(match_ids)) & (leaderboard_clean.player_name.isin(selected_player_name))]
    return l1.set_index('sets').to_dict('index')
