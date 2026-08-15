import argparse
import os
import numpy as np
import pandas as pd
# (utils star-import removed - only numpy/pandas are used)

def robust_round(x, factor=0):
    if not x or np.isnan(x):
        return 0
    else:
        return int(round(x, factor))

funcs = [
    'rally_long', 
    'serve_plus_win',
    'serve_quality_second_deuce_wide',
'serve_quality_second_deuce_t',
'serve_quality_second_ad_wide',
'serve_quality_second_ad_t',
'first_return_in_percentage_pressure',
'first_return_in_percentage_break',
'first_return_win_percentage_pressure',
'first_return_win_percentage_break',
            'win_percent_first_serve', 'win_percent_first_serve_pressure',
            'win_percent_first_serve_break', 'percent_of_first_serves_within_04m_of_sideline',
            'percent_of_first_serves_within_04m_of_sideline_pressure', 'percent_of_first_serves_within_04m_of_sideline_break',
            'first_serve_speed', 'first_serve_speed_before_bounce', 'first_serve_speed_after_bounce',
            'first_serve_speed_deuce_w', 'first_serve_speed_deuce_t', 'first_serve_speed_ad_w', 'first_serve_speed_ad_t',
            'first_serve_speed_decrease_break', 'first_serve_speed_decrease_break_deuce', 'first_serve_speed_decrease_break_ad',
            'avg_return_speed_opponent', 'percent_unreturned_first_serves',
            'percent_first_serves_won_in_two_to_four_shots', 'first_serve_in_percentage',
            'first_serve_in_percentage_pressure', 'first_serve_in_percentage_break',
            'first_serve_win_percentage_bh_deuce', 'first_serve_win_percentage_fh_deuce',
            'first_serve_win_percentage_bh_ad', 'first_serve_win_percentage_fh_ad',
            'win_percent_first_serve_rally_five_to_eight', 'win_percent_first_serve_rally_nine_plus',
            'percent_serve_points_won', 'percent_aces_per_serve_points',
            'avg_points_won_per_serve_game', 'avg_points_lost_per_serve_game',
            'serve_hold_rate', 'serve_win_percentage_when_return_in', 'serve_win_percentage_when_return_fast',
            'serve_win_percentage_when_return_deep', 'serve_win_percentage_when_return_middle',
            'serve_win_percentage_when_return_short', 
            'percent_serve_pone_deuce_after_deuce_returned_middle', 'percent_serve_pone_ad_after_ad_returned_middle',
            'percent_serve_pone_runaround_fh', 'percent_serve_pone_runaround_inside_in_fh',
            'win_percent_ad_serve_pone_runaround_inside_in_fh', 'win_percent_deuce_serve_pone_runaround_inside_in_fh',
            'percent_returns_line_and_cross', 'win_percent_first_return_higher_over_net',
            'win_percent_first_return_lower_over_net', 'percent_first_serve_slice_deuce_w',
            'percent_first_serve_slice_ad_t', 'second_serve_win_percentage_pone_bh_deuce',
            'second_serve_win_percentage_pone_fh_deuce', 'second_serve_win_percentage_pone_bh_ad',
            'second_serve_win_percentage_pone_fh_ad', 'win_percent_second_serve_rally_under_five',
            'second_serve_ad_wide_percent_dtl_return', 'second_serve_win_percentage_bh_deuce',
            'second_serve_win_percentage_fh_deuce', 'second_serve_win_percentage_bh_ad',
            'second_serve_win_percentage_fh_ad', 'second_serve_speed_deuce_w',
            'second_serve_speed_deuce_t', 'second_serve_speed_ad_w', 'second_serve_speed_ad_t', 'first_return_depth',
                'first_return_percent_deep', 'first_return_percent_short','first_return_win_percent_deep', 'first_return_percent_low',
                'first_return_win_percent_low', 'first_return_percent_to_bh', 'first_return_win_percent_to_bh',
            'first_return_percent_line', 'first_return_win_percent_line', 'first_return_win_under_five',
            'first_return_win_over_five', 'first_return_speed', 'first_return_win_percentage', 'second_return_depth',
            'second_return_percent_deep', 'second_return_win_percent_deep', 'second_return_percent_low',
            'second_return_win_percent_low', 'second_return_percent_to_bh', 'second_return_win_percent_to_bh',
            'second_return_percent_line', 'second_return_win_percent_line', 'second_return_win_under_five',
            'second_return_win_over_five', 'second_return_speed', 'second_return_win_percentage',
            'avg_forehand_dtl_speed',
            'avg_forehand_cc_speed',
            'avg_backhand_cc_speed',
            'avg_backhand_dtl_speed',
            'avg_forehand_cc_depth',
            'avg_forehand_dtl_depth',
            'avg_backhand_cc_depth',
            'avg_backhand_dtl_depth',
            'avg_backhand_spin',
            'avg_forehand_spin',
            'passing_bh_win_perc',

'passing_fh_win_perc',

'approach_win_perc',

'approach_fh_win_perc',

'approach_bh_win_perc',

'approach_to_fh_win_perc',

'approach_to_bh_win_perc',
'first_return_defeat_under_five',
'fh_consistency',
'bh_consistency',
'fh_consistency_winners',
'bh_consistency_winners',
'initiative_first_over_nine',
'initiative_over_nine',
'initiative_second',
'initiative_second_return',
'break_point_faced_win',
'break_point_opportunity_win',
'serve_speed_reduction_pressure',
'return_speed_reduction_break',
'serve_quality_deuce_wide',
'serve_quality_deuce_t',
'serve_quality_ad_wide',
'serve_quality_ad_t',
'first_return_extended_or_won',
'bh_middle_consistency',
'bh_ad_consistency',
'bh_deuce_consistency',
'fh_middle_consistency',
'fh_deuce_consistency',
'fh_ad_consistency',
'second_return_extended_or_won',
'second_return_aggressive',
'first_return_fh_speed',
'first_return_bh_speed',
'first_return_deuce_speed',
'first_return_ad_speed',
'first_return_deuce_fh_speed',
'first_return_deuce_bh_speed',
'first_return_ad_fh_speed',
'first_return_ad_bh_speed',
'second_return_fh_speed',
'second_return_bh_speed',
'second_return_deuce_speed',
'second_return_ad_speed',
'second_return_deuce_fh_speed',
'second_return_deuce_bh_speed',
'second_return_ad_fh_speed',
'second_return_ad_bh_speed',
'first_return_in_percentage',
'second_return_in_percentage',
'average_rally_length_serving_1st',
'average_rally_length_serving_2nd',
'rally_winners_per_match',
'rally_ue_per_match',
'topspin_slice',
'fh_cc_dtl_ratio',
'bh_cc_dtl_ratio',
'bh_cc_speed',
'bh_dtl_speed',
'fh_dtl_speed',
'fh_cc_speed',
'bh_cc_depth',
'bh_dtl_depth',
'fh_dtl_depth',
'fh_cc_depth',
'bh_cc_spin',
'bh_dtl_spin',
'fh_dtl_spin',
'fh_cc_spin',
'bh_cc_speed_winners',
'bh_dtl_speed_winners',
'fh_dtl_speed_winners',
'fh_cc_speed_winners',
'bh_cc_depth_winners',
'bh_dtl_depth_winners',
'fh_dtl_depth_winners',
'fh_cc_depth_winners',
'bh_cc_spin_winners',
'bh_dtl_spin_winners',
'fh_dtl_spin_winners',
'fh_cc_spin_winners',
'approach_win_percentage',
'approaches_to_FH',
'approaches_to_BH',
'approach_percentage',
'rally_play_long_rallies_won',
'rally_play_1st_serve_won_in_5_shots_or_less',
'rally_play_1st_serve_finished_in_5_shots_or_less',
'rally_play_2nd_return_won_in_5_or_less',
'bh_dtl_all_rally_shots',
'bh_dtl_well_placed',
'bh_dtl_fast',
'fh_all_rally_shots',
'run_around_fh_percentage',
'run_around_fh_winners_fe',
'win_in_rallies_with_run_around_forehand',
'fast_attacking_deuce_fh_cross_percentage',
'fast_attacking_deuce_fh_cross_won',
'fast_attacking_deuce_fh_line_percentage',
'fast_attacking_deuce_fh_line_won',
'opponent_moved_on_neutral_ball',
'dropshots_in_rallies',
'dropshots_fh_win',
'dropshots_bh_win',
'on_the_run_fh_percent',
'on_the_run_bh_percent',
'on_the_run_fh_won',
'on_the_run_bh_won',
'on_the_run_bh_slice',
'on_the_run_bh_slice_won',
'on_the_run_bh_slice_won_on_fast',
'bh_cross_finish_win',
'fh_cross_finish_win',
'bh_cross_change_dtl_win',
'fh_cross_change_dtl_win',
'bh_cross_change_to_fh',
'fh_cross_change_to_bh',
'fast_ball_received_to_bh_percent',
'fast_ball_outgoing_balls_to_opponent_bh',
'strong_serve_plus1',
'weak_serve_plus1',
'offensive_serve_plus1',
'defensive_serve_plus1',
'win_percent_second_serve',
'win_percent_second_serve_ad_wide',
'second_serve_weak_returns',
'second_serve_attacked',
'first_return_percent_high',
'first_return_percent_fast',
'first_return_percent_angled',
'first_bh_return_in_percentage',
'first_fh_return_in_percentage',
'second_bh_return_speed',
'second_fh_return_speed',
'second_fh_return_in_percentage',
'second_bh_return_in_percentage',
'rally_winners_and_forcing_error_per_match', # WINNERS & ERRORS
'bh_consistency_new',
'fh_consistency_new',
'fh_errors',
'bh_errors',
'shots_hit_further_back', # LOCATION
'shots_hit_behind_bl',
'shots_hit_inside',
'fh_winners_easy_ball',
'bh_winners_easy_ball',
'fh_errors_easy_ball',
'bh_errors_easy_ball',
'bh_cross_change_dtl_count',
'fh_cross_change_dtl_count',
'on_the_run_fh_count',
'on_the_run_bh_count',
'dropshots_win',
'dropshots_count',
'bh_slice_deep_count',
'bh_slice_deep_win',
'bh_slice_short_low_win',
'bh_slice_short_low_count',
'approach_win_perc_count',
"movement_to_fh_avg_speed",
    "movement_to_fh_avg_acc",
    "movement_to_fh_avg_decc",
    "movement_to_bh_avg_speed",
    "movement_to_bh_avg_acc",
    "movement_to_bh_avg_decc",
    "movement_first_serve_speed",
    "movement_first_serve_acc",
    "movement_first_serve_decc",
    "movement_second_serve_speed",
    "movement_second_serve_acc",
    "movement_second_serve_decc",
    "movement_to_fh_direction_right_avg_speed",
    "movement_to_fh_direction_right_avg_acc",
    "movement_to_fh_direction_right_avg_decc",
    "movement_to_fh_direction_forward_avg_speed",
    "movement_to_fh_direction_forward_avg_acc",
    "movement_to_fh_direction_forward_avg_decc",
    "movement_to_fh_direction_backward_avg_speed",
    "movement_to_fh_direction_backward_avg_acc",
    "movement_to_fh_direction_backward_avg_decc",
    "movement_to_bh_direction_forward_avg_speed",
    "movement_to_bh_direction_forward_avg_acc",
    "movement_to_bh_direction_forward_avg_decc",
    "movement_to_bh_direction_backward_avg_speed",
    "movement_to_bh_direction_backward_avg_acc",
    "movement_to_bh_direction_backward_avg_decc",
    "movement_to_bh_direction_right_avg_speed",
    "movement_to_bh_direction_right_avg_acc",
    "movement_to_bh_direction_right_avg_decc" 
        ]
    
