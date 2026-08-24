"""Post-match stat pipeline (main3) for the /gui/match_new report page.

Trimmed from the original report_util_new.py: only main3 is kept and the unused
DB imports are gone. The leaderboard is shared with report_core (same parquet).
"""
from pathlib import Path

import pandas as pd

from card_new2 import get_data_for_matches_new2

APP_DIR = Path(__file__).parent
leaderboard3 = pd.read_parquet(APP_DIR / 'leaderboard_haddad_new_wta_with_sets_clean.parquet')

# CV-derived leaderboard rows live in their own parquet so Hawk-Eye data
# refreshes never overwrite them; the app sees one combined leaderboard.
_cv_leaderboard = APP_DIR / 'cv_post_match' / 'leaderboard_cv.parquet'
if _cv_leaderboard.exists():
    leaderboard3 = pd.concat([leaderboard3, pd.read_parquet(_cv_leaderboard)], ignore_index=True)

# Some archive exports store serve-speed columns x100 (e.g. 19000 for 190 km/h).
# No tennis ball travels 1000+ km/h, so fix any such row at load time.
for _c in leaderboard3.columns:
    if 'speed' in _c and not _c.endswith('_total') and leaderboard3[_c].dtype.kind in 'if':
        _mis = leaderboard3[_c] > 1000
        if _mis.any():
            leaderboard3.loc[_mis, _c] = leaderboard3.loc[_mis, _c] / 100

