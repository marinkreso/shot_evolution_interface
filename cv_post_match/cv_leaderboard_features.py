"""Verbatim ports of the HE leaderboard feature builders (from
leaderboard_data.ipynb) plus a CV shim that synthesizes their inputs from a
cv_adapter frame. Metric semantics stay canonical; CV simply feeds them."""
import numpy as np
import pandas as pd


def get_locations_at_shot(df, column_name):
    at_shot_locations =[]
    for server_location_values in df[column_name].tolist():
        float_values = [float(x) for x in server_location_values.strip('][').split(', ')]
        if len(float_values) > 0:
            at_shot_locations.append(float_values[0])
        else:
            at_shot_locations.append(np.nan)
    return at_shot_locations

# %% cell 5


# %% cell 6


# %% cell 7


def preprocess(df, selected_player_name):
    if 'point_no' not in df.columns:   # CV frames carry point_no already; the
        # HE derivation assumes a fixed point_id layout that CV ids don't have
        df['point_no'] = df.point_id.apply(lambda x: float(x.split('_')[2]))
    df = df.sort_values(by=['match_id', 'set_no', 'game_no', 'point_no', 'serve_number', 'shot_no'])
    df['time_for_shot'] = df['shot_time_start'] - df['shot_time_start'].shift(1)
    #Simplified, because we only want to know for 3+ shots
    df['previous_speed_after_bounce_before_hit'] = df['speed_after_bounce_before_hit'].shift(1)
    df['is_shot_in_previous'] = df['is_shot_in'].shift(1) 
    df['distance_from_sideline_previous'] = df['distance_from_sideline'].shift(1) 
    #Simplified, because we only want to know for 3+ shots
    df['REBOUND_Y_mirrored_abs'] = abs(df['REBOUND_Y_mirrored'])
    df['CONTACT_Y_mirrored_abs'] = abs(df['CONTACT_Y_mirrored'])
    df['REBOUND_Y_mirrored_previous'] = df['REBOUND_Y_mirrored'].shift(1)
    df['REBOUND_Y_mirrored_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['REBOUND_Y_mirrored'].shift(-1))
    df['CONTACT_Y_mirrored_previous'] = df.groupby('point_id')['CONTACT_Y_mirrored'].shift(1)
    df['CONTACT_Y_mirrored_previous_previous'] = df.groupby('point_id')['CONTACT_Y_mirrored'].shift(2)
    df['CONTACT_X_abs_previous'] = df.groupby('point_id')['CONTACT_X_abs'].shift(1)
    df['CONTACT_X_abs_previous_previous'] = df.groupby('point_id')['CONTACT_X_abs'].shift(2)
    df['shot_type_next'] = df.groupby('point_id')['shot_type'].shift(-1)
    df['REBOUND_X_abs_previous'] = df['REBOUND_X_abs'].shift(1)
    df['spinRPM_previous'] = df['spinRPM'].shift(1)
    df['CONTACT_Z_previous'] = df['CONTACT_Z'].shift(1)
    df['distance_from_bounce_to_hit'] = df['CONTACT_X_abs'] - df['REBOUND_X_abs_previous']
    df['distance_from_bounce_to_hit_previous'] = df['distance_from_bounce_to_hit'].shift(1)
    df['SPEED_previous'] = df['SPEED'].shift(1)
    df['cross_court_ball_approaching_number'] = abs((-1*df['CONTACT_Y_mirrored']) - df['CONTACT_Y_mirrored_previous'])
    df['is_approaching_shot_cross_court'] = np.where(df['CONTACT_Y_mirrored']*df['CONTACT_Y_mirrored_previous'] > 0, 1, 0)
    df['shot_direction'] = abs((-1*df['CONTACT_Y_mirrored']) - df['REBOUND_Y_mirrored'])
    df['is_shot_cross_court'] = np.where(df['CONTACT_Y_mirrored']*df['REBOUND_Y_mirrored'] > 0, 1, 0)
    df['is_shot_in_previous'] = df['is_shot_in'].shift(1) 
    df['distance_from_sideline_previous'] = df['distance_from_sideline'].shift(1) 
    df['sel_player_max_speed'] = np.where(df['server_name'] == selected_player_name, df['server_speeds_max'], df['returner_speeds_max'])
    df['sel_player_avg_speed'] = np.where(df['server_name'] == selected_player_name, df['server_speeds_avg'], df['returner_speeds_avg'])
    df['sel_player_shot_distance_moved'] = np.where(df['server_name'] == selected_player_name, df['server_shot_distance_moved'], df['returner_shot_distance_moved'])
    df['sel_player_change_of_possition_beginning_end_x'] = np.where(df['server_name'] == selected_player_name, df['server_change_of_possition_beginning_end_x'], df['returner_change_of_possition_beginning_end_x'])
    df['sel_player_change_of_possition_beginning_end_y'] = np.where(df['server_name'] == selected_player_name, df['server_change_of_possition_beginning_end_y'], df['returner_change_of_possition_beginning_end_y'])
    df['opponent_change_of_possition_beginning_end_x'] = np.where(df['server_name'] == selected_player_name, df['returner_change_of_possition_beginning_end_x'], df['server_change_of_possition_beginning_end_x'])
    df['sel_player_shot_distance_moved_previous'] = df['sel_player_shot_distance_moved'].shift(1) 
    df['sel_player_shot_distance_moved_previous'] = df['sel_player_shot_distance_moved'].shift(1) 
    if 'spinRPM' not in df.columns.tolist():
        df['spinRPM'] = np.nan
    #Simplified, because we only want to know for 3+ shots
    df['REBOUND_Y_mirrored_abs'] = abs(df['REBOUND_Y_mirrored'])
    df['CONTACT_Y_mirrored_abs'] = abs(df['CONTACT_Y_mirrored'])
    df['REBOUND_Y_mirrored_previous'] = df['REBOUND_Y_mirrored'].shift(1)
    df['REBOUND_Y_mirrored_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['REBOUND_Y_mirrored'].shift(-1))
    df['CONTACT_Y_mirrored_previous'] = df['CONTACT_Y_mirrored'].shift(1)
    df['CONTACT_X_abs_previous'] = df['CONTACT_X_abs'].shift(1)
    df['REBOUND_X_abs_previous'] = df['REBOUND_X_abs'].shift(1)
    df['spinRPM_previous'] = df['spinRPM'].shift(1)
    df['time_for_shot_previous'] = df['time_for_shot'].shift(1)
    df['distance_from_bounce_to_hit'] = df['CONTACT_X_abs'] - df['REBOUND_X_abs_previous']
    df['cross_court_ball_approaching_number'] = abs((-1*df['CONTACT_Y_mirrored']) - df['CONTACT_Y_mirrored_previous'])
    df['is_approaching_shot_cross_court'] = np.where(df['CONTACT_Y_mirrored']*df['CONTACT_Y_mirrored_previous'] > 0, 1, 0)
    df['shot_direction'] = abs((-1*df['CONTACT_Y_mirrored']) - df['REBOUND_Y_mirrored'])
    df['is_shot_cross_court'] = np.where(df['CONTACT_Y_mirrored']*df['REBOUND_Y_mirrored'] > 0, 1, 0)
    df['is_shot_in_previous'] = df['is_shot_in'].shift(1) 
    df['distance_from_sideline_previous'] = df['distance_from_sideline'].shift(1) 
    df['sel_player_max_speed'] = np.where(df['server_name'] == selected_player_name, df['server_speeds_max'], df['returner_speeds_max'])
    df['sel_player_avg_speed'] = np.where(df['server_name'] == selected_player_name, df['server_speeds_avg'], df['returner_speeds_avg'])
    df['sel_player_decelerations_window_max'] = np.where(df['server_name'] == selected_player_name, df['server_decelerations_window_max'], df['returner_decelerations_window_max'])
    df['sel_player_accelerations_window_max'] = np.where(df['server_name'] == selected_player_name, df['server_accelerations_window_max'], df['returner_accelerations_window_max'])
    df['sel_player_shot_distance_moved'] = np.where(df['server_name'] == selected_player_name, df['server_shot_distance_moved'], df['returner_shot_distance_moved'])
    df['sel_player_change_of_possition_beginning_end_x'] = np.where(df['server_name'] == selected_player_name, df['server_change_of_possition_beginning_end_x'], df['returner_change_of_possition_beginning_end_x'])
    df['opponent_change_of_possition_beginning_end_x'] = np.where(df['server_name'] == selected_player_name, df['returner_change_of_possition_beginning_end_x'], df['server_change_of_possition_beginning_end_x'])
    df['sel_player_shot_distance_moved_previous'] = df['sel_player_shot_distance_moved'].shift(1) 
    df['sel_player_shot_distance_moved_previous'] = df['sel_player_shot_distance_moved'].shift(1) 
    df['server_location_start_x'] = [float(x.strip('][').split(', ')[0]) for x in df['server_location_x'].tolist()]
    df['returner_location_start_x'] = [float(x.strip('][').split(', ')[0]) for x in df['returner_location_x'].tolist()]
    df['opponent_decelerations_window_max'] = np.where(df['server_name'] != selected_player_name, df['server_decelerations_window_max'], df['returner_decelerations_window_max'])

    df['server_location_diff_x'] = [float(x.strip('][').split(', ')[0]) - float(x.strip('][').split(', ')[-1]) for x in df['server_location_x'].tolist()]
    df['returner_location_diff_x'] = [float(x.strip('][').split(', ')[0]) - float(x.strip('][').split(', ')[-1]) for x in df['returner_location_x'].tolist()]
    df['server_location_at_shot_x'] = get_locations_at_shot(df, 'server_location_x')
    df['returner_location_at_shot_x'] = get_locations_at_shot(df, 'returner_location_x')

    df['sel_player_location_at_shot_x'] = np.where(df['server_name'] == selected_player_name, df['server_location_at_shot_x'], df['returner_location_at_shot_x'])
    df['sel_player_location_at_shot_x_abs'] = df['sel_player_location_at_shot_x'].abs()
    df['opponent_location_at_shot_x'] = np.where(df['server_name'] == selected_player_name, df['returner_location_at_shot_x'], df['server_location_at_shot_x'])
    df['opponent_location_at_shot_x_abs'] = df['opponent_location_at_shot_x'].abs()
    df['sel_player_location_at_shot_x_abs_previous'] = df['sel_player_location_at_shot_x_abs'].shift(1)
    df['opponent_location_at_shot_x_abs_previous'] = df['opponent_location_at_shot_x_abs'].shift(1)
    df['sel_player_location_at_shot_x_abs_diff'] = df['sel_player_location_at_shot_x_abs_previous'] - df['sel_player_location_at_shot_x_abs']
    df['opponent_location_at_shot_x_abs_diff'] = df['opponent_location_at_shot_x_abs_previous'] - df['opponent_location_at_shot_x_abs']
    df['server_location_at_shot_y'] = get_locations_at_shot(df, 'server_location_y')
    df['returner_location_at_shot_y'] = get_locations_at_shot(df, 'returner_location_y')

    df['sel_player_location_at_shot_y'] = np.where(df['server_name'] == selected_player_name, df['server_location_at_shot_y'], df['returner_location_at_shot_y'])
    df['opponent_location_at_shot_y'] = np.where(df['server_name'] == selected_player_name, df['returner_location_at_shot_y'], df['server_location_at_shot_y'])
    df['opponent_location_at_shot_y_mirrored']  = np.where(df['opponent_location_at_shot_x'] > 0, -1*df['opponent_location_at_shot_y'], df['opponent_location_at_shot_y'])
    df['opponent_location_at_shot_y_mirrored_previous'] = df['opponent_location_at_shot_y_mirrored'].shift(1)
    df['server_location_at_shot_y'] = get_locations_at_shot(df, 'server_location_y')
    df['returner_location_at_shot_y'] = get_locations_at_shot(df, 'returner_location_y')

    df['sel_player_location_at_shot_y'] = np.where(df['server_name'] == selected_player_name, df['server_location_at_shot_y'], df['returner_location_at_shot_y'])
    df['opponent_location_at_shot_y'] = np.where(df['server_name'] == selected_player_name, df['returner_location_at_shot_y'], df['server_location_at_shot_y'])
    df['opponent_location_at_shot_y_mirrored']  = np.where(df['opponent_location_at_shot_x'] > 0, -1*df['opponent_location_at_shot_y'], df['opponent_location_at_shot_y'])
    df['opponent_location_at_shot_y_mirrored_previous'] = df['opponent_location_at_shot_y_mirrored'].shift(1)
    
    df['sel_player_location_at_shot_y_previous'] = df['sel_player_location_at_shot_y'].shift(1)
    df['sel_player_location_at_shot_y_abs_diff'] = abs(df['sel_player_location_at_shot_y_previous'] - df['sel_player_location_at_shot_y'])
    
    df['opponent_location_at_shot_y_previous'] = df['opponent_location_at_shot_y'].shift(1)
    df['opponent_player_location_at_shot_y_abs_diff'] = abs(df['opponent_location_at_shot_y_previous'] - df['opponent_location_at_shot_y'])

    df['sel_player_location_at_shot_x_y_abs_diff'] = df['sel_player_location_at_shot_x_abs_diff'] + df['sel_player_location_at_shot_y_abs_diff']
    df['distance_from_base_line_previous'] = df['distance_from_base_line'].shift(1)
    
    df['REBOUND_Y_mirrored_previous_previous'] = df['REBOUND_Y_mirrored_previous'].shift(1) 
    df['REBOUND_X_abs_previous_previous'] = df['REBOUND_X_abs_previous'].shift(1) 
    df['CONTACT_Y_mirrored_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['CONTACT_Y_mirrored'].shift(-1))
    df['CONTACT_X_abs_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['CONTACT_X_abs'].shift(-1))
    df['shot_id_next'] = df['shot_id'].shift(-1)
    df['shot_id_previous'] = df['shot_id'].shift(1)
    
    return df


RALLY_END_MAP = {'UnforcedError': 'Unforced Error', 'ForcedError': 'Forcing Error',
                 'Winner': 'Winner', 'Ace': 'Winner'}


def _loc_str(vals):
    return ['[{0}, {0}]'.format(v if pd.notna(v) else 'nan') for v in vals]


def add_cv_inputs(df, player_name):
    """Synthesize the columns  expects from a cv_adapter frame."""
    df = df.sort_values(['match_id', 'set_no', 'game_no', 'point_no', 'serve_number', 'shot_no']).reset_index(drop=True)
    df['is_last_shot'] = (df.groupby(['point_id', 'serve'])['shot_no'].transform('max') == df['shot_no']).astype(int)
    df['shot_id'] = df['rally_id'] + '_' + df['shot_no'].astype(str)
    df['shot_time_start'] = pd.to_timedelta(df['Hit_time']).dt.total_seconds()
    # spinRPM > 0 is used by the engine as a row-quality gate; CV has no spin, so
    # pass the gate with a placeholder and NULL the spin metrics after the run
    # (cv_pipeline.SPIN_METRICS) so no fake spin numbers ever surface.
    df['spinRPM'] = 1.0
    df['SPIN'] = np.nan
    df['CONTACT_X'] = df['hit_x']
    df['CONTACT_Y'] = df['hit_y']
    df['speed_after_bounce_before_hit'] = np.nan
    df['SPEED_KMH'] = df['SPEED']
    df['REBOUND_X'] = df['bounce_x']
    df['REBOUND_Y'] = df['bounce_y']
    df['previous_shot_speed'] = df.groupby('point_id')['SPEED'].shift(1)
    df['serve_quality_number'] = np.nan   # HE serve-quality model has no CV equivalent yet
    df['is_neutral'] = 0                  # needs both players' movement; CV tracks the hitter only
    df['distance_from_base_line'] = 11.89 - df['REBOUND_X_abs']
    df['Rally ending shot'] = df['outcome'].map(RALLY_END_MAP)

    hitter_is_server = (df['impact_player'] == df['server_name']).to_numpy()
    sx = np.where(hitter_is_server, df['player_location_x'], df['receiver_location_x'])
    sy = np.where(hitter_is_server, df['player_location_y'], df['receiver_location_y'])
    rx = np.where(hitter_is_server, df['receiver_location_x'], df['player_location_x'])
    ry = np.where(hitter_is_server, df['receiver_location_y'], df['player_location_y'])
    df['server_location_x'] = _loc_str(sx)
    df['server_location_y'] = _loc_str(sy)
    df['returner_location_x'] = _loc_str(rx)
    df['returner_location_y'] = _loc_str(ry)
    df['_srv_x'] = sx
    df['_ret_x'] = rx

    # movement: CV tracks the HITTER reaching the ball; the other side is unknown
    spd_max = df.get('move_spd_max', pd.Series(np.nan, index=df.index))
    spd_avg = df.get('move_spd_avg', pd.Series(np.nan, index=df.index))
    acc_max = df.get('move_acc_max', pd.Series(np.nan, index=df.index))
    dec_max = df.get('move_dec_max', pd.Series(np.nan, index=df.index))
    dist = spd_avg * df.get('time_passed', pd.Series(np.nan, index=df.index))
    for side, mask in (('server', hitter_is_server), ('returner', ~hitter_is_server)):
        df[f'{side}_speeds_max'] = np.where(mask, spd_max, np.nan)
        df[f'{side}_speeds_avg'] = np.where(mask, spd_avg, np.nan)
        df[f'{side}_accelerations_window_max'] = np.where(mask, acc_max, np.nan)
        df[f'{side}_decelerations_window_max'] = np.where(mask, dec_max, np.nan)
        df[f'{side}_shot_distance_moved'] = np.where(mask, dist, np.nan)

    # change of position over the point (first -> last known x per side)
    for side, col in (('server', '_srv_x'), ('returner', '_ret_x')):
        g = df.groupby('point_id')[col]
        df[f'{side}_change_of_possition_beginning_end_x'] = g.transform('first') - g.transform('last')
        df[f'{side}_change_of_possition_beginning_end_y'] = np.nan
    df = df.drop(columns=['_srv_x', '_ret_x'])
    return df


def build_leaderboard_frame(df, player_name):
    df = add_cv_inputs(df, player_name)
    df = preprocess(df, player_name)
    # opponent-side movement columns preprocess does not build
    server_is_sel = df['server_name'] == player_name
    for stat in ('shot_distance_moved', 'speeds_avg', 'speeds_max',
                 'accelerations_window_max', 'decelerations_window_max'):
        df[f'opponent_{stat}'] = np.where(server_is_sel, df[f'returner_{stat}'], df[f'server_{stat}'])
    df['opponent_avg_speed'] = df['opponent_speeds_avg']
    for col in ('opponent_shot_distance_moved', 'opponent_avg_speed',
                'opponent_accelerations_window_max', 'sel_player_avg_speed',
                'sel_player_accelerations_window_max'):
        df[f'{col}_previous'] = df.groupby('point_id')[col].shift(1)
    return df