gs_stats = [
"movement_to_fh_avg_speed",
    "movement_to_fh_avg_acc",
    "movement_to_fh_avg_decc",
    "movement_to_bh_avg_speed",
    "movement_to_bh_avg_acc",
    "movement_to_bh_avg_decc",
    "movement_first_serve_speed",
    "movement_first_serve_acc",
    "movement_first_serve_decc",
    "movement_second_serve_speed",
    "movement_second_serve_acc",
    "movement_second_serve_decc",
    "movement_to_fh_direction_right_avg_speed",
    "movement_to_fh_direction_right_avg_acc",
    "movement_to_fh_direction_right_avg_decc",
    "movement_to_fh_direction_forward_avg_speed",
    "movement_to_fh_direction_forward_avg_acc",
    "movement_to_fh_direction_forward_avg_decc",
    "movement_to_fh_direction_backward_avg_speed",
    "movement_to_fh_direction_backward_avg_acc",
    "movement_to_fh_direction_backward_avg_decc",
    "movement_to_bh_direction_forward_avg_speed",
    "movement_to_bh_direction_forward_avg_acc",
    "movement_to_bh_direction_forward_avg_decc",
    "movement_to_bh_direction_backward_avg_speed",
    "movement_to_bh_direction_backward_avg_acc",
    "movement_to_bh_direction_backward_avg_decc",
    "movement_to_bh_direction_right_avg_speed",
    "movement_to_bh_direction_right_avg_acc",
    "movement_to_bh_direction_right_avg_decc",
'shots_hit_further_back', # LOCATION
'shots_hit_behind_bl',
'shots_hit_inside',
'on_the_run_fh_won',
    'on_the_run_bh_won',
'dropshots_win',

'bh_slice_deep_win',
'bh_slice_short_low_win',


'approach_win_perc',
    'rally_winners_per_match',
    'bh_cross_finish_win',
'fh_cross_finish_win',
'bh_cross_change_dtl_win',
'fh_cross_change_dtl_win',

    'topspin_slice',
    'fh_cc_dtl_ratio',
    'bh_cc_dtl_ratio',
    'bh_cc_speed',
    'bh_cc_depth',
    'bh_cc_spin',
    'bh_dtl_speed',
    'fh_cc_speed',
    'fh_cc_spin',
    'fh_cc_depth',
    'fh_dtl_speed',
    
    
    'bh_dtl_depth',
    'fh_dtl_depth',
    
    
    'bh_dtl_spin',
    'fh_dtl_spin',
    'rally_winners_per_match',
'topspin_slice',
'fh_cc_dtl_ratio',
'bh_cc_dtl_ratio',
'bh_cc_speed',
'bh_dtl_speed',
'fh_dtl_speed',
'fh_cc_speed',
'bh_cc_depth',
'bh_dtl_depth',
'fh_dtl_depth',
'fh_cc_depth',
'bh_cc_speed_winners',
'bh_dtl_speed_winners',
'fh_dtl_speed_winners',
'fh_cc_speed_winners',
'bh_cc_depth_winners',
'bh_dtl_depth_winners',
'fh_dtl_depth_winners',
'fh_cc_depth_winners',
'bh_dtl_all_rally_shots',
'bh_dtl_well_placed',
'bh_dtl_fast',
'fh_all_rally_shots',
'run_around_fh_percentage',
'run_around_fh_winners_fe',
'win_in_rallies_with_run_around_forehand',
'fast_attacking_deuce_fh_cross_percentage',
'fast_attacking_deuce_fh_cross_won',
'fast_attacking_deuce_fh_line_percentage',
'fast_attacking_deuce_fh_line_won',
'opponent_moved_on_neutral_ball',
'dropshots_in_rallies',
'dropshots_fh_win',
'dropshots_bh_win',
'on_the_run_fh_percent',
'on_the_run_bh_percent',
'on_the_run_fh_won',
'on_the_run_bh_won',
'on_the_run_bh_slice',
'on_the_run_bh_slice_won',
'on_the_run_bh_slice_won_on_fast',
'bh_cross_finish_win',
'fh_cross_finish_win',
'bh_cross_change_dtl_win',
'fh_cross_change_dtl_win',
'bh_cross_change_to_fh',
'fh_cross_change_to_bh',
'fast_ball_received_to_bh_percent',
'fast_ball_outgoing_balls_to_opponent_bh']
    
