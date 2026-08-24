import pandas as pd
import time
import numpy as np

functions = [
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
'fh_rally_winners_per_match',
'bh_rally_winners_per_match',
'rally_ue_per_match',
'fh_rally_ue_per_match',
'bh_rally_ue_per_match',
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
'fh_rally_winners_and_forcing_error_per_match', # WINNERS & ERRORS
'bh_rally_winners_and_forcing_error_per_match', # WINNERS & ERRORS
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
columns = ['player_name', 'match_id', 'opponent_name', 'surface']
for x in functions:
    columns.append(x)
    columns.append(x + '_total')

class Calculations:
    # instance variable for player name - assuming we are running these calculations on data from an individual player
    PLAYER_NAME = None
    # magic numbers
    PRESSURE = {'0030', '30', '1530', '3030', '4040', 'deuce'}
    BREAK = {'0040', '40', '1540', '3040', '40Adv', '40Av', '40A'}
    SLICE = None
    FAST = 190
    SHORT_BORDER = 6.40
    DEEP_BORDER = 9.18
    MIDDLE_Y = 0
    STANDS_IN = 11.88
    STANDS_BACK = 11.88
    STANDS_FAR_BACK = 13.88
    DEUCE_THIRD_COORDS = -1.37
    AD_THIRD_COORDS = 1.37
    HIGHER_OVER_NET = 2.09
    LOWER_OVER_NET = 1.5


    # initialize results dataframe
    results_df = pd.DataFrame(columns=columns)

    #  class param is file name of an individual player's data csv formatted ...data/name_data.csv
    def __init__(self, player_name, df, df_serve, is_leftie, sets='ALL'):

        # get player name from csv name
        Calculations.PLAYER_NAME = player_name
        if is_leftie:
            Calculations.LEFTIE = -1
        else:
            Calculations.LEFTIE = 1
        all_matches_df = df
        all_matches_df_serve = df_serve
        # only include shots by player
        # all_matches_df = all_matches_df[all_matches_df.PLAYER_HIT == Calculations.PLAYER_NAME]
        # calculate career statistics
        if sets != 'ALL':
            all_matches_df = all_matches_df[all_matches_df.set_no == sets]
            all_matches_df_serve = all_matches_df_serve[all_matches_df_serve.set_no == sets]
        if all_matches_df.empty:
            return
        Calculations.calculate_all(self, all_matches_df, all_matches_df_serve, 'ALL', sets)
        # calculate per match statistics
        Calculations.calculate_matches(self, all_matches_df, all_matches_df_serve, sets)

    def calculate_all(self, df, df_serve, match_id, sets):
        # Define a list of functions and their corresponding labels

        # Calculate and add the values for each function to the DataFrame
        new_row = {'player_name': Calculations.PLAYER_NAME,
                   'match_id': match_id,
                   'opponent_name': self.get_opponent_name(df, match_id),
                   'surface': self.get_surface(df, match_id)}
        for func_name in functions:
            if func_name in [
                'rally_long', 
    'serve_plus_win',
               'win_percent_first_serve', 'win_percent_first_serve_pressure',
                'win_percent_first_serve_break', 'percent_of_first_serves_within_04m_of_sideline',
                'percent_of_first_serves_within_04m_of_sideline_pressure', 'percent_of_first_serves_within_04m_of_sideline_break',
                'first_serve_speed','first_serve_speed_deuce_w', 'first_serve_speed_deuce_t', 'first_serve_speed_ad_w', 'first_serve_speed_ad_t',
            'first_serve_speed_decrease_break', 'first_serve_speed_decrease_break_deuce', 'first_serve_speed_decrease_break_ad',
            'avg_return_speed_opponent', 'percent_unreturned_first_serves',
            'percent_first_serves_won_in_two_to_four_shots', 'first_serve_in_percentage',
            'first_serve_in_percentage_pressure', 'first_serve_in_percentage_break',
            
            
            'win_percent_first_serve_rally_five_to_eight', 'win_percent_first_serve_rally_nine_plus',
            'percent_serve_points_won', 'percent_aces_per_serve_points',
            'avg_points_won_per_serve_game', 'avg_points_lost_per_serve_game',
            'serve_hold_rate', 'serve_win_percentage_when_return_in', 'serve_win_percentage_when_return_fast',
            'serve_win_percentage_when_return_deep', 'serve_win_percentage_when_return_middle',
            'serve_win_percentage_when_return_short', 'serve_win_percentage_when_returner_stands_in',
            'serve_win_percentage_when_returner_stands_back', 'serve_win_percentage_when_returner_stands_far_back',
            'percent_serve_pone_deuce_after_deuce_returned_middle', 'percent_serve_pone_ad_after_ad_returned_middle','first_return_in_percentage',
'second_return_in_percentage','serve_quality_deuce_wide',
'serve_quality_deuce_t',
'serve_quality_ad_wide',
'serve_quality_ad_t','strong_serve_plus1',
'win_percent_second_serve',
'win_percent_second_serve_ad_wide',
'second_serve_weak_returns',
'first_return_percent_high',
'first_return_percent_fast',
'first_return_percent_angled',
'first_return_win_percentage',
'serve_quality_second_deuce_wide',
'serve_quality_second_deuce_t',
'serve_quality_second_ad_wide',
'serve_quality_second_ad_t',
'first_return_in_percentage_pressure',
'first_return_in_percentage_break',
'first_return_win_percentage_pressure',
'first_return_win_percentage_break'


            ]:
                func = getattr(self, func_name)
                result = func(df_serve)
            else:
                func = getattr(self, func_name)
                result = func(df)
            if result is not None:
                new_row[f'{func_name}'] = result[0]
                new_row[f'{func_name}_total'] = result[1]
            else:
                # Handle the case when result is None (if needed)
                new_row[f'{func_name}'] = None
                new_row[f'{func_name}_total'] = None
        new_dataset = pd.DataFrame(new_row, index=[0])
        new_dataset['sets'] = sets
        Calculations.results_df = \
            pd.concat([Calculations.results_df, new_dataset], ignore_index=True)


    # groups by match and calls calculate_all for each match
    def calculate_matches(self, all_matches_df, all_matches_df_serve, sets):
        grouped_matches_df = all_matches_df.groupby('match_id')
        grouped_matches_df_serve = all_matches_df_serve.groupby('match_id')
        for match_id, match_group in grouped_matches_df:
            for match_id_serve, match_group_serve in grouped_matches_df_serve:
                if match_id == match_id_serve:
                    Calculations.calculate_all(self, match_group, match_group_serve, match_id, sets)

    


    def get_opponent_name(self, df, match_id):
        if match_id == 'ALL':
            return 'ALL'
        df = df.reset_index(drop=True)
        server_name = df.at[1, 'server_name']
        receiver_name = df.at[1, 'receiver_name']
        if server_name == Calculations.PLAYER_NAME:
            Calculations.opponent_name = receiver_name
            return receiver_name
        else:
            Calculations.opponent_name = server_name
            return server_name

    def get_surface(self, df, match_id):
        if match_id == 'ALL':
            return 'ALL'
        df = df.reset_index(drop=True)
        surface = df.at[1, 'surface']
        return surface
    
    def strong_serve_plus1(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        strong_count = len(df_serves[(df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME) & (df.rally_length < 7)])
        if total == 0:
            return 0, 0
        percent = strong_count / total
        return percent, total

    def offensive_serve_plus1(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_serves)
        strong_count = len(df_serves[(df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME) & (df.rally_length < 7)])
        if total == 0:
            return 0, 0
        percent = strong_count / total
        return percent, total
    
    def defensive_serve_plus1(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_returns = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 4) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_serves)
        weak_count = list(df_returns[(df_returns.PLAYER_WIN_NAME != df_returns.server_name) & (df.rally_length == 4)].point_id.unique())
        pushed_back = list(df_returns[(df_returns.CONTACT_X_abs_next > df_returns.CONTACT_X_abs_previous + 1) & (df.rally_length == 4)].point_id.unique())
        weak_count = weak_count + list(df_returns[df_returns['sel_player_shot_distance_moved'] > 5].point_id.unique()) + pushed_back
        weak_count = len(list(set(weak_count)))

        if total == 0:
            return 0, 0
        percent = weak_count / total
        return percent, total
    
    def weak_serve_plus1(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_returns = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 4) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        weak_count = list(df_returns[(df_returns.PLAYER_WIN_NAME != df_returns.server_name) & (df.rally_length == 4)].point_id.unique())
        weak_count = weak_count + list(df_returns[df_returns['sel_player_shot_distance_moved'] > 5].point_id.unique())
        weak_count = len(list(set(weak_count)))

        if total == 0:
            return 0, 0
        percent = weak_count / total
        return percent, total

    def second_serve_weak_returns(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_not_in_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 0)
                       & (df.serve_number == 2)]
        df_weak_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df.PLAYER_WIN_NAME == df.server_name) & (df.rally_length <= 4)]
        
        total = len(df_serves)
        weak_returns = df_not_in_returns.point_id.nunique() + df_weak_returns.point_id.nunique()
        if total == 0:
            return 0, 0
        percent = weak_returns / total
        return percent, total
    
    def second_serve_attacked(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_attacked = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df.PLAYER_WIN_NAME != df.server_name) & (df.rally_length <= 3)]
        df_moved = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df['sel_player_shot_distance_moved'] > 5)]
        
        attacked = len(set(list(df_moved.point_id.unique()) + list(df_attacked.point_id.unique())))
        
        total = len(df_serves)
       
        if total == 0:
            return 0, 0
        percent = attacked / total
        return percent, total


    def win_percent_second_serve(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_df = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 0)
                       & (df.serve_number == 2)]
        total = len(df_serves) + len(df_df)
        win_count = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        percent = win_count / total
        return percent, total

    def win_percent_second_serve_ad_wide(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df.serve_direction == 'W') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        win_count = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        percent = win_count / total
        return percent, total
    
    def win_percent_first_serve(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        win_count = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        percent = win_count / total
        return percent, total


    

    def win_percent_first_serve_pressure(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[df_serves.is_pressure_point == 1]
        total = len(df_serves)
        win_count = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win_count / total, total

    def win_percent_first_serve_break(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[df_serves['is_break_point'] == 1]
        total = len(df_serves)
        win_count = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        # need to avoid errors in case there were no pressure points
        if total == 0:
            return 0, 0
        return win_count / total, total

    def percent_of_first_serves_within_04m_of_sideline(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        close_to_sideline = len(df_serves[df_serves['distance_from_side_or_center_line'] <= 0.4])
        # need to avoid errors in case there were no pressure points
        if total == 0:
            return 0, 0
        return close_to_sideline / total, total

    def percent_of_first_serves_within_04m_of_sideline_pressure(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[df_serves.is_pressure_point == 1]
        total = len(df_serves)
        close_to_sideline = len(df_serves[df_serves['distance_from_side_or_center_line'] <= 0.4])
        # need to avoid errors in case there were no pressure points
        if total == 0:
            return 0, 0
        return close_to_sideline / total, total

    def percent_of_first_serves_within_04m_of_sideline_break(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[df_serves['is_break_point'] == 1]
        total = len(df_serves)
        close_to_sideline = len(df_serves[df_serves['distance_from_side_or_center_line'] <= 0.4])
        # need to avoid errors in case there were no pressure points
        if total == 0:
            return 0, 0
        return close_to_sideline / total, total

    #  average first serve speed for an in serve
    def first_serve_speed(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    #  Is this the same as first serve speed?
    def first_serve_speed_before_bounce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_serve_speed_after_bounce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        return df_serves['speed_after_bounce'].mean(), total

    def first_serve_speed_deuce_w(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'deuce') & (df_serves.serve_direction == 'W')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_serve_speed_deuce_t(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'deuce') & (df_serves.serve_direction == 'T')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_serve_speed_ad_w(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'ad') & (df_serves.serve_direction == 'W')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_serve_speed_ad_t(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'ad') & (df_serves.serve_direction == 'T')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_serve_speed_decrease_break(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        avg_speed = df_serves['SPEED'].mean()
        df_serves = df_serves[df_serves['is_break_point'] == 1]
        total = len(df_serves)
        return avg_speed - df_serves['SPEED'].mean(), total

    def first_serve_speed_decrease_break_deuce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce')]
        avg_speed = df_serves['SPEED'].mean()
        df_serves = df_serves[df_serves['is_break_point'] == 1]
        total = len(df_serves)
        return avg_speed - df_serves['SPEED'].mean(), total

    def first_serve_speed_decrease_break_ad(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'ad')]
        avg_speed = df_serves['SPEED'].mean()
        df_serves = df_serves[df_serves['is_break_point'] == 1]
        total = len(df_serves)
        return avg_speed - df_serves['SPEED'].mean(), total

    def avg_return_speed_opponent(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)]
        total = len(df_returns)
        return df_returns['SPEED'].mean(), total
    
    def percent_unreturned_first_serves(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.PLAYER_WIN_NAME == df.PLAYER_HIT)]
        total = len(df_serves)
        df_serves = df_serves[(df_serves.rally_length == 1) | ((df_serves.rally_length == 2) & (df_serves.PLAYER_WIN_NAME == df_serves.server_name) )]
        aces = len(df_serves)
        if total == 0:
            return 0, 0
        return aces/total, total

    def percent_first_serves_won_in_two_to_four_shots(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        df_serves = df_serves[(df_serves.rally_length >= 2) & (df_serves.rally_length <= 4)
                              & (df_serves.PLAYER_WIN_NAME == Calculations.PLAYER_NAME)]
        points_won_in_two_to_four_shots = len(df_serves)
        if total == 0:
            return 0, 0
        return points_won_in_two_to_four_shots/total, total

    def first_serve_in_percentage(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1)
                       & (df.serve_number == 1)]
        total = len(df_serves)
        df_serves = df_serves[df_serves.is_shot_in == 1]
        in_serves = len(df_serves)
        if total == 0:
            return 0, 0
        return in_serves/total, total

    def first_serve_in_percentage_pressure(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.serve_number == 1) &
                       (df['is_pressure_point'] == 1)]
        total = len(df_serves)
        in_serves = len(df_serves[df_serves.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return in_serves/total, total

    def first_serve_in_percentage_break(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.serve_number == 1) &
                       (df['is_break_point'] == 1)]
        total = len(df_serves)
        in_serves = len(df_serves[df_serves.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return in_serves/total, total

    def first_serve_win_percentage_bh_deuce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 1) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def first_serve_win_percentage_fh_deuce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 1) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def first_serve_win_percentage_bh_ad(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 1) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def first_serve_win_percentage_fh_ad(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 1) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def win_percent_first_serve_rally_five_to_eight(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_rally_5_to_8 = df_serves[(df_serves.rally_length >= 5) & (df_serves.rally_length <= 8)]
        total = len(df_rally_5_to_8)
        wins = len(df_rally_5_to_8[df_rally_5_to_8['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])

        if total == 0:
            return 0, 0
        return wins / total, total

    def win_percent_first_serve_rally_nine_plus(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        # Filter shots with rally lengths of 9 or more
        df_rally_9_plus = df_serves[df_serves.rally_length >= 9]
        total = len(df_rally_9_plus)
        wins = len(df_rally_9_plus[df_rally_9_plus['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])

        if total == 0:
            return 0, 0
        return wins / total, total

    def percent_serve_points_won(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])

        if total == 0:
            return 0, 0
        return wins / total, total

    def percent_aces_per_serve_points(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)]
        total = len(df_serves)

        # Filter shots that are aces (rally length is 1 and rally ending shot is Winner)
        df_aces = df_serves[(df_serves.rally_length == 1) & (df_serves['PLAYER_WIN_NAME'] == df_serves['server_name'])]
        aces = len(df_aces)

        if total == 0:
            return 0, 0
        return aces / total, total
    

    def avg_points_won_per_serve_game(self, df):
        next_row_is_different_server = df['server_name'] != df['server_name'].shift(-1)
        is_last_row = df.index == df.index[-1]
        df_serve_games = df[(next_row_is_different_server | is_last_row) & (df.server_name == Calculations.PLAYER_NAME)]
        total = len(df_serve_games)

        df_won_service_points = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) &
                                   (df.is_shot_in == 1) & (df['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME)]
        points_won = len(df_won_service_points)
        if total == 0:
            return 0, 0
        avg_points_won = points_won / total
        return avg_points_won, total

    def avg_points_lost_per_serve_game(self, df):
        next_row_is_different_server = df['server_name'] != df['server_name'].shift(-1)
        is_last_row = df.index == df.index[-1]
        df_serve_games = df[(next_row_is_different_server | is_last_row) & (df.server_name == Calculations.PLAYER_NAME)]
        total = len(df_serve_games)

        df_lost_service_points = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) &
                                    (df['PLAYER_WIN_NAME'] != Calculations.PLAYER_NAME)]
        points_won = len(df_lost_service_points)
        if total == 0:
            return 0, 0
        avg_points_won = points_won / total
        return avg_points_won, total

    def serve_hold_rate(self, df):
        # Step 1: Count the total number of serve games played by the player
        next_row_is_different_server = df['server_name'] != df['server_name'].shift(-1)
        is_last_row = df.index == df.index[-1]
        df_serve_games = df[(next_row_is_different_server | is_last_row) & (df.server_name == Calculations.PLAYER_NAME)]
        total = len(df_serve_games)

        if total == 0:
            return 0, 0

        # Step 2: Count the number of serve games won by the player
        df_won_serve_games = df_serve_games[df_serve_games['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME]
        won_serve_games = len(df_won_serve_games)

        # Step 3: Calculate the percentage of serve games won
        serve_hold_rate = (won_serve_games / total)
        return serve_hold_rate, total

    def serve_win_percentage_when_return_in(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        df_returns = df[serves].shift(-1)
        df_serves_returns = df_returns[df_returns.is_shot_in == 1]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_return_fast(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        df_returns = df[serves].shift(-1)
        df_serves_returns = df_returns[(df_returns.is_shot_in == 1) & (df_returns['SPEED'] >= Calculations.FAST)]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_return_deep(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        returns = serves.shift(-1)

        # REVISIT WHEN WE GET DEEP DEFINITION
        serves_returns = returns & (df.is_shot_in == 1) & (df.REBOUND_X_abs >= Calculations.DEEP_BORDER)
        df_serves_returns = df[serves_returns]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_return_middle(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        returns = serves.shift(-1)

        # REVISIT WHEN WE GET MIDDLE DEFINITION
        serves_returns = returns & (df.is_shot_in == 1) & (df.REBOUND_X_abs >= Calculations.SHORT_BORDER) & (df.REBOUND_X_abs <= Calculations.DEEP_BORDER)
        df_serves_returns = df[serves_returns]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_return_short(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        df_returns = df[serves].shift(-1)

        # REVISIT WHEN WE GET SHORT DEFINITION
        df_serves_returns = df_returns[(df_returns.is_shot_in == 1) &
                                       (df_returns.REBOUND_X_abs <= Calculations.SHORT_BORDER)]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_returner_stands_in(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        returns = serves.shift(-1)

        # REVISIT WHEN WE GET IN DEFINITION
        serves_returns = returns & (df.opponent_location_at_shot_x_abs <= Calculations.STANDS_IN)
        df_serves_returns = df[serves_returns]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_returner_stands_back(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        df_returns = df[serves].shift(-1)

        # REVISIT WHEN WE GET BACK DEFINITION
        df_serves_returns = df_returns[df_returns.opponent_location_at_shot_x_abs >= Calculations.STANDS_BACK]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def serve_win_percentage_when_returner_stands_far_back(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1)
        df_returns = df[serves].shift(-1)

        # REVISIT WHEN WE GET FAR BACK DEFINITION
        df_serves_returns = df_returns[df_returns.opponent_location_at_shot_x_abs >= Calculations.STANDS_FAR_BACK]
        total = len(df_serves_returns)
        if total == 0:
            return 0, 0
        win_count = len(df_serves_returns[df_serves_returns['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        percent = win_count / total
        return percent, total

    def percent_serve_pone_deuce_after_deuce_returned_middle(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1) & (df.serve_deuce_or_ad == 'deuce')
        serves = serves.shift(-1)


        # DEFINE MIDDLE AND DEUCE
        returns = (serves & (df.is_shot_in == 1) & (df.CONTACT_Y_mirrored >= Calculations.DEUCE_THIRD_COORDS) &
                   (df.CONTACT_Y_mirrored <= Calculations.AD_THIRD_COORDS))
        serves_plus_one = returns.shift(-1)
        serves_plus_one = serves_plus_one & (df.REBOUND_Y_mirrored < Calculations.MIDDLE_Y) & (df.is_shot_in == 1)

        df_serves_plus_one = df[serves_plus_one]
        total = len(df[returns])
        if total == 0:
            return 0, 0
        count = len(df_serves_plus_one)
        percent = count / total
        return percent, total

    def percent_serve_pone_ad_after_ad_returned_middle(self, df):
        serves = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1) \
                 & (df.rally_length > 1) & (df.serve_deuce_or_ad == 'ad')
        returns = serves.shift(-1)

        # DEFINE MIDDLE AND DEUCE
        returns = returns & (df.is_shot_in == 1) & (df.CONTACT_Y_mirrored >= Calculations.DEUCE_THIRD_COORDS) & \
                  (df.CONTACT_Y_mirrored <= Calculations.AD_THIRD_COORDS)
        serves_plus_one = returns.shift(-1)
        serves_plus_one = serves_plus_one & (df.REBOUND_Y_mirrored > Calculations.MIDDLE_Y) & (df.is_shot_in == 1)

        df_serves_plus_one = df[serves_plus_one]
        total = len(df[returns])
        if total == 0:
            return 0, 0
        count = len(df_serves_plus_one)
        percent = count / total
        return percent, total

    def percent_serve_pone_runaround_fh(self, df):
        df_serve_p_one = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) &
                            (df.server_name == Calculations.PLAYER_NAME) & (df.is_shot_in == 1)]
        total = len(df_serve_p_one)
        # UPDATE WITH AD COORDS
        runarounds = len(df_serve_p_one[(df_serve_p_one.shot_type == 'F') &
                                        (df_serve_p_one.CONTACT_Y_mirrored > Calculations.MIDDLE_Y)])
        if total == 0:
            return 0, 0
        return runarounds / total, total

    def percent_serve_pone_runaround_inside_in_fh(self, df):
        # UPDATE WITH AD COORDS
        df_serve_p_one = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) &
                            (df.server_name == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) &
                            (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > Calculations.MIDDLE_Y)]
        total = len(df_serve_p_one)
        # UPDATE WITH DEUCE COORDS
        inside_in = len(df_serve_p_one[df_serve_p_one.REBOUND_Y_mirrored < Calculations.MIDDLE_Y])
        if total == 0:
            return 0, 0
        return inside_in / total, total

    def win_percent_ad_serve_pone_runaround_inside_in_fh(self, df):
        df_serve_p_one = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) &
                            (df.server_name == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) &
                            (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > Calculations.MIDDLE_Y) &
                            (df.serve_deuce_or_ad == 'ad') & (df.REBOUND_Y_mirrored < Calculations.MIDDLE_Y)]
        total = len(df_serve_p_one)
        # UPDATE WITH DEUCE COORDS
        win = len(df_serve_p_one[df_serve_p_one.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def win_percent_deuce_serve_pone_runaround_inside_in_fh(self, df):
        df_serve_p_one = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3) &
                            (df.server_name == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) &
                            (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > Calculations.MIDDLE_Y) &
                            (df.serve_deuce_or_ad == 'deuce') & (df.REBOUND_Y_mirrored < Calculations.MIDDLE_Y)]
        total = len(df_serve_p_one)
        # UPDATE WITH DEUCE COORDS
        win = len(df_serve_p_one[df_serve_p_one.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def percent_returns_line_and_cross(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)]
        total = len(df_returns)
        # ADD MIDDLE
        df_not_middle_returns = df_returns[(df_returns.REBOUND_Y_mirrored > Calculations.AD_THIRD_COORDS) |
                                           (df_returns.REBOUND_Y < Calculations.DEUCE_THIRD_COORDS)]
        not_middle = len(df_not_middle_returns)
        if total == 0:
            return 0, 0
        return not_middle / total, total

    def win_percent_first_return_higher_over_net(self, df):
        # ADD HIGHER
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.ON_NET_Z >= Calculations.HIGHER_OVER_NET)]
        total = len(df_returns)
        won = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return won / total, total

    def win_percent_first_return_lower_over_net(self, df):
        # ADD LOWER
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.ON_NET_Z <= Calculations.LOWER_OVER_NET)]
        total = len(df_returns)
        won = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return won / total, total

    def percent_first_serve_slice_deuce_w(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce') & (df.serve_direction == 'W')]
        total = len(df_serves)
        slices = len(df_serves[df_serves['SPEED'] == Calculations.SLICE])
        if total == 0:
            return 0, 0
        return slices / total, total

    def percent_first_serve_slice_ad_t(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'ad') & (df.serve_direction == 'T')]
        total = len(df_serves)
        slices = len(df_serves[df_serves['SPEED'] == Calculations.SLICE])
        if total == 0:
            return 0, 0
        return slices / total, total

    def second_serve_win_percentage_pone_bh_deuce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 2) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_pone_fh_deuce(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 2) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_pone_bh_ad(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 2) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_pone_fh_ad(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 3)
                       & (df.serve_number == 2) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def win_percent_second_serve_rally_under_five(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_rally_5 = df_serves[df_serves.rally_length < 5]
        total = len(df_rally_5)
        wins = len(df_rally_5[df_rally_5['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])

        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_ad_wide_percent_dtl_return(self, df):
        df_serve_ad_wide = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) &
                            (df.serve_number == 2) & (df.is_shot_in == 1) &
                            (df.serve_deuce_or_ad == 'ad') & (df.serve_direction == 'W')]
        total = len(df_serve_ad_wide)
        # UPDATE WITH DEUCE COORDS
        dtl = len(df_serve_ad_wide[df_serve_ad_wide.REBOUND_Y_mirrored_next < Calculations.DEUCE_THIRD_COORDS])
        if total == 0:
            return 0, 0
        return dtl / total, total

    def second_serve_win_percentage_bh_deuce(self, df):
        df_serves = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 2)
                       & (df.serve_number == 2) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_fh_deuce(self, df):
        df_serves = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 2)
                       & (df.serve_number == 2) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'deuce')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_bh_ad(self, df):
        df_serves = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 2)
                       & (df.serve_number == 2) & (df.shot_type == 'B') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_win_percentage_fh_ad(self, df):
        df_serves = df[(df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 2)
                       & (df.serve_number == 2) & (df.shot_type == 'F') & (df.serve_deuce_or_ad == 'ad')]
        total = len(df_serves)
        wins = len(df_serves[df_serves['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_serve_speed_deuce_w(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'deuce') & (df_serves.serve_direction == 'W')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def second_serve_speed_deuce_t(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'deuce') & (df_serves.serve_direction == 'T')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def second_serve_speed_ad_w(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'ad') & (df_serves.serve_direction == 'W')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def second_serve_speed_ad_t(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_serves = df_serves[(df_serves.serve_deuce_or_ad == 'ad') & (df_serves.serve_direction == 'T')]
        total = len(df_serves)
        return df_serves['SPEED'].mean(), total

    def first_return_depth(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        depth = df_returns.REBOUND_X_abs.mean()
        if total == 0:
            return 0, 0
        return depth, total

    def first_return_percent_deep(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.REBOUND_X_abs >= Calculations.DEEP_BORDER])
        if total == 0:
            return 0, 0
        return deep / total, total
    
    def first_return_percent_short(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.REBOUND_X_abs <= Calculations.SHORT_BORDER])
        if total == 0:
            return 0, 0
        return deep / total, total

    def first_return_win_percent_deep(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.REBOUND_X_abs >= Calculations.DEEP_BORDER)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def first_return_percent_low(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.ON_NET_Z <= Calculations.LOWER_OVER_NET])
        if total == 0:
            return 0, 0
        return deep / total, total
    
    def first_return_percent_angled(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[(df_returns.CONTACT_Y_mirrored_next.abs() >= 5.3) & (df.CONTACT_Y_mirrored*df.REBOUND_Y_mirrored > 0)]) # cross angled return
        if total == 0:
            return 0, 0
        return deep / total, total
    
    def second_return_percent_angled(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_returns)
        deep = len(df_returns[(df_returns.CONTACT_Y_mirrored_next.abs() >= 5.3) & (df.CONTACT_Y_mirrored*df.REBOUND_Y_mirrored > 0)]) # cross angled return
        if total == 0:
            return 0, 0
        return deep / total, total

    def first_return_percent_fast(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.SPEED >= 118])
        if total == 0:
            return 0, 0
        return deep / total, total
    
    def first_return_percent_high(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.ON_NET_Z >= Calculations.HIGHER_OVER_NET])
        if total == 0:
            return 0, 0
        return deep / total, total
    def first_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 1)]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def first_return_in_percentage_pressure(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 1) & (df.is_pressure_point == 1)]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def first_return_in_percentage_break(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 1) & (df.is_break_point == 1)]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def first_bh_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 1) & (df.shot_type == 'B')]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def first_fh_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 1) & (df.shot_type == 'F')]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def second_bh_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 2) & (df.shot_type == 'B')]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def second_fh_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 2) & (df.shot_type == 'F')]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total
    
    def second_return_in_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) 
                       & (df.serve_number == 2)]
        total = len(df_returns)
        inreturn = len(df_returns[df_returns.is_shot_in == 1])
        if total == 0:
            return 0, 0
        return inreturn / total, total

    def first_return_win_percent_low(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1) & (df.ON_NET_Z <= Calculations.LOWER_OVER_NET)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def first_return_percent_to_bh(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 1)
        df_returns = df[returns]
        total = len(df_returns)
        pones = df_returns.shift(-1)
        df_bh = pones[pones.shot_type == 'B']
        if total == 0:
            return 0, 0
        return len(df_bh) / total, total

    def first_return_win_percent_to_bh(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 1)
        df_returns = df[returns]
        pones = df_returns.shift(-1)
        df_bh = pones[pones.shot_type == 'B']
        total = len(df_bh)
        win = len(df_bh[df_bh.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def first_return_percent_line(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 1)
        df_returns = df[returns]
        total = len(df_returns)
        pones = df_returns.shift(-1)
        df_line = pones[pones.CONTACT_Y_mirrored * pones.REBOUND_Y_mirrored < 0]
        if total == 0:
            return 0, 0
        return len(df_line) / total, total

    def first_return_win_percent_line(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 1)
        df_returns = df[returns]
        pones = df_returns.shift(-1)
        df_line = pones[pones.CONTACT_Y_mirrored * pones.REBOUND_Y_mirrored < 0]
        total = len(df_line)
        win = len(df_line[df_line.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def first_return_win_under_five(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_rally_under_5 = df_serves[(df_serves.rally_length <= 5)]
        total = len(df_rally_under_5)
        wins = len(df_rally_under_5[df_rally_under_5['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total
    
    def first_return_defeat_under_five(self, df): # actually it's those that extended over five
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_rally_under_5 = df_serves[(df_serves.rally_length >= 5)]
        total = len(df_serves)
        if total == 0:
            return 0, 0
        return round(len(df_rally_under_5) / total, 2), total
    
    def first_return_extended_or_won(self, df): # actually it's those that extended over five
        df_serves = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_rally_under_5 = df_serves[(df_serves.rally_length > 5) | (df_serves.rally_length.between(2, 4) & (df_serves.PLAYER_WIN_NAME == Calculations.PLAYER_NAME))]
        total = len(df_serves)
        if total == 0:
            return 0, 0
        return round(len(df_rally_under_5) / total, 2), total

    def second_return_extended_or_won(self, df): # actually it's those that extended over five
        df_serves = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_rally_under_5 = df_serves[(df_serves.rally_length > 5) | (df_serves.rally_length.between(2, 4) & (df_serves.PLAYER_WIN_NAME == Calculations.PLAYER_NAME))]
        total = len(df_serves)
        if total == 0:
            return 0, 0
        return round(len(df_rally_under_5) / total, 2), total
    
    def second_return_aggressive(self, df): # actually it's those that extended over five
        df_serves = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_aggresive = df_serves[(df_serves.rally_length.between(2, 5) & (df_serves.PLAYER_WIN_NAME == Calculations.PLAYER_NAME))]
        total = len(df_serves)
        if total == 0:
            return 0, 0
        return round(len(df_aggresive) / total, 2), total

    def second_return_killer(self, df): # actually it's those that extended over five
        df_serves = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_aggresive = df_serves[(df_serves.rally_length.between(2, 3) & (df_serves.PLAYER_WIN_NAME == Calculations.PLAYER_NAME))]
        total = len(df_serves)
        if total == 0:
            return 0, 0
        return round(len(df_aggresive) / total, 2), total

    def first_return_win_over_five(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 1)]
        df_rally_under_5 = df_serves[(df_serves.rally_length > 5)]
        total = len(df_rally_under_5)
        wins = len(df_rally_under_5[df_rally_under_5['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def first_return_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1)]
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_deuce_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    

    def first_return_ad_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'ad')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_deuce_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_deuce_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_ad_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def first_return_ad_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_deuce_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'deuce')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    

    def second_return_ad_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'ad')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_deuce_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_deuce_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_ad_fh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'F')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_return_ad_bh_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.serve_deuce_or_ad == 'deuce') & (df.shot_type == 'B')]
        
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total

    def first_return_win_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                        & (df.serve_number == 1)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME != df_returns.server_name])
        if total == 0:
            return 0, 0
        return win / total, total

    def first_return_win_percentage_break(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.is_break_point == 1)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME != df_returns.server_name])
        if total == 0:
            return 0, 0
        return win / total, total
    
    def first_return_win_percentage_pressure(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                        & (df.serve_number == 1) & (df.is_pressure_point == 1)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME != df_returns.server_name])
        if total == 0:
            return 0, 0
        return win / total, total

    def second_return_depth(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_returns)
        depth = df_returns.REBOUND_X_abs.mean()
        if total == 0:
            return 0, 0
        return depth, total

    def second_return_percent_deep(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.REBOUND_X_abs >= Calculations.DEEP_BORDER])
        if total == 0:
            return 0, 0
        return deep / total, total

    def second_return_win_percent_deep(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df.REBOUND_X_abs >= Calculations.DEEP_BORDER)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def second_return_percent_low(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        total = len(df_returns)
        deep = len(df_returns[df_returns.ON_NET_Z <= Calculations.LOWER_OVER_NET])
        if total == 0:
            return 0, 0
        return deep / total, total

    def second_return_win_percent_low(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2) & (df.ON_NET_Z <= Calculations.LOWER_OVER_NET)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def second_return_percent_to_bh(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 2)
        df_returns = df[returns]
        total = len(df_returns)
        pones = df_returns.shift(-1)
        df_bh = pones[pones.shot_type == 'B']
        if total == 0:
            return 0, 0
        return len(df_bh) / total, total

    def second_return_win_percent_to_bh(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 2)
        df_returns = df[returns]
        pones = df_returns.shift(-1)
        df_bh = pones[pones.shot_type == 'B']
        total = len(df_bh)
        win = len(df_bh[df_bh.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def second_return_percent_line(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 2)
        df_returns = df[returns]
        total = len(df_returns)
        pones = df_returns.shift(-1)
        df_line = pones[pones.CONTACT_Y_mirrored * pones.REBOUND_Y_mirrored < 0]
        if total == 0:
            return 0, 0
        return len(df_line) / total, total

    def second_return_win_percent_line(self, df):
        returns = (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1) \
                  & (df.serve_number == 2)
        df_returns = df[returns]
        pones = df_returns.shift(-1)
        df_line = pones[pones.CONTACT_Y_mirrored * pones.REBOUND_Y_mirrored < 0]
        total = len(df_line)
        win = len(df_line[df_line.PLAYER_WIN_NAME == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return win / total, total

    def second_return_win_under_five(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_rally_under_5 = df_serves[(df_serves.rally_length <= 5)]
        total = len(df_rally_under_5)
        wins = len(df_rally_under_5[df_rally_under_5['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_return_win_over_five(self, df):
        df_serves = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                       & (df.serve_number == 2)]
        df_rally_under_5 = df_serves[(df_serves.rally_length > 5)]
        total = len(df_rally_under_5)
        wins = len(df_rally_under_5[df_rally_under_5['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME])
        if total == 0:
            return 0, 0
        return wins / total, total

    def second_return_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2)]
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_bh_return_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.shot_type == 'B')]
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total
    
    def second_fh_return_speed(self, df):
        df_returns = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.is_shot_in == 1)
                        & (df.serve_number == 2) & (df.shot_type == 'F')]
        total = len(df_returns)
        depth = df_returns.SPEED.mean()
        if total == 0:
            return 0, 0
        return depth, total

    def second_return_win_percentage(self, df):
        df_returns = df[(df.PLAYER_HIT != Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.is_shot_in == 1)
                        & (df.serve_number == 2)]
        total = len(df_returns)
        win = len(df_returns[df_returns.PLAYER_WIN_NAME != df_returns.server_name])
        if total == 0:
            return 0, 0
        return win / total, total

    def avg_forehand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
            

    def avg_forehand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
                

    def avg_backhand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total

    def avg_backhand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total

    def avg_forehand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
            

    def avg_forehand_dtl_depth(self, df, leftie=False):
        
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F')]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
                

    def avg_backhand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total

    def avg_backhand_dtl_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B')]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        
    def avg_backhand_spin(self, df, leftie=False):
        df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.spinRPM > 0)]
        total = len(df_bh)
        return df_bh['spinRPM'].mean(), total

    def avg_forehand_spin(self, df, leftie=False):
        df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.spinRPM > 0)]
        total = len(df_fh)
        return df_fh['spinRPM'].mean(), total

    def avg_deuce_forehand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
            

    def avg_deuce_forehand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
                

    def avg_deuce_backhand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total

    def avg_deuce_backhand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total

    def avg_deuce_forehand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
            

    def avg_deuce_forehand_dtl_depth(self, df, leftie=False):
        
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
                

    def avg_deuce_backhand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total

    def avg_deuce_backhand_dtl_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        
    def avg_deuce_backhand_spin(self, df, leftie=False):
        df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored < -2) & (df.spinRPM > 0)]
        total = len(df_bh)
        return df_bh['spinRPM'].mean(), total

    def avg_deuce_forehand_spin(self, df, leftie=False):
        df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored < -2) & (df.spinRPM > 0)]
        total = len(df_fh)
        return df_fh['spinRPM'].mean(), total
    
    def avg_ad_forehand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
            

    def avg_ad_forehand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
                

    def avg_ad_backhand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total

    def avg_ad_backhand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total

    def avg_ad_forehand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
            

    def avg_ad_forehand_dtl_depth(self, df, leftie=False):
        
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2)]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
                

    def avg_ad_backhand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total

    def avg_ad_backhand_dtl_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2)]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        
    def avg_ad_backhand_spin(self, df, leftie=False):
        df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored > 2) & (df.spinRPM > 0)]
        total = len(df_bh)
        return df_bh['spinRPM'].mean(), total

    def avg_ad_forehand_spin(self, df, leftie=False):
        df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored > 2) & (df.spinRPM > 0)]
        total = len(df_fh)
        return df_fh['spinRPM'].mean(), total
    

    def avg_middle_forehand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['SPEED'].mean(), total
            

    def avg_middle_forehand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['SPEED'].mean(), total
                

    def avg_middle_backhand_cc_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['SPEED'].mean(), total

    def avg_middle_backhand_dtl_speed(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['SPEED'].mean(), total

    def avg_middle_forehand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9) ]
            total = len(df_fh_cc)
            return df_fh_cc['REBOUND_X_abs'].mean(), total
            

    def avg_middle_forehand_dtl_depth(self, df, leftie=False):
        
        if not leftie:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_fh['CONTACT_Y_mirrored'] < 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_fh['CONTACT_Y_mirrored'] > 0) & (df_fh['CONTACT_X_abs'] > 9)]
            total = len(df_fh_dtl)
            return df_fh_dtl['REBOUND_X_abs'].mean(), total
                

    def avg_middle_backhand_cc_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] > 1)  & (df_bh['CONTACT_Y_mirrored'] > 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_cc = df_bh[(df_bh['shot_no'] > 2) & (df_bh['REBOUND_Y_mirrored'] < -1)  & (df_bh['CONTACT_Y_mirrored'] < 0) & 
                        (df_bh['CONTACT_X_abs'] > 9) ]
            total = len(df_bh_cc)
            return df_bh_cc['REBOUND_X_abs'].mean(), total

    def avg_middle_backhand_dtl_depth(self, df, leftie=False):
        if not leftie:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] < -1)  & 
                        (df_bh['CONTACT_Y_mirrored'] > 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        else:
            df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2))]
            df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored'] > 1)  & 
                        (df_bh['CONTACT_Y_mirrored'] < 0) & (df_bh['CONTACT_X_abs'] > 9)]
            total = len(df_bh_dtl)
            return df_bh_dtl['REBOUND_X_abs'].mean(), total
        
    def avg_middle_backhand_spin(self, df, leftie=False):
        df_bh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'B') & (df.CONTACT_Y_mirrored.between(-2, 2)) & (df.spinRPM > 0)]
        total = len(df_bh)
        return df_bh['spinRPM'].mean(), total

    def avg_middle_forehand_spin(self, df, leftie=False):
        df_fh = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no > 3) & (df.is_shot_in == 1) & (df.shot_type == 'F') & (df.CONTACT_Y_mirrored.between(-2, 2)) & (df.spinRPM > 0)]
        total = len(df_fh)
        return df_fh['spinRPM'].mean(), total

    def passing_bh_win_perc(self, df):
        #our player passing
        df_passing = df[(df['PLAYER_HIT'] == Calculations.PLAYER_NAME) & (df['opponent_location_at_shot_x_abs'] < 8) & (df['CONTACT_X_abs'] > 8) & (df['sel_player_location_at_shot_x_abs'] > 9) &
                        (df['shot_no'] > 2) & (df['is_shot_in'].shift(1) == 1) & (df['opponent_change_of_possition_beginning_end_x'].shift(1) == 'forward') & (df['ON_NET_Z'] < 3) & (df['CONTACT_X_abs'].shift(1) > 8)]
        df_passing_bh = df_passing[df_passing['shot_type'] == 'B']
        won_points = df_passing_bh[df_passing_bh['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_passing_bh.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points
    

    def passing_fh_win_perc(self, df):
        #our player passing
        df_passing = df[(df['PLAYER_HIT'] == Calculations.PLAYER_NAME) & (df['opponent_location_at_shot_x_abs'] < 8) & (df['CONTACT_X_abs'] > 8) & (df['sel_player_location_at_shot_x_abs'] > 9) &
                        (df['shot_no'] > 2) & (df['is_shot_in'].shift(1) == 1) & (df['opponent_change_of_possition_beginning_end_x'].shift(1) == 'forward') & (df['ON_NET_Z'] < 3) & (df['CONTACT_X_abs'].shift(1) > 8)]
        df_passing_bh = df_passing[df_passing['shot_type'] == 'F']
        won_points = df_passing_bh[df_passing_bh['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_passing_bh.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points

    def approach_win_perc(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
             &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)

        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points
    
    def approach_win_perc_count(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
             &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)

        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, df.match_id.nunique()
        return total_points, df.match_id.nunique()

    def approach_fh_win_perc(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
             &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_type == 'F']
        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points

    def approach_bh_win_perc(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_type == 'B']
        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points

    def approach_to_fh_win_perc(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_type_next == 'F']
        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points

    def approach_to_bh_win_perc(self, df):
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != Calculations.PLAYER_NAME) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == Calculations.PLAYER_NAME)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_type_next == 'B']
        won_points = df_approach[df_approach['PLAYER_WIN_NAME'] == Calculations.PLAYER_NAME].point_id.nunique()
        total_points = df_approach.point_id.nunique()
        if total_points == 0:
            return 0, 0
        return round(won_points / total_points, 2), total_points
    
    def fh_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_ue = fh_shots[(fh_shots.is_last_shot == 1) & (fh_shots.is_shot_in == 0) & (fh_shots['Rally ending shot'] == 'Unforced Error')]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_ue) / total * 100, 2), total

    def fh_consistency_new(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def fh_errors(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_out = fh_shots[fh_shots.is_shot_in == 0]
        
        return len(fh_shots_out), df.match_id.nunique()
    
    def bh_errors(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'B']
        fh_shots_out = fh_shots[fh_shots.is_shot_in == 0]
        
        return len(fh_shots_out), df.match_id.nunique()

    def bh_consistency_new(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'B']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def bh_consistency(self, df):
        # Consistency
        df_shots     = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        bh_shots = df_shots[df_shots.shot_type == 'B']
        bh_shots_ue = bh_shots[(bh_shots.is_last_shot == 1) & (bh_shots.is_shot_in == 0) & (bh_shots['Rally ending shot'] == 'Unforced Error')]
        total = len(bh_shots)
        if total == 0:
            return 0, 0
        return round(len(bh_shots_ue) / total * 100, 2), total
    
    def fh_middle_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored.between(-2, 2))]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def fh_ad_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored > 2)]
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def fh_deuce_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored < -2)]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def bh_ad_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored > 2)]
        
        fh_shots = df_shots[df_shots.shot_type == 'B']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def bh_deuce_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored < -2)]
        
        fh_shots = df_shots[df_shots.shot_type == 'B']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def bh_middle_consistency(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (df.CONTACT_Y_mirrored.between(-2, 2))]
        
        fh_shots = df_shots[df_shots.shot_type == 'B']
        fh_shots_in = fh_shots[fh_shots.is_shot_in == 1]
        total = len(fh_shots)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_in) / total * 100, 2), total
    
    def bh_consistency(self, df):
        # Consistency
        df_shots     = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        bh_shots = df_shots[df_shots.shot_type == 'B']
        bh_shots_ue = bh_shots[(bh_shots.is_last_shot == 1) & (bh_shots.is_shot_in == 0) & (bh_shots['Rally ending shot'] == 'Unforced Error')]
        total = len(bh_shots)
        if total == 0:
            return 0, 0
        return round(len(bh_shots_ue) / total * 100, 2), total
    

    def fh_consistency_winners(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        fh_shots = df_shots[df_shots.shot_type == 'F']
        fh_shots_ue = fh_shots[(fh_shots.is_last_shot == 1) & (fh_shots.is_shot_in == 0) & (fh_shots['Rally ending shot'] == 'Unforced Error')]
        fh_shots_winners = fh_shots[(fh_shots.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (fh_shots.rally_length - 1  <= fh_shots.shot_no)  & (fh_shots.is_shot_in == 1) & (fh_shots['Rally ending shot'].isin(['Winner', 'Forcing Error']))]
        total = len(fh_shots_ue) + len(fh_shots_winners)
        if total == 0:
            return 0, 0
        return round(len(fh_shots_ue) / total * 100, 2), total
    
    def bh_consistency_winners(self, df):
        # Consistency
        df_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4)]
        
        bh_shots = df_shots[df_shots.shot_type == 'B']
        bh_shots_ue = bh_shots[(bh_shots.is_last_shot == 1) & (bh_shots.is_shot_in == 0) & (bh_shots['Rally ending shot'] == 'Unforced Error')]
        bh_shots_winners = bh_shots[(bh_shots.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (bh_shots.rally_length - 1  <= bh_shots.shot_no) & (bh_shots.is_shot_in == 1) & (bh_shots['Rally ending shot'].isin(['Winner', 'Forcing Error']))]
        total = len(bh_shots_ue) + len(bh_shots_winners)
        if total == 0:
            return 0, 0
        return round(len(bh_shots_ue) / total * 100, 2), total
        

    def initiative_first_over_nine(self, df): # actually 7
        # Taking the initiative 
        ds_points = df[(df['PLAYER_HIT'] != Calculations.PLAYER_NAME) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
            (df['sel_player_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['opponent_location_at_shot_x_abs_diff'] > -2)
            & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['opponent_decelerations_window_max'] > -5)].point_id.unique()
        df_gs = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (~df.point_id.isin(ds_points))]

        # 1st serve
        df_gs_1 = df_gs[(df_gs.serve_number == 1) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        df_gs_1_over_nine = df_gs_1[df_gs_1.shot_no >= 7] # TODO -> change everything to over Nine
        over_nine_total = len(df_gs_1_over_nine)
        over_nine_inside_total = len(df_gs_1_over_nine[df_gs_1_over_nine.CONTACT_X_abs <= 11.88])

        # 2nd serve
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        second_initiative_total = len(df_gs_2)
        second_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # 2nd return
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name != Calculations.PLAYER_NAME)]
        second_return_initiative_total = len(df_gs_2)
        second_return_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # over nine
        df_gs_over_nine = df_gs[df_gs.shot_no >= 9]
        over_nine_all_total = len(df_gs_over_nine)
        over_nine_inside_all_total = len(df_gs_over_nine[df_gs_over_nine.CONTACT_X_abs <= 11.88])


        if not over_nine_total:
            initiative_first_over_nine = 0
        else:
            initiative_first_over_nine = round(over_nine_inside_total / over_nine_total * 100, 2)
        
        return initiative_first_over_nine, over_nine_total
    
    def initiative_over_nine(self, df):
        # Taking the initiative 
        ds_points = df[(df['PLAYER_HIT'] != Calculations.PLAYER_NAME) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
            (df['sel_player_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['opponent_location_at_shot_x_abs_diff'] > -2)
            & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['opponent_decelerations_window_max'] > -5)].point_id.unique()
        df_gs = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (~df.point_id.isin(ds_points))]

        # 1st serve
        df_gs_1 = df_gs[(df_gs.serve_number == 1) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        df_gs_1_over_nine = df_gs_1[df_gs_1.shot_no >= 9]
        over_nine_total = len(df_gs_1_over_nine)
        over_nine_inside_total = len(df_gs_1_over_nine[df_gs_1_over_nine.CONTACT_X_abs <= 11.88])

        # 2nd serve
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        second_initiative_total = len(df_gs_2)
        second_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # 2nd return
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name != Calculations.PLAYER_NAME)]
        second_return_initiative_total = len(df_gs_2)
        second_return_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # over nine
        df_gs_over_nine = df_gs[df_gs.shot_no >= 9]
        over_nine_all_total = len(df_gs_over_nine)
        over_nine_inside_all_total = len(df_gs_over_nine[df_gs_over_nine.CONTACT_X_abs <= 11.88])


        if not over_nine_all_total:
            initiative_over_nine = 0
        else:
            initiative_over_nine = round(over_nine_inside_all_total / over_nine_all_total * 100, 2) # TODO: these are all points, not just 1st serve
        
        return initiative_over_nine, over_nine_all_total
    
    def initiative_second(self, df):
        # Taking the initiative 
        ds_points = df[(df['PLAYER_HIT'] != Calculations.PLAYER_NAME) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
            (df['sel_player_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['opponent_location_at_shot_x_abs_diff'] > -2)
            & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['opponent_decelerations_window_max'] > -5)].point_id.unique()
        df_gs = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (~df.point_id.isin(ds_points))]

        # 1st serve
        df_gs_1 = df_gs[(df_gs.serve_number == 1) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        df_gs_1_over_nine = df_gs_1[df_gs_1.shot_no >= 9]
        over_nine_total = len(df_gs_1_over_nine)
        over_nine_inside_total = len(df_gs_1_over_nine[df_gs_1_over_nine.CONTACT_X_abs <= 11.88])

        # 2nd serve
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        second_initiative_total = len(df_gs_2)
        second_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # 2nd return
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name != Calculations.PLAYER_NAME)]
        second_return_initiative_total = len(df_gs_2)
        second_return_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # over nine
        df_gs_over_nine = df_gs[df_gs.shot_no >= 9]
        over_nine_all_total = len(df_gs_over_nine)
        over_nine_inside_all_total = len(df_gs_over_nine[df_gs_over_nine.CONTACT_X_abs <= 11.88])

        if not second_initiative_total:
            initiative_second = 0
        else:
            initiative_second = round(second_initiative_inside_total / second_initiative_total * 100, 2)
        
        
        return initiative_second, second_initiative_total
    
    def initiative_second_return(self, df):
        # Taking the initiative 
        ds_points = df[(df['PLAYER_HIT'] != Calculations.PLAYER_NAME) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
            (df['sel_player_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['opponent_location_at_shot_x_abs_diff'] > -2)
            & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['opponent_decelerations_window_max'] > -5)].point_id.unique()
        df_gs = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 4) & (~df.point_id.isin(ds_points))]

        # 1st serve
        df_gs_1 = df_gs[(df_gs.serve_number == 1) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        df_gs_1_over_nine = df_gs_1[df_gs_1.shot_no >= 9]
        over_nine_total = len(df_gs_1_over_nine)
        over_nine_inside_total = len(df_gs_1_over_nine[df_gs_1_over_nine.CONTACT_X_abs <= 11.88])

        # 2nd serve
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name == Calculations.PLAYER_NAME)]
        second_initiative_total = len(df_gs_2)
        second_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # 2nd return
        df_gs_2 = df_gs[(df_gs.serve_number == 2) & (df_gs.server_name != Calculations.PLAYER_NAME)]
        second_return_initiative_total = len(df_gs_2)
        second_return_initiative_inside_total = len(df_gs_2[df_gs_2.CONTACT_X_abs <= 11.88])

        # over nine
        df_gs_over_nine = df_gs[df_gs.shot_no >= 9]
        over_nine_all_total = len(df_gs_over_nine)
        over_nine_inside_all_total = len(df_gs_over_nine[df_gs_over_nine.CONTACT_X_abs <= 11.88])


        if not second_return_initiative_total:
            initiative_second_return = 0
        else:
            initiative_second_return = round(second_return_initiative_inside_total / second_return_initiative_total * 100, 2)
        
        return initiative_second_return, second_return_initiative_total
        
    def serve_speed_reduction_pressure(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_pressure_point != 1)]
        df_serve_pressure = df[(df.is_shot_in == 1) &(df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_pressure_point == 1)]

        total = len(df_serve_pressure)
        return -1*round(df_serve.SPEED.mean() - df_serve_pressure.SPEED.mean(), 2), total

    def return_speed_reduction_break(self, df):
        df_return = df[(df.is_shot_in == 1) &(df.serve_number == 2) & (df.server_name != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_break_point != 1)]
        df_return_break = df[(df.is_shot_in == 1) &(df.serve_number == 2) & (df.server_name != Calculations.PLAYER_NAME) & (df.shot_no == 2) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_break_point == 1)]

        total = len(df_return_break)
        return -1*round(df_return.SPEED.mean() - df_return_break.SPEED.mean(), 2), total
    
    def break_point_faced_win(self, df):
        df_break_faced = df[(df.is_break_point == 1) & (df.server_name == Calculations.PLAYER_NAME)][['point_id', 'PLAYER_WIN_NAME']].drop_duplicates()
        df_break_faced['won'] = np.where(df_break_faced.PLAYER_WIN_NAME == Calculations.PLAYER_NAME, 1, 0)
        return round(df_break_faced.won.mean() * 100, 2), len(df_break_faced)

    def break_point_opportunity_win(self, df):
        df_break_opportunity = df[(df.is_break_point == 1) & (df.server_name != Calculations.PLAYER_NAME)][['point_id', 'PLAYER_WIN_NAME']].drop_duplicates()
        df_break_opportunity['won'] = np.where(df_break_opportunity.PLAYER_WIN_NAME == Calculations.PLAYER_NAME, 1, 0)
        return round(df_break_opportunity.won.mean() * 100, 2), len(df_break_opportunity)
    
    def serve_quality_deuce_wide(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'deuce') & (df_serve.serve_direction == 'W')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total

    def serve_quality_deuce_t(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'deuce') & (df_serve.serve_direction == 'T')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total
    
    def serve_quality_ad_wide(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'ad') & (df_serve.serve_direction == 'W')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total
    
    def serve_quality_ad_t(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'ad') & (df_serve.serve_direction == 'T')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total

    def serve_quality_second_deuce_wide(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 2) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'deuce') & (df_serve.serve_direction == 'W')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total

    def serve_quality_second_deuce_t(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 2) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'deuce') & (df_serve.serve_direction == 'T')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total
    
    def serve_quality_second_ad_wide(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 2) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'ad') & (df_serve.serve_direction == 'W')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total
    
    def serve_quality_second_ad_t(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 2) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        df_serve = df_serve[(df_serve.serve_deuce_or_ad == 'ad') & (df_serve.serve_direction == 'T')]
        total = len(df_serve)
        return round(np.nan_to_num(np.nanmean(df_serve['serve_quality_number'].values), 0), 2), total
    
    def average_rally_length_serving_1st(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 1) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        total = len(df_serve)
        if total:
            return round(df['rally_length'].mean()), total
        else:
            return 0, 0
    
    def average_rally_length_serving_2nd(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.serve_number == 2) & (df.server_name == Calculations.PLAYER_NAME) & (df.shot_no == 1) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) ]
        total = len(df_serve)
        if total:
            return round(df['rally_length'].mean()), total
        else:
            return 0, 0
    
    def rally_winners_per_match(self, df):
        df_winner = df[(df.shot_no >= 4) 
                       & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                       & (df.is_last_shot == 1)
                       & (df.is_shot_in == 1)
                       & (df.CONTACT_X_abs >= 9)
                       & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
        return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()
    
    def rally_ue_per_match(self, df):
        df_winner = df[(df.shot_no >= 4) 
                       & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                       & (df.is_last_shot == 1)
                       & (df.is_shot_in == 0)
                        & (df.CONTACT_X_abs >= 9)
                       & (df['Rally ending shot'] == 'Unforced Error')
                       & (df.PLAYER_HIT != df.PLAYER_WIN_NAME)]
        return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()

    def fh_rally_winners_per_match(self, df):
            df_winner = df[(df.shot_no >= 4) 
                           & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                           & (df.is_last_shot == 1)
                           & (df.is_shot_in == 1)
                            & (df.shot_type == 'F')
                            & (df.CONTACT_X_abs >= 9)
                           & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
            return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()
        
    def fh_rally_ue_per_match(self, df):
            df_winner = df[(df.shot_no >= 4) 
                           & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                           & (df.is_last_shot == 1)
                           & (df.is_shot_in == 0)
                           & (df.shot_type == 'F')
                           & (df.CONTACT_X_abs >= 9)
                           & (df['Rally ending shot'] == 'Unforced Error')
                           & (df.PLAYER_HIT != df.PLAYER_WIN_NAME)]
            return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()
    def bh_rally_winners_per_match(self, df):
                df_winner = df[(df.shot_no >= 4) 
                               & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                               & (df.is_last_shot == 1)
                               & (df.is_shot_in == 1)
                                & (df.shot_type == 'B')
                                & (df.CONTACT_X_abs >= 9)
                               & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
                return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()
            
    def bh_rally_ue_per_match(self, df):
                df_winner = df[(df.shot_no >= 4) 
                               & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                               & (df.is_last_shot == 1)
                               & (df.is_shot_in == 0)
                               & (df.shot_type == 'B')
                               & (df.CONTACT_X_abs >= 9)
                               & (df['Rally ending shot'] == 'Unforced Error')
                               & (df.PLAYER_HIT != df.PLAYER_WIN_NAME)]
                return len(df_winner) / df.match_id.nunique(), df.match_id.nunique()
    def rally_winners_and_forcing_error_per_match(self, df):
        df_winner = df[(df.shot_no >= 4) 
                       & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                       & (df.is_last_shot == 1)
                       & (df.is_shot_in == 1)
                       & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
        df_fe = df[(df.shot_no >= 4) 
                       & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                       & (df.shot_no == df.rally_length - 1)
                       & (df['Rally ending shot'] == 'Forcing Error')
                       & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
        return (len(df_winner)+len(df_fe)) / df.match_id.nunique(), df.match_id.nunique()

    def fh_rally_winners_and_forcing_error_per_match(self, df):
            df_winner = df[(df.shot_no >= 4) 
                           & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                           & (df.is_last_shot == 1)
                           & (df.is_shot_in == 1)
                           & (df.shot_type == 'F')
                         & (df.CONTACT_X_abs >= 9)
                           & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
            df_fe = df[(df.shot_no >= 4) 
                           & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                           & (df.shot_no == df.rally_length - 1)
                           & (df.shot_type == 'F')
                         & (df.CONTACT_X_abs >= 9)
                           & (df['Rally ending shot'] == 'Forcing Error')
                           & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
            return (len(df_winner)+len(df_fe)) / df.match_id.nunique(), df.match_id.nunique()

    def bh_rally_winners_and_forcing_error_per_match(self, df):
                df_winner = df[(df.shot_no >= 4) 
                               & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                               & (df.is_last_shot == 1)
                               & (df.is_shot_in == 1)
                               & (df.shot_type == 'B')
                             & (df.CONTACT_X_abs >= 9)
                               & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
                df_fe = df[(df.shot_no >= 4) 
                               & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                               & (df.shot_no == df.rally_length - 1)
                               & (df.shot_type == 'B')
                             & (df.CONTACT_X_abs >= 9)
                               & (df['Rally ending shot'] == 'Forcing Error')
                               & (df.PLAYER_HIT == df.PLAYER_WIN_NAME)]
                return (len(df_winner)+len(df_fe)) / df.match_id.nunique(), df.match_id.nunique()
    
    def topspin_slice(self, df):
        df = df[df.shot_type == 'B']
        df_topspin = df[(df.shot_no >= 4) 
                        & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                        & (df.spinRPM > 0)]
        df_slice = df[(df.shot_no >= 4) 
                        & (df.PLAYER_HIT == Calculations.PLAYER_NAME)
                        & (df.spinRPM < 0)]
        if len(df_slice) and len(df_topspin):
            ratio = round(len(df_topspin) / len(df_slice), 2)
            return ratio, len(df_topspin) + len(df_slice)
        else:
            return 0, len(df_topspin) + len(df_slice)
    
    def fh_cc_dtl_ratio(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        if len(df_fh_dtl) and len(df_fh_cc):
            ratio = round(len(df_fh_cc) / len(df_fh_dtl), 2)
            return ratio, len(df_fh_cc) + len(df_fh_dtl)
        else:
            return 0, len(df_fh_cc) + len(df_fh_dtl)


    def bh_cc_dtl_ratio(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        if len(df_fh_dtl) and len(df_fh_cc):
            ratio = round(len(df_fh_cc) / len(df_fh_dtl), 2)
            return ratio, len(df_fh_cc) + len(df_fh_dtl)
        else:
            return 0, len(df_fh_cc) + len(df_fh_dtl)

    
        
    def bh_cc_speed(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
           return  0, 0
    
    def bh_dtl_speed(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
           return  0, 0

    def fh_cc_speed(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_speed(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.SPEED.mean(), 2), total
        else:
            return 0, 0
    def bh_cc_depth(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def bh_dtl_depth(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0

    def fh_cc_depth(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_depth(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def bh_cc_spin(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0
    
    def bh_dtl_spin(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0

    def fh_cc_spin(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_spin(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.rally_length-df.shot_no >= 2)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.spinRPM.mean(), 2), total
        else:
            return 0, 0
    
    def bh_cc_speed_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
           return  0, 0
    
    def bh_dtl_speed_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
           return  0, 0

    def fh_cc_speed_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.SPEED.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_speed_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.SPEED.mean(), 2), total
        else:
            return 0, 0
    def bh_cc_depth_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def bh_dtl_depth_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0

    def fh_cc_depth_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_depth_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.REBOUND_X_abs.mean(), 2), total
        else:
            return 0, 0
    
    def bh_cc_spin_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0
    
    def bh_dtl_spin_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0

    def fh_cc_spin_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_cc)
        if total:
            return round(df_fh_cc.spinRPM.mean(), 2), total
        else:
            return 0, 0
    
    def fh_dtl_spin_winners(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[df.spinRPM > 0]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.is_shot_in == 1) & (df.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df.rally_length - df.shot_no <= 1)]
        
        
        df_fh_dtl = df_fh[(df_fh['shot_no'] > 2) &(df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier < 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        
        df_fh_cc = df_fh[(df_fh['shot_no'] > 2) & (df_fh['REBOUND_Y_mirrored']*leftie_multiplier > 1)  & 
                  (df_fh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_fh['CONTACT_X_abs'] > 9) & (df_fh['opponent_location_at_shot_x_abs'] > 9)]
        total = len(df_fh_dtl)
        if total:
            return round(df_fh_dtl.spinRPM.mean(), 2), total
        else:
            return 0, 0
        
    def rally_play_1st_serve_finished_in_5_shots_or_less(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.shot_no == 1) 
                      & (df.server_name == Calculations.PLAYER_NAME) & (df.serve_number == 1)]
        total = len(df_serve)
        if total:
            return round(len(df_serve[(df_serve.rally_length <= 5)]) / total, 2), total
        else:
            return 0, 0
        
    def rally_play_1st_serve_won_in_5_shots_or_less(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.shot_no == 1) 
                      & (df.server_name == Calculations.PLAYER_NAME) & (df.serve_number == 1)]
        total = len(df_serve)
        if total:
            return round(len(df_serve[(df_serve.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df_serve.rally_length <= 5)]) / total, 2), total
        else:
            return 0, 0
    
    def rally_play_2nd_return_won_in_5_or_less(self, df):
        df_serve = df[(df.is_shot_in == 1) & (df.shot_no == 1) 
                      & (df.server_name != Calculations.PLAYER_NAME) & (df.serve_number == 2)]
        total = len(df_serve)
        if total:
            return round(len(df_serve[(df_serve.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) & (df_serve.rally_length <= 5)]) / total, 2), total
        else:
            return 0, 0
    

    def rally_play_long_rallies_won(self, df):
        df_long = df[df.rally_length >= 6]
        total = len(df_long.point_id.unique())
        if total:
            return round(len(df_long[(df_long.PLAYER_WIN_NAME == Calculations.PLAYER_NAME)].point_id.unique()) / total, 2), total
        else:
            return 0, 0

    def approach_percentage(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_no >= 3]
        df_all_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 3)]
        total = len(df_all_shots)
        if total:
            return (len(df_approach) / total)
        else:
            return 0, 0
    

    def approach_percentage(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_no >= 3]
        df_all_shots = df[(df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.shot_no >= 3)]
        total = len(df_all_shots)
        if total:
            return round(len(df_approach) / total, 2), total
        else:
            return 0, 0

    
    def approach_win_percentage(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_no >= 3]
        total = len(df_approach.point_id.unique())
        if total:
            return round(len(df_approach[df_approach.PLAYER_WIN_NAME == selected_player_name].point_id.unique()) / total, 2), total
        else:
            return 0, 0
    

    def approaches_to_FH(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_no >= 3]
        total = len(df_approach)
        if len(df_approach[df_approach.shot_type_next.isin(['B', 'F'])]):
            return round(len(df_approach[df_approach.shot_type_next == 'F']) / len(df_approach[df_approach.shot_type_next.isin(['B', 'F'])]), 2), total
        else:
            return 0, 0

    def approaches_to_BH(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_s = df[(df['server_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['server_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] == selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['server_location_start_x']) > 7.5) & (abs(df['returner_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_r = df[(df['returner_change_of_possition_beginning_end_x'] == 'forward')&(abs(df['returner_location_diff_x']) > 1.9)&(df['SPEED'] > 70)&(df['server_name'] != selected_player_name) & (df['CONTACT_X_abs'] > 8)
            &(abs(df['returner_location_start_x']) > 7.5) & (abs(df['server_location_start_x']) > 10.5) & (df['shot_no'] > 1)&(df['is_last_shot'] == 0) & (df['PLAYER_HIT'] == selected_player_name)]

        df_approach = df_s.append(df_r)
        df_approach = df_approach[df_approach.shot_no >= 3]
        total = len(df_approach)
        if len(df_approach[df_approach.shot_type_next.isin(['B', 'F'])]):
            return round(len(df_approach[df_approach.shot_type_next == 'B']) / len(df_approach[df_approach.shot_type_next.isin(['B', 'F'])]), 2), total
        else:
            return 0, 0
    
    def bh_dtl_all_rally_shots(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df =  df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_bh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_bh['CONTACT_X_abs'] > 9) & (df_bh['opponent_location_at_shot_x_abs'] > 9)]
        if len(df):
            return round(len(df_bh_dtl) / len(df), 4), len(df)
        else:
            return 0, 0
    
    def bh_dtl_well_placed(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df =  df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_bh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_bh['CONTACT_X_abs'] > 9) & (df_bh['opponent_location_at_shot_x_abs'] > 9)]
        df_bh_dtl_well_placed = df_bh_dtl[df_bh_dtl.distance_from_sideline < 1]
        if len(df_bh_dtl):
            return round(len(df_bh_dtl_well_placed) / len(df_bh_dtl),42), len(df_bh_dtl)
        else:
            return 0, 0
    
    def bh_dtl_fast(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh = df[(df.shot_type == 'B') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_bh_dtl = df_bh[(df_bh['shot_no'] > 2) &(df_bh['REBOUND_Y_mirrored']*leftie_multiplier < -1)  & 
                  (df_bh['CONTACT_Y_mirrored']*leftie_multiplier > 0) & (df_bh['CONTACT_X_abs'] > 9) & (df_bh['opponent_location_at_shot_x_abs'] > 9)]
        df_bh_dtl_fast = df_bh_dtl[df_bh_dtl.SPEED > 115]
        if len(df_bh_dtl):
            return round(len(df_bh_dtl_fast) / len(df_bh_dtl), 4), len(df_bh_dtl)
        else:
            return 0, 0
    
    def fh_all_rally_shots(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]

        if len(df):
            return round(len(df_fh) / len(df), 4), len(df)
        else:
            return 0, 0
    
    def run_around_fh_percentage(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_run_around_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier > 1)]
        if len(df_fh):
            return round(len(df_run_around_fh) / len(df_fh), 4), len(df_fh)
        else:
            return 0, 0
    
    def run_around_fh_winners_fe(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_run_around_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier > 1)]
        df_run_around_fh_w_fe = df_run_around_fh[(df_run_around_fh.shot_no >= df_run_around_fh.rally_length - 1) 
                            & (df_run_around_fh.is_shot_in == 1) 
                            & (df_run_around_fh.PLAYER_WIN_NAME == Calculations.PLAYER_NAME) 
                            & (df_run_around_fh['Rally ending shot'].isin(['Winner', 'Forcing Error']))]
        if len(df_run_around_fh):
            return round(len(df_run_around_fh_w_fe) / len(df_run_around_fh), 4), len(df_run_around_fh)
        else:
            return 0, 0

    def win_in_rallies_with_run_around_forehand(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_run_around_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier > 1)]
        total = df_run_around_fh.point_id.nunique()
        won = df_run_around_fh[df_run_around_fh.PLAYER_WIN_NAME == Calculations.PLAYER_NAME].point_id.nunique()
        if total:
            return round(won / total, 4), total
        else:
            return 0, 0
    
    def fast_attacking_deuce_fh_cross_percentage(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier < 0) & (df.REBOUND_Y_mirrored*leftie_multiplier < -1)]
        df_fh_attack = df_fh[(df_fh.SPEED >= 120)]
        if len(df_fh):
            return round(len(df_fh_attack) / len(df_fh), 4), len(df_fh)
        else:
            return 0, 0

    def fast_attacking_deuce_fh_cross_won(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier < 0) & (df.REBOUND_Y_mirrored*leftie_multiplier < -1)]
        df_fh_attack = df_fh[(df_fh.SPEED >= 120)]
        df_fh_attack_won = df_fh_attack[df_fh_attack.PLAYER_WIN_NAME == Calculations.PLAYER_NAME]
        if len(df_fh_attack):
            return round(len(df_fh_attack_won.point_id.unique()) / len(df_fh_attack.point_id.unique()), 4), len(df_fh_attack.point_id.unique())
        else:
            return 0, 0
    
    def fast_attacking_deuce_fh_line_percentage(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier < 0) & (df.REBOUND_Y_mirrored*leftie_multiplier > 1)]
        df_fh_attack = df_fh[(df_fh.SPEED >= 120)]
        if len(df_fh):
            return round(len(df_fh_attack) / len(df_fh), 4), len(df_fh)
        else:
            return 0, 0

    def fast_attacking_deuce_fh_line_won(self, df):
        leftie_multiplier = Calculations.LEFTIE
        df = df[(df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_fh = df[(df.shot_type == 'F') & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME) & (df.CONTACT_Y_mirrored*leftie_multiplier < 0) & (df.REBOUND_Y_mirrored*leftie_multiplier > 1)]
        df_fh_attack = df_fh[(df_fh.SPEED >= 120)]
        df_fh_attack_won = df_fh_attack[df_fh_attack.PLAYER_WIN_NAME == Calculations.PLAYER_NAME]
        if len(df_fh_attack):
            return round(len(df_fh_attack_won.point_id.unique()) / len(df_fh_attack.point_id.unique()), 4), len(df_fh_attack.point_id.unique())
        else:
            return 0, 0

    def opponent_moved_on_neutral_ball(self, df):
        df = df[(df.is_neutral == 1) & (df.CONTACT_Y_mirrored.between(-2, 2)) & (df.shot_no >= 3) & (df.PLAYER_HIT == Calculations.PLAYER_NAME)]
        df_moved = df[df.opponent_shot_distance_moved.abs() > 5]
        if len(df):
            return round(len(df_moved) / len(df), 4), len(df)
        else:
            return 0, 0

    def dropshots_in_rallies(self, df):
        #df_ds_over_net
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no > 2)]
        df_ds_over_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['sel_player_location_at_shot_x_abs_diff'] > -2)
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & (df['is_in_the_net'] == 1) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) & 
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['sel_player_location_at_shot_x_abs_diff'] > -2) & (pd.isna(df['REBOUND_X']))
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & (df['spinRPM'] < 0) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds = df_ds_over_net.append(df_ds_net)
        
        if len(df):
            return round(len(df_ds) / len(df), 4), len(df)
        else:
            return 0, 0
        
    def dropshots_count(self, df):
        #df_ds_over_net
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no > 2)]
        df_ds_over_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['sel_player_location_at_shot_x_abs_diff'] > -2)
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & (df['is_in_the_net'] == 1) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) & 
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['sel_player_location_at_shot_x_abs_diff'] > -2) & (pd.isna(df['REBOUND_X']))
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & (df['spinRPM'] < 0) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds = df_ds_over_net.append(df_ds_net)
        
        if True:
            return len(df_ds), df.match_id.nunique()
        else:
            return 0, 0
        
    def dropshots_win(self, df):
        #df_ds_over_net
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no > 2)]
        df_ds_over_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['sel_player_location_at_shot_x_abs_diff'] > -2)
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & (df['is_in_the_net'] == 1) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) & 
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['sel_player_location_at_shot_x_abs_diff'] > -2) & (pd.isna(df['REBOUND_X']))
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & (df['spinRPM'] < 0) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds = df_ds_over_net.append(df_ds_net)
        #df_ds = df_ds[df_ds.shot_type == 'B']
        if len(df_ds):
            return round(len(df_ds[df_ds.PLAYER_WIN_NAME == selected_player_name]) / len(df_ds), 4), len(df_ds)
        else:
            return 0, 0
    
    def dropshots_bh_win(self, df):
        #df_ds_over_net
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no > 2)]
        df_ds_over_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['sel_player_location_at_shot_x_abs_diff'] > -2)
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & (df['is_in_the_net'] == 1) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) & 
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['sel_player_location_at_shot_x_abs_diff'] > -2) & (pd.isna(df['REBOUND_X']))
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & (df['spinRPM'] < 0) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds = df_ds_over_net.append(df_ds_net)
        df_ds = df_ds[df_ds.shot_type == 'B']
        if len(df_ds):
            return round(len(df_ds[df_ds.PLAYER_WIN_NAME == selected_player_name]) / len(df_ds), 4), len(df_ds)
        else:
            return 0, 0
    

    def dropshots_fh_win(self, df):
        #df_ds_over_net
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no > 2)]
        df_ds_over_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['REBOUND_X_abs'] <5) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) &
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['REBOUND_X'] * df['CONTACT_X'] < 0) & (df['sel_player_location_at_shot_x_abs_diff'] > -2)
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & ~(df['spinRPM'] > 500) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds_net = df[(df['PLAYER_HIT'] == selected_player_name) & (df['SPEED'] <75) & (df['CONTACT_X_abs'] > 7) & (df['is_in_the_net'] == 1) & ~(pd.isna(df['REBOUND_X_abs'].shift(1))) & 
                (df['opponent_location_at_shot_x_abs'] > 10) & (df['shot_no'] > 2) & (df['sel_player_location_at_shot_x_abs_diff'] > -2) & (pd.isna(df['REBOUND_X']))
                & (df['CONTACT_Z'] < 2.2) & (df['CONTACT_Z'] > 0.3) & (df['spinRPM'] < 0) & (df['CONTACT_X_abs'] < 15) & (df['sel_player_decelerations_window_max'] > -5)]
        df_ds = df_ds_over_net.append(df_ds_net)
        df_ds = df_ds[df_ds.shot_type == 'F']
        if len(df_ds):
            return round(len(df_ds[df_ds.PLAYER_WIN_NAME == selected_player_name]) / len(df_ds), 4), len(df_ds)
        else:
            return 0, 0
        
    def on_the_run_fh_count(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)&(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier < -1.5) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier > -0.5) & (df['shot_type'] == 'F')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier < -2]

        if len(df):
            return len(df_run_fh), df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    

    def on_the_run_bh_count(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)&(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0.5) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]

        if len(df):
            return len(df_run_fh), df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    
    def on_the_run_fh_percent(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)
                       &(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier < -1.5) 
                       & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier > -0.5) 
                       & (df['shot_type'] == 'F')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier < -2]

        if len(df):
            return round(len(df_run_fh) / len(df), 4), len(df)
        else:
            return 0, 0
    

    def on_the_run_bh_percent(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)&(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0.5) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]

        if len(df):
            return round(len(df_run_fh) / len(df), 4), len(df)
        else:
            return 0, 0
    
    def on_the_run_fh_won(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)&(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier < -1.5) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier > -0.5) & (df['shot_type'] == 'F')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier < -2]

        if len(df_run_fh):
            return round(len(df_run_fh[df_run_fh.PLAYER_WIN_NAME == selected_player_name].point_id.unique()) / len(df_run_fh.point_id.unique()), 4), len(df_run_fh.point_id.unique())
        else:
            return 0, 0
    
    def on_the_run_bh_won(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT != selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] != selected_player_name) & (df['SPIN'] != 3)&(df['CONTACT_X_abs'] > 10)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0.5) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['opponent_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]

        if len(df_run_fh):
            return round(len(df_run_fh[df_run_fh.PLAYER_WIN_NAME == selected_player_name].point_id.unique()) / len(df_run_fh.point_id.unique()), 4), len(df_run_fh.point_id.unique())
        else:
            return 0, 0

    def on_the_run_bh_slice(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT == selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] == selected_player_name) &(df['CONTACT_X_abs'] > 12)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['sel_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]

        if len(df_run_fh):
            return round(len(df_run_fh[df_run_fh.spinRPM < 0]) / len(df_run_fh), 4), len(df_run_fh)
        else:
            return 0, 0

    
    def on_the_run_bh_slice_won(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT == selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] == selected_player_name)&(df['CONTACT_X_abs'] > 12)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['sel_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]
        df_run_fh_slice = df_run_fh[df_run_fh.spinRPM < 0]
        if len(df_run_fh_slice):
            return round(len(df_run_fh_slice[df_run_fh_slice.PLAYER_WIN_NAME == selected_player_name]) / len(df_run_fh_slice), 4), len(df_run_fh_slice)
        else:
            return 0, 0

    def on_the_run_bh_slice_won_on_fast(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no  >= 4) & (df.PLAYER_HIT == selected_player_name)]
        df_run_fh = df[(df['PLAYER_HIT'] == selected_player_name)&(df['CONTACT_X_abs'] > 12)&(df['CONTACT_Y_mirrored']*leftie_multiplier > 2) & (df['CONTACT_Y_mirrored'].shift(2)*leftie_multiplier < 0) & (df['shot_type'] == 'B')
              & (df['SPEED'] >75) & (df['shot_no'] > 3) & (df['sel_player_location_at_shot_y_abs_diff'] > 4)]
        df_run_fh = df_run_fh[df_run_fh.CONTACT_Y_mirrored*leftie_multiplier > 2]
        df_run_fh_slice = df_run_fh[(df_run_fh.spinRPM < 0) & (df_run_fh.previous_shot_speed > 115)]
        if len(df_run_fh_slice):
            return round(len(df_run_fh_slice[df_run_fh_slice.PLAYER_WIN_NAME == selected_player_name]) / len(df_run_fh_slice), 4), len(df_run_fh_slice)
        else:
            return 0, 0

    def fh_cross_finish_win(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df_fh_cross = df[(df.shot_type == 'F') & (df.CONTACT_Y_mirrored*leftie_multiplier < -1) & (df.REBOUND_Y_mirrored*leftie_multiplier < -1)]


        df_fh_cross_fe = df_fh_cross[(df_fh_cross.shot_no + 1 == df_fh_cross.rally_length) 
        & (df_fh_cross['Rally ending shot'] == 'Forcing Error')]

        df_fh_cross_last = df_fh_cross[df_fh_cross.is_last_shot == 1]
        df_fh_cross = df_fh_cross_fe.append(df_fh_cross_last, ignore_index=True)

        if len(df_fh_cross):
            return round(df_fh_cross[df_fh_cross.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df_fh_cross.point_id.nunique(), 4), df_fh_cross.point_id.nunique()
        else:
            return 0, 0
    
    def bh_cross_finish_win(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df_fh_cross = df[(df.shot_type == 'B') & (df.CONTACT_Y_mirrored*leftie_multiplier > 1) & (df.REBOUND_Y_mirrored*leftie_multiplier > 1)]


        df_fh_cross_fe = df_fh_cross[(df_fh_cross.shot_no + 1 == df_fh_cross.rally_length) 
        & (df_fh_cross['Rally ending shot'] == 'Forcing Error')]

        df_fh_cross_last = df_fh_cross[df_fh_cross.is_last_shot == 1]
        df_fh_cross = df_fh_cross_fe.append(df_fh_cross_last, ignore_index=True)

        if len(df_fh_cross):
            return round(df_fh_cross[df_fh_cross.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df_fh_cross.point_id.nunique(), 4), df_fh_cross.point_id.nunique()
        else:
            return 0, 0
    

    def fh_cross_change_dtl_win(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier < -1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier < -1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier > 1) 
        & (df.shot_type == 'F')]


        if len(df):
            return round(df[df.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df.point_id.nunique(), 4), df.point_id.nunique()
        else:
            return 0, 0
    

    def bh_cross_change_dtl_win(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier > 1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier > 1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier < -1) 
        & (df.shot_type == 'B')]


        if len(df):
            return round(df[df.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df.point_id.nunique(), 4), df.point_id.nunique()
        else:
            return 0, 0
    
    def fh_cross_change_dtl_count(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier < -1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier < -1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier > 1) 
        & (df.shot_type == 'F')]


        if len(df):
            return len(df), df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    

    def bh_cross_change_dtl_count(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier > 1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier > 1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier < -1) 
        & (df.shot_type == 'B')]


        if len(df):
            return len(df), df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    
    def bh_cross_change_to_fh(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier > 1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier > 1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier < 2) 
        & (df.shot_type_next == 'F') 
        & (df.shot_type == 'B')]


        if len(df):
            return round(df[df.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df.point_id.nunique(), 4), df.point_id.nunique()
        else:
            return 0, 0

    def fh_cross_change_to_bh(self, df):
        leftie_multiplier = Calculations.LEFTIE
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.CONTACT_Y_mirrored_previous*leftie_multiplier < -1) 
        & (df.CONTACT_Y_mirrored*leftie_multiplier < -1) 
        & (df.REBOUND_Y_mirrored*leftie_multiplier > -2) 
        & (df.shot_type_next == 'B') 
        & (df.shot_type == 'F')]


        if len(df):
            return round(df[df.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / df.point_id.nunique(), 4), df.point_id.nunique()
        else:
            return 0, 0

    def fast_ball_received_to_bh_percent(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.shot_type == 'B')]
        df_fast = df[df.previous_shot_speed > 120]

        if len(df):
            return round(len(df_fast) / len(df), 4), len(df)
        else:
            return 0, 0
    

    def fast_ball_outgoing_balls_to_opponent_bh(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.shot_no >= 4) & (df.PLAYER_HIT == selected_player_name)]

        df = df[(df.shot_type_next == 'B')]
        df_fast = df[df.SPEED > 120]

        if len(df):
            return round(len(df_fast) / len(df), 4), len(df)
        else:
            return 0, 0


    def shots_hit_inside(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no>=4)]
        total = len(df)
        if not total:
            return 0, 0
        
        return round(len(df[df.CONTACT_X_abs < 11.88]) / total, 2), total
    
    def shots_hit_behind_bl(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no>=4)]
        total = len(df)
        if not total:
            return 0, 0
        
        return round(len(df[df.CONTACT_X_abs.between(11.88, 13.88)]) / total, 2), total

    def shots_hit_further_back(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no>=4)]
        total = len(df)
        if not total:
            return 0, 0
        
        return round(len(df[df.CONTACT_X_abs > 13.88]) / total, 2), total
    
    def fh_winners_easy_ball(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_easy_ball_with_fh = df[(df.SPEED <= 115) 
                          & (df.spinRPM < 2500)
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'F')
                          & (df.is_shot_in == 1)]
        
        df_easy_ball_with_bh = df[(df.SPEED <= 110) 
                          & (df.spinRPM < 1600) 
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'B')
                          & (df.is_shot_in == 1)]
        df_easy_balls = df_easy_ball_with_fh.append(df_easy_ball_with_bh, ignore_index=True)
        total = len(df_easy_balls)
        if total:
            return len(df_easy_balls[
                (df_easy_balls.PLAYER_WIN_NAME == selected_player_name) 
                & (df_easy_balls.shot_no >= df_easy_balls.rally_length - 2)
                & (df_easy_balls.shot_type_next == 'F')]) , df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    
    def bh_winners_easy_ball(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_easy_ball_with_fh = df[(df.SPEED <= 115) 
                          & (df.spinRPM < 2500)
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'F')
                          & (df.is_shot_in == 1)]
        
        df_easy_ball_with_bh = df[(df.SPEED <= 110) 
                          & (df.spinRPM < 1600) 
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'B')
                          & (df.is_shot_in == 1)]
        df_easy_balls = df_easy_ball_with_fh.append(df_easy_ball_with_bh, ignore_index=True)
        total = len(df_easy_balls)
        if total:
            return len(df_easy_balls[
                (df_easy_balls.PLAYER_WIN_NAME == selected_player_name) 
                & (df_easy_balls.shot_no >= df_easy_balls.rally_length - 2)
                & (df_easy_balls.shot_type_next == 'B')]) , df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    
    def bh_errors_easy_ball(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_easy_ball_with_fh = df[(df.SPEED <= 115) 
                          & (df.spinRPM < 2500)
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'F')
                          & (df.is_shot_in == 1)]
        
        df_easy_ball_with_bh = df[(df.SPEED <= 110) 
                          & (df.spinRPM < 1600) 
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'B')
                          & (df.is_shot_in == 1)]
        df_easy_balls = df_easy_ball_with_fh.append(df_easy_ball_with_bh, ignore_index=True)
        total = len(df_easy_balls)
        if total:
            return len(df_easy_balls[
                (df_easy_balls.PLAYER_WIN_NAME != selected_player_name) 
                & (df_easy_balls.shot_no == df_easy_balls.rally_length - 1)
                & (df_easy_balls.shot_type_next == 'B')]) , df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
    
    def fh_errors_easy_ball(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_easy_ball_with_fh = df[(df.SPEED <= 115) 
                          & (df.spinRPM < 2500)
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'F')
                          & (df.is_shot_in == 1)]
        
        df_easy_ball_with_bh = df[(df.SPEED <= 110) 
                          & (df.spinRPM < 1600) 
                          & (df.spinRPM > 0)
                          & (df.PLAYER_HIT != selected_player_name) 
                          & (df.CONTACT_X_abs > 9)
                          & (df.shot_type == 'B')
                          & (df.is_shot_in == 1)]
        df_easy_balls = df_easy_ball_with_fh.append(df_easy_ball_with_bh, ignore_index=True)
        total = len(df_easy_balls)
        if total:
            return len(df_easy_balls[
                (df_easy_balls.PLAYER_WIN_NAME != selected_player_name) 
                & (df_easy_balls.shot_no == df_easy_balls.rally_length - 1)
                & (df_easy_balls.shot_type_next == 'F')]) , df.match_id.nunique()
        else:
            return 0, df.match_id.nunique()
        
    def bh_slice_deep_count(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_slice = df[(df.PLAYER_HIT == selected_player_name)
                & (df.shot_no > 3)
                & (df.REBOUND_X_abs > 9.15)
                & (df.is_shot_in == 1)
                & (df.shot_type == 'B')
                & (df.spinRPM < 0)]
        return len(df_slice), df.match_id.nunique()
    
    def bh_slice_deep_win(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_slice = df[(df.PLAYER_HIT == selected_player_name)
                & (df.shot_no > 3)
                & (df.REBOUND_X_abs > 9.15)
                & (df.is_shot_in == 1)
                & (df.shot_type == 'B')
                & (df.spinRPM < 0)]
        if len(df_slice):
            return round(len(df_slice[df_slice.PLAYER_WIN_NAME == selected_player_name]) / len(df_slice), 2), len(df_slice)
        return 0, 0
    
    def bh_slice_short_low_win(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_slice = df[(df.PLAYER_HIT == selected_player_name)
                & (df.shot_no > 3)
                & (df.ON_NET_Z < 1.35)
                & (df.REBOUND_X_abs.between(4.5, 7))
                & (df.is_shot_in == 1)
                & (df.shot_type == 'B')
                & (df.spinRPM < 0)]
        if len(df_slice):
            return round(len(df_slice[df_slice.PLAYER_WIN_NAME == selected_player_name]) / len(df_slice), 2), len(df_slice)
        return 0, 0
    
    def bh_slice_short_low_count(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_slice = df[(df.PLAYER_HIT == selected_player_name)
                & (df.shot_no > 3)
                & (df.ON_NET_Z < 1.35)
                & (df.REBOUND_X_abs.between(4.5, 7))
                & (df.is_shot_in == 1)
                & (df.shot_type == 'B')
                & (df.spinRPM < 0)]
        if len(df_slice):
            return len(df_slice), df.match_id.nunique()
        return 0, df.match_id.nunique()
    
    def movement_to_fh_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_fh_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_fh)
        if total:
           return  df_fh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_bh_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    

    def movement_first_serve_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 1) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_avg_speed.mean(), total
        return 0, 0
    

    def movement_first_serve_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 1) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max.mean(), total
        return 0, 0
    
    def movement_first_serve_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 1) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max.mean(), total
        return 0, 0
    

    def movement_second_serve_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 2) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_avg_speed.mean(), total
        return 0, 0
    

    def movement_second_serve_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 2) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max.mean(), total
        return 0, 0
    
    def movement_second_serve_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.serve_number == 2) & (df.shot_no  == 1) & (df.PLAYER_HIT == selected_player_name)]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_right_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        else:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_fh_direction_right_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        else:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_right_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        else:
            df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_forward_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_fh_direction_forward_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_forward_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_fh)
        if total:
           return  df_fh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_backward_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_fh_direction_backward_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_backward_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_forward_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_bh_direction_forward_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_forward_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'forward')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_backward_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_bh)
        if total:
           return  df_bh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_bh_direction_backward_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_backward_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_x == 'backward')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    def movement_to_fh_direction_right_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_fh_direction_right_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_fh_direction_right_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        df_fh = df[(df.shot_type == 'F') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        total = len(df_fh)
        if total:
            return df_fh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_right_avg_speed(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        else:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_avg_speed_previous.mean(), total
        return 0, 0
    

    def movement_to_bh_direction_right_avg_acc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        else:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_accelerations_window_max_previous.mean(), total
        return 0, 0
    
    def movement_to_bh_direction_right_avg_decc(self, df):
        selected_player_name = Calculations.PLAYER_NAME
        leftie = Calculations.LEFTIE
        if leftie:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'right')]
        else:
            df_bh = df[(df.shot_type == 'B') & (df.shot_no > 3) & (df.PLAYER_HIT == selected_player_name) & (df.sel_player_change_of_possition_beginning_end_y == 'left')]
        total = len(df_bh)
        if total:
            return df_bh.sel_player_decelerations_window_max_previous.mean(), total
        return 0, 0
    
    
    def serve_plus_win(self, df):
       selected_player_name = Calculations.PLAYER_NAME
       leftie = Calculations.LEFTIE
       df_sp = df[(df.PLAYER_HIT == selected_player_name) & (df.shot_no == 3) & (df.is_shot_in == 1)] # confirm this with Ben
       df_sp_won = df_sp[(df_sp.PLAYER_WIN_NAME == selected_player_name) & (df_sp.rally_length <= 6)]

       if len(df_sp):
           return len(df_sp_won) / len(df_sp), len(df_sp)
       else:
           return 0, 0
    
    def rally_long(self, df):
       selected_player_name = Calculations.PLAYER_NAME
       leftie = Calculations.LEFTIE
       long_rallies = df[df.rally_length >= 9]
       total = long_rallies.point_id.nunique() 
       

       if total:
           return long_rallies[long_rallies.PLAYER_WIN_NAME == selected_player_name].point_id.nunique() / total, total
       else:
           return 0, 0  
        