def main3(selected_player_name='BERRETTINI', 
        opponent_name='',
        matches=[],
        leaderboard1 = True
        ):

    
    #with open('ultimate_results.json', 'rb') as f:
        #result = pickle.load(f)
    
    
    
    #print('------------------------------------', selected_player_name, opponent_name, matches)
    data_player = get_data_for_matches_new2(selected_player_name, leaderboard3, matches)
    #print('DATA PLAYER', matches, data_player)
    data_opponent = get_data_for_matches_new2(opponent_name, leaderboard3, matches)
    #data_2023_1 = get_data_for_matches(['DJOKOVIC', 'SINNER', 'ALCARAZ'], leaderboard, [])
    #data_2023_2 = get_data_for_matches(['PAUL', 'FRITZ', 'RUBLEV', 'NAKASHIMA'], leaderboard, [])
    #_,data_2023_1 = get_data_for_player_best_matches('HADDAD MAIA', leaderboard, ['SWIATEK', 'GAUFF', 'RYBAKINA'])
    #print(data_2023_all)
    #data_2023_all = get_data_for_matches(selected_player_name, leaderboard, [x for x in selected_match_ids if '2023' in x])
    #data_2023_lost = get_data_for_matches(selected_player_name, leaderboard, [x for x in selected_match_ids if '2022' in x])
    #best_matches = ['US_Open_2023_R32_Paul_Davidovich-Fokina', 'Rogers-cup_2023_QF_Alcaraz_Paul', 'Rogers-cup_2023_R16_Paul_Giron', 'Acapulco_2023_QF_Mcdonald_Paul', 'Miami_2023_R32_Davidovich-Fokina_Paul', 'Indian-Wells_2023_R32_Hurkacz_Paul', 'Acapulco_2023_SF_Paul_Fritz']
    #data_2023_best = get_data_for_matches(selected_player_name, leaderboard, [x for x in selected_match_ids if x in best_matches])
    #data, data_previous, data_player, data_best, post_match, prior_matches, data_player_best = get_he_visuals(selected_player_name, selected_match_ids, selected_match_ids_previous, reference_players=reference_players, reference_matches=reference_matches)

    
    #p = document.add_paragraph(f"2023 US SWING ALL MATCHES: {', '.join(matches_2023)}")
    #p = document.add_paragraph(f"2022 LATE AND 2023 EARLY ALL MATCHES: {', '.join(matches_2022)}")
    #p = document.add_paragraph(f"2023 BEST MATCHES: {', '.join(best_matches)}")
    

    data_order = {
        'other': [
            'rally_long', 
    'serve_plus_win',
        ],
        'serve': [
            'first_serve_in_percentage',
            'first_serve_in_percentage_pressure',
            'first_serve_in_percentage_break',
            'win_percent_first_serve',
            'win_percent_first_serve_pressure',
            'win_percent_first_serve_break',
            'first_serve_speed',
            'percent_of_first_serves_within_04m_of_sideline',
            'percent_unreturned_first_serves',
            'strong_serve_plus1',
            'weak_serve_plus1'
        ],
        'serve_2nd': [
            
            'win_percent_second_serve',
            
            'second_serve_weak_returns',
            'second_serve_attacked',
            'offensive_serve_plus1',
            'defensive_serve_plus1',
            'second_serve_speed_ad_t',
            'second_serve_speed_ad_w',
            'second_serve_speed_deuce_t',
            'second_serve_speed_deuce_w'
            
            
        ], #
        'movement': ["movement_to_fh_avg_speed",
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
    "movement_to_bh_direction_right_avg_decc" ],
        'return': [
            'first_return_in_percentage',
            'first_return_in_percentage',
'first_return_in_percentage_pressure',
'first_return_in_percentage_break',
'first_return_win_percentage',
'first_return_win_percentage_pressure',
'first_return_win_percentage_break',
            'first_return_percent_deep',
            'first_return_depth',
            
            'first_return_extended_or_won',
            'first_return_speed',
            'first_return_fh_speed',
            'first_return_bh_speed',
            'first_bh_return_in_percentage',
'first_fh_return_in_percentage',
        
            

        ],
        'return_2nd': [
            'second_return_in_percentage',
            'second_return_win_percentage',
            'second_fh_return_in_percentage',
            'second_bh_return_in_percentage',
            'second_return_extended_or_won',
            'second_return_percent_deep',
            'second_return_depth',
            'second_return_aggressive',
            'second_return_fh_speed',
            'second_return_bh_speed',
            
        ],
        'return_speed': [
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
            'second_return_ad_bh_speed'
        ],
        'consistency': [
            'fh_deuce_consistency',
            'fh_middle_consistency',
            'fh_ad_consistency',
            'bh_middle_consistency',
            'bh_ad_consistency',
            'bh_deuce_consistency'    
        ],
        'initiative': [
            'initiative_first_over_nine',
            'initiative_over_nine',
            'initiative_second',
            'initiative_second_return',
        ],
        'strength': [
            'break_point_faced_win',
            'break_point_opportunity_win',
            'serve_speed_reduction_pressure',
            'return_speed_reduction_break'
        ],
        'groundstroke_table': [
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
'on_the_run_fh_won',
    'on_the_run_bh_won',
'dropshots_win',
'dropshots_count',
'bh_slice_deep_count',
'bh_slice_deep_win',
'bh_slice_short_low_win',
'bh_slice_short_low_count',
'approach_win_perc_count',
'approach_win_perc',
    'rally_winners_per_match',
    'fh_rally_winners_and_forcing_error_per_match',
    'bh_rally_winners_and_forcing_error_per_match',
    'rally_ue_per_match',
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
    
            ],
        'approach_stats': [
            'approach_win_percentage',
    'approaches_to_FH',
    'approaches_to_BH',
    'approach_percentage',
    'approach_fh_win_perc',

    'approach_bh_win_perc',

    'approach_to_fh_win_perc',

    'approach_to_bh_win_perc',
        ],
        'rally_play_type': [
            'rally_play_long_rallies_won',
    'rally_play_1st_serve_won_in_5_shots_or_less',
    'rally_play_1st_serve_finished_in_5_shots_or_less',
    'rally_play_2nd_return_won_in_5_or_less'
        ],
        'dropshots': [           
    'dropshots_in_rallies',
    'dropshots_fh_win',
    'dropshots_bh_win'
        ],
        'offensive': [
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
    'opponent_moved_on_neutral_ball'
        ],
        'defensive': ['on_the_run_fh_percent',
    'on_the_run_bh_percent',
    'on_the_run_fh_won',
    'on_the_run_bh_won',
    'on_the_run_bh_slice',
    'on_the_run_bh_slice_won',
    'on_the_run_bh_slice_won_on_fast'],
    'rally_patterns': ['bh_cross_finish_win',
    'fh_cross_finish_win',
    'bh_cross_change_dtl_win',
    'fh_cross_change_dtl_win',
    'bh_cross_change_to_fh',
    'fh_cross_change_to_bh',
    'fast_ball_received_to_bh_percent',
    'fast_ball_outgoing_balls_to_opponent_bh']
        }

    
    
    pretty_dict = {
        'second_fh_return_in_percentage': 'FH Return In%',
            'second_bh_return_in_percentage': 'BH Return In%',
            'second_return_fh_speed': 'Avg FH Speed',
            'second_return_bh_speed': 'Avg BH Speed',
        'offensive_serve_plus1': 'Offensive Serve +1',
'defensive_serve_plus1': 'Defensive Serve +1',
        'strong_serve_plus1': '% of Strong Serve +1',
        'weak_serve_plus1': '% of Weak Serve +1',
        'second_return_in_percentage': 'In%',
        'first_return_in_percentage': 'In%',
'first_return_in_percentage_pressure': 'In% - pressure points',
'first_return_in_percentage_break': 'In% - break points',

'first_return_win_percentage_pressure': 'Win% - Pressure points',
'first_return_win_percentage_break': 'Win% - Break points',
        'second_serve_speed_ad_t': 'Speed AD T',
    'second_serve_speed_ad_w': 'Speed AD W',
    'second_serve_speed_deuce_t': 'Speed Deuce T',
    'second_serve_speed_deuce_w': 'Speed Deuce W',
        'serve_quality_second_deuce_wide': 'SQ 2nd Deuce Wide',
'serve_quality_second_deuce_t':'SQ 2nd Deuce T',
'serve_quality_second_ad_wide': 'SQ 2nd AD Wide',
'serve_quality_second_ad_t':'SQ 2nd AD T',
        'win_percent_first_serve': '1st serve win%',
        'win_percent_first_serve_pressure': f'1st serve win% - pressure points',
        'win_percent_first_serve_break': f'1st serve win% - break points',
        'first_serve_in_percentage_pressure': f'1st serve in% - pressure points',
        'first_serve_in_percentage_break': f'1st serve in% - break points',
        'second_return_depth': 'Average Return Depth',
        'second_return_percent_deep': f'% of deep returns',
        'second_return_win_percentage': 'Win%',
        'first_bh_return_in_percentage': 'BH Return In%',
        'first_fh_return_in_percentage': 'FH Return In%',
        'first_return_speed': 'Avg Return Speed',
        'first_return_fh_speed': 'Avg FH Return Speed',
        'first_return_bh_speed': 'Avg BH Return Speed',
        'second_serve_weak_returns': f'% of 2nd serves with weak returns',
        'second_serve_attacked': f'% of 2nd serves that opponents attacked',
        'win_percent_second_serve': f'Win%',
        'win_percent_second_serve_ad_wide': f'2nd Ad Wide Win%',
        'first_return_depth': 'Average Return Depth',
        'first_return_win_percentage': 'Return Win %',
        'percent_unreturned_first_serves': f'% unreturned serves',
        'first_serve_in_percentage': '1st serve in%',
        'first_serve_speed': '1st serve average speed',
        'percent_of_first_serves_within_04m_of_sideline': f'% of well-placed serves (<40cm)',
        'serve_quality_deuce_wide': 'SQ 1st Deuce Wide',
        'serve_quality_deuce_t': 'SQ 1st Deuce T',
        'serve_quality_ad_wide': 'SQ 1st Ad Wide',
        'serve_quality_ad_t': 'SQ 1st AD T',
        'first_return_extended_or_won': f'% of returns that led to extended rallies (5+)',
        'first_return_defeat_under_five': f'% of 1st serve returns that led to extended rallies (5+)',
        'second_return_extended_or_won': f'% of good 2nd returns that extended the point (5+) or player won the point',
        'second_return_aggressive': f'% of aggresive 2nd returns*',
        'first_return_percent_deep': f'% of deep returns',
        'initiative_first_over_nine': f'% of playing inside the court\n on while server on 1st serve when\n rallies 9+ shots ',
        'initiative_over_nine': f'% of playing inside the court\n on rallies +9 shots',
        'initiative_second': '% playing inside the court on 2nd serve',
        'initiative_second_return': f'% of playing inside the court\n on 2nd return',
        'fh_consistency': 'FH unforced errors/amount of total shots hit',
        'bh_consistency': 'BH unforced errors/amount of total shots hit',
        'fh_consistency_winners': 'FH unforced errors percentage among winners/FE',
        'bh_consistency_winners': 'BH unforced errors percentage among winners/FE',
        'break_point_faced_win': f'Break points faced win%',
        'break_point_opportunity_win': f'Break point opportunity win%',
        'serve_speed_reduction_pressure': '1st serve speed reduction when under pressure versus no pressure (negative means speed reduction)',
        'return_speed_reduction_break': 'Return speed reduction on break point opportunities (negative means speed reduction)',
        'fh_deuce_consistency': 'Deuce FH Ball in play%',
        'fh_middle_consistency': 'Middle FH Ball in play%',
        'fh_ad_consistency': 'Ad FH Ball in play%',
        'bh_middle_consistency': 'Middle BH Ball in play%',
        'bh_ad_consistency': 'Ad BH Ball in play%',
        'bh_deuce_consistency': 'Deuce BH Ball in play%',
        'bh_dtl_all_rally_shots': f'% BH DTL IN ALL RALLIES',
        'bh_dtl_well_placed': f'% BH DTL WELL PLACED' ,
        'bh_dtl_fast': f'% FAST BH DTL',
        'fh_all_rally_shots': f'% FH HIT IN RALLIES',
        'run_around_fh_percentage': f'% USE RUN AROUND FH',
        'run_around_fh_winners_fe': f'% WINNERS WHEN RUN AROUND FH',
        'win_in_rallies_with_run_around_forehand': f'WIN % IN RALLIES USING RUN AROUND FH',
        'fast_attacking_deuce_fh_cross_percentage': f'% FAST ATTACKING DEUCE FH CROSS SHOTS',
        'fast_attacking_deuce_fh_cross_won': f'% FAST ATTACKING DEUCE FH CROSS WON',
        'fast_attacking_deuce_fh_line_percentage': f'% FAST ATTACKING DEUCE FH DTL SHOTS',
        'fast_attacking_deuce_fh_line_won': f'% FAST ATTACKING DEUCE FH DTL WON',
        'opponent_moved_on_neutral_ball': f'% MOVED THE OPPONENT AFTER RECEIVING A NEUTRAL BALL',
        'on_the_run_fh_percent': f'% OF TIMES PUT ON THE RUN TO THE FH IN RALLIES',
'on_the_run_bh_percent': f'% OF TIMES PUT ON THE RUN TO THE BH IN RALLIES',
'on_the_run_fh_won': f'% WON WHEN ON THE RUN TO FH',
'on_the_run_bh_won': f'% WON WHEN ON THE RUN TO BH',
'on_the_run_bh_slice': f'% USED SLICE WHEN ON THE RUN TO THE BH',
'on_the_run_bh_slice_won': f'% WON WHEN BH SLICE ON THE RUN',
'on_the_run_bh_slice_won_on_fast': f'% WON WHEN BH SLICE ON THE RUN ON FAST INCOMING BALL',
'bh_cross_finish_win': f'WIN % BH CROSS FINISH',
'fh_cross_finish_win':f'WIN % FH CROSS FINISH',
'bh_cross_change_dtl_win': f'WIN % BH CROSS CHANGE DTL',
'fh_cross_change_dtl_win': f'WIN % FH CROSS CHANGE DTL',
'bh_cross_change_to_fh': f'WIN % BH CROSS CHANGE TO FH',
'fh_cross_change_to_bh': f'WIN % FH CROSS CHANGE TO BH',
'fast_ball_received_to_bh_percent': f'% OF FAST BALLS RECEIVED TO THE BH',
'fast_ball_outgoing_balls_to_opponent_bh': f'% OF FAST OUTGOING BALLS HIT TO OPPONENT BH',
'approach_win_percentage': f'WIN% ON APPROACHES',
'approaches_to_FH': f'% APPROACHES TO FH',
'approaches_to_BH': f'% APPROACHES TO BH',
'approach_percentage': f'% APPROACHES IN RALLIES',
'approach_fh_win_perc': f'WIN % ON FH APPROACHES',

'approach_bh_win_perc': f'WIN % ON BH APPROACHES',

'approach_to_fh_win_perc': f'WIN % APPROACH TO FH',

'approach_to_bh_win_perc': f'WIN % APPROACH TO BH',
'dropshots_in_rallies': f'% DROPSHOTS IN RALLIES',
'dropshots_fh_win': f'WIN% ON FH DROP SHOTS',
'dropshots_bh_win': f'WIN% ON BH DROP SHOTS',
'rally_play_long_rallies_won': f'% of long rallies won',
'rally_play_1st_serve_won_in_5_shots_or_less': '% of 1st serves won in 5 shots or less',
'rally_play_1st_serve_finished_in_5_shots_or_less': '% of 1st serves finished in 5 shots or less',
'rally_play_2nd_return_won_in_5_or_less': '% of 2nd returns won in 5 shots or less',
'rally_winners_per_match': 'rally winners per match',
'fh_rally_winners_and_forcing_error_per_match': 'FH WINNERS + FORCING ERRORS',
'bh_rally_winners_and_forcing_error_per_match': 'BH WINNERS + FORCING ERRORS',
'rally_ue_per_match': 'UNFORCED ERRORS',
'fh_cc_dtl_ratio': 'FH CC / DTL ratio',
'bh_cc_dtl_ratio': 'BH CC / DTL ratio',
'bh_cc_speed': 'bh cc speed',
'bh_dtl_speed': 'bh dtl speed',
'fh_dtl_speed': 'fh dtl speed',
'fh_cc_speed': 'fh cc speed',
'bh_cc_depth': 'bh cc depth',
'bh_dtl_depth': 'bh dtl depth',
'fh_dtl_depth': 'fh dtl depth',
'fh_cc_depth': 'fh cc depth',
'bh_cc_spin': 'bh cc spin',
'bh_dtl_spin': 'bh dtl spin',
'fh_dtl_spin': 'fh dtl spin',
'fh_cc_spin': 'fh cc spin',
'bh_cc_speed_winners': 'bh cc speed winners',
'bh_dtl_speed_winners': 'bh dtl speed winners',
'fh_dtl_speed_winners': 'fh dtl speed winners',
'fh_cc_speed_winners': 'fh cc speed winners',
'bh_cc_depth_winners': 'bh cc depth winners',
'bh_dtl_depth_winners': 'bh dtl depth winners',
'fh_dtl_depth_winners': 'fh dtl depth winners',
'fh_cc_depth_winners': 'fh cc depth winners',
'bh_cc_spin_winners': 'bh cc spin winners',
'bh_dtl_spin_winners': 'bh dtl spin winners',
'fh_dtl_spin_winners': 'fh dtl spin winners',
'fh_cc_spin_winners': 'fh cc spin winners',
'topspin_slice': 'BH Topspin / BH Slice ratio',
'bh_cross_finish_win': f'WIN% IN CROSS BH RALLIES',
'fh_cross_finish_win':f'WIN% IN CROSS FH RALLIES',
'bh_cross_change_dtl_win': f'WIN% CHANGING DIRECTION BH DTL',
'fh_cross_change_dtl_win': f'WIN% CHANGING DIRECTION FH DTL',
'rally_winners_and_forcing_error_per_match': 'WINNERS + FORCING ERRORS', # WINNERS & ERRORS
'bh_consistency_new': 'BH IN PLAY %',
'fh_consistency_new': 'FH IN PLAY %',
'fh_errors': 'FH ERRORS',
'bh_errors': 'BH ERRORS',
'shots_hit_inside': '% OF SHOTS HIT INSIDE THE COURT', # LOCATION
'shots_hit_behind_bl': '% OF SHOTS HIT FROM BEHIND THE BASELINE',
'shots_hit_further_back': '% OF SHOTS HIT FROM FURTHER BACK',
'fh_winners_easy_ball': 'FH FINISHING SHOTS ON EASY BALLS',
'bh_winners_easy_ball': 'BH FINISHING SHOTS ON EASY BALLS',
'fh_errors_easy_ball': 'FH ERRORS ON EASY BALLS',
'bh_errors_easy_ball': 'BH ERRORS ON EASY BALLS',
'bh_cross_change_dtl_count': 'CHANGES OF DIRECTION BH DTL',
'fh_cross_change_dtl_count': 'CHANGES OF DIRECTION FH DTL',
'on_the_run_fh_count': 'TIMES PLACING THE OPPONENT ON THE RUN TO FH',
'on_the_run_bh_count': 'TIMES PLACING THE OPPONENT ON THE RUN TO BH',
'on_the_run_fh_won': 'WIN% PLACING THE OPPONENT ON THE RUN TO FH',
    'on_the_run_bh_won': 'WIN% PLACING THE OPPONENT ON THE RUN TO BH',
'dropshots_win': 'WIN% ON DROP SHOTS',
'dropshots_count': 'TIMES HITTING A DROP SHOT',
'bh_slice_deep_count': 'TIMES USING CROSS BH SLICE DEEP',
'bh_slice_deep_win': 'WIN% USING CROSS BH SLICE DEEP',
'bh_slice_short_low_count': 'TIMES USING CROSS BH SLICE LOW SHORT ANGLE',
'bh_slice_short_low_win': 'WIN% USING CROSS BH SLICE LOW SHORT ANGLE',
'approach_win_perc_count': 'TIMES APPROACHING THE NET',
'approach_win_perc': 'WIN% APPROACHING THE NET',
'rally_long': 'WIN% IN LONG RALLIES (+9 SHOTS)', 
    'serve_plus_win': '% OF POINTS WON WITH THE SERVE +1 (WITHIN 5 SHOTS AFTER SERVE)',


    }
    for k in ['bh_cc_speed',
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
'fh_cc_spin_winners']:
        if 'winner' in k:
            xk = f'{k.replace("_", " ").upper()} FE'
        else:
            xk = f'{k.replace("_", " ").upper()}'
        pretty_dict[k] = xk
    
    return pretty_dict, data_player, data_opponent, data_order