not_by_100 = [
    "movement_to_fh_avg_speed",
    "movement_to_fh_avg_acc",
    "movement_to_fh_avg_decc",
    "movement_to_bh_avg_speed",
    "movement_to_bh_avg_acc",
    "movement_to_bh_avg_decc",
    "movement_first_serve_speed",
    "movement_first_serve_acc",
    "movement_first_serve_decc",
    "movement_second_serve_speed",
    "movement_second_serve_acc",
    "movement_second_serve_decc",
    "movement_to_fh_direction_right_avg_speed",
    "movement_to_fh_direction_right_avg_acc",
    "movement_to_fh_direction_right_avg_decc",
    "movement_to_fh_direction_forward_avg_speed",
    "movement_to_fh_direction_forward_avg_acc",
    "movement_to_fh_direction_forward_avg_decc",
    "movement_to_fh_direction_backward_avg_speed",
    "movement_to_fh_direction_backward_avg_acc",
    "movement_to_fh_direction_backward_avg_decc",
    "movement_to_bh_direction_forward_avg_speed",
    "movement_to_bh_direction_forward_avg_acc",
    "movement_to_bh_direction_forward_avg_decc",
    "movement_to_bh_direction_backward_avg_speed",
    "movement_to_bh_direction_backward_avg_acc",
    "movement_to_bh_direction_backward_avg_decc",
    "movement_to_bh_direction_right_avg_speed",
    "movement_to_bh_direction_right_avg_acc",
    "movement_to_bh_direction_right_avg_decc",
    'rally_winners_and_forcing_error_per_match', # WINNERS & ERRORS
'bh_consistency_new',
'fh_consistency_new',
'fh_errors',
'bh_errors',
'fh_winners_easy_ball',
'bh_winners_easy_ball',
'fh_errors_easy_ball',
'bh_errors_easy_ball',
'bh_cross_change_dtl_count',
'fh_cross_change_dtl_count',
'on_the_run_fh_count',
'on_the_run_bh_count',


'dropshots_count',
'bh_slice_deep_count',


'bh_slice_short_low_count',
'approach_win_perc_count',

    'rally_winners_per_match',
    'rally_ue_per_match',



    'second_serve_speed_ad_t',
    'second_serve_speed_ad_w',
    'second_serve_speed_deuce_t',
    'second_serve_speed_deuce_w',
    'serve_quality_second_deuce_wide',
'serve_quality_second_deuce_t',
'serve_quality_second_ad_wide',
'serve_quality_second_ad_t',
    'fh_consistency_winners', 
                     'bh_consistency_winners', 'first_serve_speed', 
                     'fh_consistency', 
                     'bh_consistency', 'initiative_over_nine', 'initiative_second', 'initiative_second_return', 'initiative_first_over_nine', 'serve_speed_reduction_pressure', 
                     'return_speed_reduction_break', 'break_point_faced_win', 
                     'break_point_opportunity_win',
                     'serve_quality_deuce_wide',
                    'serve_quality_deuce_t',
                    'serve_quality_ad_wide',
                    'serve_quality_ad_t',
                    'bh_middle_consistency',
                    'bh_ad_consistency',
                    'fh_middle_consistency',
                    'fh_deuce_consistency',
                    'fh_ad_consistency',
                    'first_return_speed',
                    'first_return_fh_speed',
    'first_return_bh_speed',
    'first_return_deuce_speed',
    'first_return_ad_speed',
    'first_return_deuce_fh_speed',
    'first_return_deuce_bh_speed',
    'first_return_ad_fh_speed',
    'first_return_ad_bh_speed',
    'second_return_fh_speed',
    'second_return_bh_speed',
    'second_return_deuce_speed',
    'second_return_ad_speed',
    'second_return_deuce_fh_speed',
    'second_return_deuce_bh_speed',
    'second_return_ad_fh_speed',
    'second_return_ad_bh_speed',
    
'second_return_depth',
'first_return_depth',
'average_rally_length_serving_1st',
'average_rally_length_serving_2nd',
'rally_winners_per_match',
'rally_ue_per_match',
'topspin_slice',
'fh_cc_dtl_ratio',
'bh_cc_dtl_ratio',
'bh_cc_speed',
'bh_dtl_speed',
'fh_dtl_speed',
'fh_cc_speed',
'bh_cc_depth',
'bh_dtl_depth',
'fh_dtl_depth',
'fh_cc_depth',
'bh_deuce_consistency',
'bh_cc_spin',
'bh_dtl_spin',
'fh_dtl_spin',
'fh_cc_spin',
'bh_cc_speed_winners',
'bh_dtl_speed_winners',
'fh_dtl_speed_winners',
'fh_cc_speed_winners',
'bh_cc_depth_winners',
'bh_dtl_depth_winners',
'fh_dtl_depth_winners',
'fh_cc_depth_winners',
'bh_cc_spin_winners',
'bh_dtl_spin_winners',
'fh_dtl_spin_winners',
'fh_cc_spin_winners'


                     ]


