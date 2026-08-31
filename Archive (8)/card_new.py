import argparse
import os
import numpy as np
import pandas as pd
from utils import *

def robust_round(x, factor=0):
    if not x or np.isnan(x):
        return 0
    else:
        return int(round(x, factor))
funcs = [
    
    'second_return_in_percentage',
    'second_serve_speed_ad_t',
    'second_serve_speed_ad_w',
    'second_serve_speed_deuce_t',
    'second_serve_speed_deuce_w',
    'win_percent_first_serve',
    'win_percent_first_serve_pressure',
    'win_percent_first_serve_break',
    'serve_quality_second_deuce_wide',
'serve_quality_second_deuce_t',
'serve_quality_second_ad_wide',
'serve_quality_second_ad_t',
'first_return_in_percentage',
'first_return_in_percentage_pressure',
'first_return_in_percentage_break',
'first_return_win_percentage_pressure',
'first_return_win_percentage_break',
    'win_percent_second_serve_ad_wide',
        'percent_unreturned_first_serves',
        'first_serve_in_percentage',
        'first_serve_in_percentage_pressure',
        'first_serve_in_percentage_break',
        'first_serve_speed',
        'percent_of_first_serves_within_04m_of_sideline',
        'first_return_percent_deep',
        'first_return_percent_short',
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
        'fh_middle_consistency',
        'fh_deuce_consistency',
        'fh_ad_consistency',
        'bh_deuce_consistency',
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
                'first_return_depth',
                'second_return_depth',
                'second_return_percent_deep',
                'first_return_win_percentage',
                'second_return_win_percentage',
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
'approach_win_perc',

'approach_fh_win_perc',

'approach_bh_win_perc',

'approach_to_fh_win_perc',

'approach_to_bh_win_perc',
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
'first_return_speed',
            'first_return_fh_speed',
            'first_return_bh_speed',
'strong_serve_plus1',
'weak_serve_plus1',
'win_percent_second_serve',
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
'second_bh_return_in_percentage'
    ]
    
gs_stats = ['rally_winners_per_match',
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
'fast_ball_outgoing_balls_to_opponent_bh',
'fh_errors',]
    
not_by_100 = [
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

def get_data_for_matches(selected_player_name, leaderboardx, match_ids=[]):
    
    data_new = dict()
    for k in funcs:
        
        leaderboard = leaderboardx.copy(deep=True)
        leaderboard = leaderboard[leaderboard.player_name.isin(selected_player_name)]
        if k == 'first_serve_speed':
            
            print('MATCHES:', leaderboard.match_id.unique())
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
    
    return data_new
        




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