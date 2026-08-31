import pandas as pd
import numpy as np
import psycopg2
import os
import re
import toml
from sqlalchemy import create_engine

import psycopg2
from concurrent.futures import ProcessPoolExecutor
import csv
from datetime import datetime

import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.patches import FancyBboxPatch
#from docx.shared import Inches
from io import BytesIO
import matplotlib.patches as mpatches
from os import listdir
import pickle
import time
import matplotlib.patches as patches

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['DIN Condensed']
rcParams['font.size'] = 18 #12



def load_data(player_name, selected_match_ids, tour='ATP'):
    import warnings
    warnings.filterwarnings('ignore')
    selected_player_name = player_name
    folder_main = ""
    folder_selected = ''
    #Here we set parameters from outside with papermill
    new_name_for_visuals = ''
    sets = []
    separation_score = []
    old_folder_selected = folder_selected
    usecols = ['CONTACT_X',
            'shot_id',
    'CONTACT_X_abs',
    'surface',
    'CONTACT_Y',
    'CONTACT_Y_abs',
    'CONTACT_Y_mirrored',
    'CONTACT_Z',
    'LET',
    'MAX_TRAJ_Z',
    'NET_COORD_Y',
    'NET_COORD_Y_mirrored',
    'ON_NET_Y',
    'ON_NET_Y_mirrored',
    'distance_from_side_or_center_line',
    'ON_NET_Z',
    'PLAYER_HIT',
    'PLAYER_WIN',
    'PLAYER_WIN_NAME',
    'player_win_name',
    'REBOUND_X',
    'REBOUND_X_abs',
    'REBOUND_Y',
    'REBOUND_Y_mirrored',
    'SET_GAME_POINT',
    'is_pressure_point',
    'SPEED',
    'SPIN',
    'distance',
    'distance_from_base_line',
    'distance_from_sideline',
    'game_no',
    'is_in_the_net',
    'is_last_shot',
    'is_shot_in',
    'match_id',
    'match_point_serve_id',
    'point_id',
    'previous_shot_speed',
    'rally_length',
    'receiver_name',
    'returner_accelerations',
    'returner_accelerations_window_max',
    'returner_change_of_possition_beginning_end_x',
    'returner_decelerations_window_max',
    'returner_location_x',
    'returner_location_y',
    'returner_shot_distance_moved',
    'returner_speeds',
    'returner_speeds_avg',
    'returner_speeds_max',
    'round',
    
    'serve_deuce_or_ad',
    'serve_direction',
    'serve_number',
    'server_accelerations',
    'server_accelerations_window_max',
    'server_change_of_possition_beginning_end_x',
    'server_decelerations_window_max',
    'server_location_x',
    'server_location_y',
    'server_name',
    'server_shot_distance_moved',
    'server_speeds',
    'server_speeds_avg',
    'server_speeds_max',
    'set_no',
    'shot_no',
    'shot_time',
    'shot_time_end',
    'shot_time_start',
    'shot_type',
    'side',
    'speed_after_bounce',
    'speed_after_bounce_before_hit',
    'spinRPM',
    'is_break_point',
    'Rally ending shot']
    # LOAD LIBRARIES AND CONNECT TO 
    

    user='marin'
    password='RV4vjA9xUxTjMc'
    host='gsa-pg-data-production.postgres.database.azure.com'
    port='5432'
    database='hawkeye'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')
    pg_conn = psycopg2.connect(f"dbname={database} user={user} host={host} password={password} port='5432'")

    if not selected_match_ids:
        selected_match_ids = pd.read_sql(f"SELECT match_id from hawkeye_app.{tour.lower()}_matches_data", engine).match_id.to_list()
        matches = []
        selected_match_ids = list(set([x for x in selected_match_ids if selected_player_name.lower() in x.lower() or selected_player_name.replace(' ', '_').lower() in x.lower()]))
    
    selected_match_ids = [x.replace("'", "''") for x in selected_match_ids]
    cols = ','.join(list(f'\"{x}\"' for x in usecols))
    if tour.lower() == 'atp':
        query  = "SELECT %s FROM hawkeye_app.atp_all_movement_data WHERE match_id IN (%s)" % (cols, ','.join([f"'{x}'" for x in selected_match_ids]))
    else:
         query  = "SELECT %s FROM hawkeye_app.wta_all_movement_data WHERE match_id IN (%s)" % (cols, ','.join([f"'{x}'" for x in selected_match_ids]))
    df = pd.read_sql(query, engine)
    df['point_no'] = df.point_id.apply(lambda x: float(x.split('_')[2]))
    df = df.sort_values(by=['match_id', 'set_no', 'game_no', 'point_no', 'serve_number', 'shot_no'])
    #df = pd.read_parquet('Berrettini.parquet')
    #df['time_for_shot'] = df['shot_time_end'] - df['shot_time_start']
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
    df['sel_player_decelerations_window_max'] = np.where(df['server_name'] == selected_player_name, df['server_decelerations_window_max'], df['returner_decelerations_window_max'])
    df['opponent_decelerations_window_max'] = np.where(df['server_name'] != selected_player_name, df['server_decelerations_window_max'], df['returner_decelerations_window_max'])
    df['sel_player_accelerations_window_max'] = np.where(df['server_name'] == selected_player_name, df['server_accelerations_window_max'], df['returner_accelerations_window_max'])
    df['sel_player_shot_distance_moved'] = np.where(df['server_name'] == selected_player_name, df['server_shot_distance_moved'], df['returner_shot_distance_moved'])
    df['sel_player_change_of_possition_beginning_end_x'] = np.where(df['server_name'] == selected_player_name, df['server_change_of_possition_beginning_end_x'], df['returner_change_of_possition_beginning_end_x'])
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

    df['sel_player_location_at_shot_x_y_abs_diff'] = df['sel_player_location_at_shot_x_abs_diff'] + df['sel_player_location_at_shot_y_abs_diff']
    df['distance_from_base_line_previous'] = df['distance_from_base_line'].shift(1)
    df_1 = df[df['SET_GAME_POINT'].str.split('_', expand=True)[0].isin(['1'])]
    df_2 = df[df['SET_GAME_POINT'].str.split('_', expand=True)[0].isin(['2'])]
    df_3 = df[df['SET_GAME_POINT'].str.split('_', expand=True)[0].isin(['3'])]
    df_12 = df[df['SET_GAME_POINT'].str.split('_', expand=True)[0].isin(['1', '2'])]
    df_34 = df[df['SET_GAME_POINT'].str.split('_', expand=True)[0].isin(['3', '4'])]
    df['REBOUND_Y_mirrored_previous_previous'] = df['REBOUND_Y_mirrored_previous'].shift(1) 
    df['REBOUND_X_abs_previous_previous'] = df['REBOUND_X_abs_previous'].shift(1) 
    df['CONTACT_Y_mirrored_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['CONTACT_Y_mirrored'].shift(-1))
    df['CONTACT_X_abs_next'] = np.where(df['is_last_shot'] == 1, np.nan, df['CONTACT_X_abs'].shift(-1))
    df['shot_id_next'] = df['shot_id'].shift(-1)
    df['shot_id_previous'] = df['shot_id'].shift(1)
    
    return df

def get_locations_at_shot(df, column_name):
    at_shot_locations =[]
    for server_location_values in df[column_name].tolist():
        float_values = [float(x) for x in server_location_values.strip('][').split(', ')]
        if len(float_values) > 0:
            at_shot_locations.append(float_values[0])
        else:
            at_shot_locations.append(np.nan)
    return at_shot_locations