def get_data_for_player_best_matches(selected_player_name, leaderboardx, reference_players):
    
    data = dict()
    for k in funcs:
        
        leaderboard = leaderboardx.copy(deep=True)
        leaderboard = leaderboard[leaderboard.player_name == selected_player_name]
        leaderboard = leaderboard[leaderboard.match_id != 'ALL']
        if k not in ['return_speed_reduction_break', 'serve_speed_reduction_pressure', 'rally_winners_per_match', 'rally_ue_per_match']:
            leaderboard = leaderboard[leaderboard[f"{k}_total"] > 6]
        else:
            if k not in ['rally_winners_per_match', 'rally_ue_per_match']:
                leaderboard[k] = leaderboard[k]*(-1)
        ascending = False
        if k in ['fh_consistency', 'bh_consistency', 'short_return', 'fh_consistency_winners', 'bh_consistency_winners', 'rally_ue_per_match']:
            ascending = True
        leaderboard[f'{k}_rank'] = leaderboard[f'{k}'].rank(ascending=ascending, method='min')
        if k not in not_by_100:
            leaderboard[f'{k}'] = round(leaderboard[f'{k}'] * 100, 0)
        else:
            if k in ['first_return_depth', 'second_return_depth'] or k in gs_stats:
                leaderboard[k] = round(leaderboard[k] * 1, 2)
            else:
                leaderboard[k] = round(leaderboard[k] * 1, 0)
        leaderboard = leaderboard[leaderboard[f'{k}_rank'] == 1]
        best_match = '\n'.join([f"{x}: {y}" for x, y in zip(leaderboard.match_id.to_list(), leaderboard[f'{k}'].to_list())])
        data[k] = best_match

    data_best = dict()
    for k in funcs:    
        leaderboard = leaderboardx.copy(deep=True)
        leaderboard = leaderboard[leaderboard.match_id == 'ALL']
        if k not in ['return_speed_reduction_break', 'serve_speed_reduction_pressure', 'rally_winners_per_match', 'rally_ue_per_match']:
            leaderboard = leaderboard[leaderboard[f"{k}_total"] > 9]
        else:
            if k not in ['rally_winners_per_match', 'rally_ue_per_match']:
                leaderboard[k] = leaderboard[k]*(-1)
        leaderboard = leaderboard[leaderboard.player_name.isin(reference_players)]
        ascending = False
        if k in ['fh_consistency', 'bh_consistency', 'short_return', 'fh_consistency_winners', 'bh_consistency_winners']:
            ascending = True
        leaderboard[f'{k}_rank'] = leaderboard[f'{k}'].rank(ascending=ascending, method='min')
        if k not in not_by_100:
            leaderboard[f'{k}'] = round(leaderboard[f'{k}'] * 100, 0)
        else:
            if k in ['first_return_depth', 'second_return_depth'] or k in gs_stats:
                leaderboard[k] = round(leaderboard[k] * 1, 2)
            else:
                leaderboard[k] = round(leaderboard[k] * 1, 0)
        leaderboard = leaderboard[leaderboard[f'{k}_rank'] <= 5]
        leaderboard = leaderboard.sort_values(f'{k}_rank')
        best_match = '\n'.join([f"{x}: {y}" for x, y in zip(leaderboard.player_name.to_list(), leaderboard[f'{k}'].to_list())])
        data_best[k] = best_match
    return (data, data_best)

def get_data_for_matches_new(selected_player_name, leaderboardx, match_ids=[]):
    print(selected_player_name)
    sets_data = dict()
    for sets in ['ALL', '1', '2', '3', '4', '5']:
        data_new = dict()
        for k in funcs:
            
            leaderboard = leaderboardx.copy(deep=True)
            leaderboard = leaderboard[leaderboard.sets == sets]
            
            leaderboard = leaderboard[leaderboard.player_name.isin(selected_player_name)]
            
            #print('Leader1', leaderboard.shape)
            if match_ids:
                leaderboard = leaderboard[leaderboard.match_id.isin(match_ids)]
            else:
                leaderboard = leaderboard[leaderboard.match_id != 'ALL']
            #print('Leader2', leaderboard.shape)
            
            ascending = False
            if k in ['fh_consistency', 'bh_consistency', 'short_return', 'fh_consistency_winners', 'bh_consistency_winners', 'serve_speed_reduction_pressure', 'return_speed_reduction_break']:
                ascending = True
            if k in ['return_speed_reduction_break', 'serve_speed_reduction_pressure']:
                leaderboard[k] = leaderboard[k]*(-1)        
            leaderboard[f'{k}_mul'] = leaderboard[f'{k}']*leaderboard[f'{k}_total']
            leaderboard[f'{k}_rank'] = leaderboard[f'{k}'].rank(ascending=ascending, method='min')
            
            if leaderboard[f'{k}_total'].sum() < 0 and k not in ['return_speed_reduction_break', 'serve_speed_reduction_pressure', 'rally_winners_per_match', 'rally_ue_per_match']:
                data_new[k] = 'Not enough shots (< 6)'
            else:
                if leaderboard[f'{k}_total'].astype(float).sum() == 0:
                    data_new[k] = 0
                else:
                    data_new[k] = leaderboard[f'{k}_mul'].astype(float).sum() / leaderboard[f'{k}_total'].astype(float).sum()
            
                if k not in not_by_100:
                    data_new[k] = robust_round(data_new[k] * 100)
                else:
                    if k in ['first_return_depth', 'second_return_depth'] or k in gs_stats or k in ['bh_dtl_all_rally_shots',
    'bh_dtl_well_placed',
    'bh_dtl_fast',
    'fh_all_rally_shots',
    'run_around_fh_percentage',
    'run_around_fh_winners_fe',
    'win_in_rallies_with_run_around_forehand',
    'fast_attacking_deuce_fh_cross_percentage',
    'fast_attacking_deuce_fh_cross_won',
    'fast_attacking_deuce_fh_line_percentage',
    'fast_attacking_deuce_fh_line_won',
    'opponent_moved_on_neutral_ball',
    'dropshots_in_rallies',
    'dropshots_fh_win',
    'dropshots_bh_win']:
                        #print('here')
                        data_new[k] = round(data_new[k] * 1, 2)
                    else:
                        data_new[k] = robust_round(data_new[k] * 1)
            sets_data[sets] = data_new
    #print(sets_data, 'HEEERERAJPFOAJFOPAJFOPAGJAOPGJAGOPJGPOA')
    import json
    with open('json_data.json', 'w') as f:
        json.dump(sets_data, f, indent=4)
    return sets_data
        

def get_data_for_matches_new2(selected_player_name, leaderboard_clean, match_ids=[]):
    l1 = leaderboard_clean[(leaderboard_clean.match_id.isin(match_ids)) & (leaderboard_clean.player_name.isin(selected_player_name))]
    return l1.set_index('sets').to_dict('index')


# def get_he_visuals(selected_player_name='SINNER', selected_match_ids=[], selected_match_ids_previous=[], reference_players=[], reference_matches=[], leftie=False, tour='ATP'):
#     pronoun = 'THEIR'
#     if tour.lower() == 'atp':
#         pronoun = 'HIS'
#     elif tour.lower() == 'wta':
#         pronoun = 'HER'
#     selected_player_name = selected_player_name.upper()
#     if len(selected_player_name.split(' ')[0]) == 1:
#         selected_player_name = ' '.join(selected_player_name.split(' ')[1:])
   
    
#     data = get_data_for_matches(selected_player_name, leaderboard, selected_match_ids)
#     data_previous = get_data_for_matches(selected_player_name,leaderboard, selected_match_ids_previous)
#     data_player_reference = get_data_for_matches(selected_player_name,leaderboard, reference_matches)
#     data_player, data_best = get_data_for_player_best_matches(selected_player_name, leaderboard, reference_players=reference_players)

    


    
#     #return data, data_previous, data_player, data_best, selected_match_ids, selected_match_ids_previous
#     return data, data_previous, data_player_reference, data_best, selected_match_ids, selected_match_ids_previous, data_player

#get_he_visuals()