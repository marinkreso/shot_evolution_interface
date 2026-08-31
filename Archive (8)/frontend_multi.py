from nicegui import ui
from utils_bootstrap_new import *
from utils_bootstrap_new2 import *
from report_util_new import main2, main3
from fastapi import FastAPI
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from collections import defaultdict
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
#img = Image.open('GSAfulllogssso-white.png')asss


shot_movement_columns = ['movement_to_fh_avg_speed',
 'movement_to_fh_avg_acc',
 'movement_to_fh_avg_decc',
 'movement_to_bh_avg_speed',
 'movement_to_bh_avg_acc',
 'movement_to_bh_avg_decc',
 'movement_first_serve_speed',
 'movement_first_serve_acc',
 'movement_first_serve_decc',
 'movement_second_serve_speed',
 'movement_second_serve_acc',
 'movement_second_serve_decc',
 'movement_to_fh_direction_right_avg_speed',
 'movement_to_fh_direction_right_avg_acc',
 'movement_to_fh_direction_right_avg_decc',
 'movement_to_fh_direction_forward_avg_speed',
 'movement_to_fh_direction_forward_avg_acc',
 'movement_to_fh_direction_forward_avg_decc',
 'movement_to_fh_direction_backward_avg_speed',
 'movement_to_fh_direction_backward_avg_acc',
 'movement_to_fh_direction_backward_avg_decc',
 'movement_to_bh_direction_forward_avg_speed',
 'movement_to_bh_direction_forward_avg_acc',
 'movement_to_bh_direction_forward_avg_decc',
 'movement_to_bh_direction_backward_avg_speed',
 'movement_to_bh_direction_backward_avg_acc',
 'movement_to_bh_direction_backward_avg_decc',
 'movement_to_bh_direction_right_avg_speed',
 'movement_to_bh_direction_right_avg_acc',
 'movement_to_bh_direction_right_avg_decc']
#ui.image(img).classes('w-64').classes('mx-auto')s

#df = #load_df()s
movement_patterns = pd.read_csv('movement_patterns.csv')
leaderboard_movement = pd.read_parquet('leaderboard_movement.parquet')
longest_point_all = pd.read_csv('longest_points.csv')
fatigues = pd.read_parquet('fatigues.parquet')

from report_util_all import main5
from PIL import Image
import json


#pretty_dict, data1, data2, data3, data_order = main2()



with open('shot_evolution_data.json') as f:
  data = json.load(f)

@ui.page('/report/{report}', dark=True, response_timeout=15)
async def main_page(report: str):
    #data
    ui.markdown(f'# GSA Shot Quality Evolution Report - {report.split("_")[0]}').classes('mx-auto')
    pretty_dict, data_list, data_order = await run.cpu_bound(main5, data[report])
    #with ui.row():
    #    ui.label('sCSS').style('color: #888; font-weight: bold')
    #    ui.label('Tailwind').classes('font-serif')
    #    ui.label('Quasar').classes('q-ml-xl')
    #ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')
    #img = Image.opens('blockx.jpeg')
    #img = img.resize((10,20), Image.LANCZOS)
    #ui.image(img).classes('w-64')

    with ui.tabs().classes('w-full') as tabs:
        ui.tab('serve', label='Serve')
        ui.tab('return', label='Return')
        ui.tab('return_speed', label='Return Speed')
        ui.tab('consistency', label='Consistency')
        ui.tab('initiative', label='Initiative')
        ui.tab('pressure', label='pressure')
        ui.tab('groundstroke_table', label='Rally FH/BH')
        ui.tab('winners_table', label='WINNERS')
        #ui.tab('groundstroke_table', label='Groundstroke Table')
        ui.tab('approach_stats', label='Approach Stats')
        ui.tab('rally_play_type', label='Rally play type')
    #with ui.tabs() as tabs2:
        ui.tab('offensive', label='Offensive')
        ui.tab('defensive', label='Defensive')
        ui.tab('dropshots', label='Drop shots')
        
    #ui.add_head_html('<style>.my-table tbody td { font-size: 1.25em }</style>')
    #ui.add_head_html('<style>.my-table-header thead th { font-size: 1.25em }</style>')

    with ui.tab_panels(tabs, value='serve').classes('mx-auto'):
        for key in data_order:
            with ui.tab_panel(key).classes('w-full'):
                
                for table in data_order[key]:
                  rows = []
                  for k in table['columns']:
                  #for k in data_order[key]:
                      row_dict = {
                      'filter': pretty_dict.get(k, k.replace("_", " ")).upper().replace('FIRST', '1ST').replace('SECOND', '2ND')#.replace('RETURN FH SPEED', 'FH SPEED').replace('RETURN BH SPEED', 'FH SPEED').replace('DEUCE FH', 'FH DEUCE').replace('DEUCE BH', 'BH DEUCE').replace('AD FH', 'FH AD').replace('AD BH', 'BH AD')
                      
                      }
                      for i, d in enumerate(data_list):
                          row_dict['report' + str(i)] = d[0][k]
                      rows.append(row_dict)
                  columns=[{'name': 'filter', 'label': '', 'field': 'filter', 'align': 'center'}]
                  for i, d in enumerate(data_list):
                      columns.append({'name': 'report1', 'label': f'{d[1]} {d[2]}', 'field': 'report' + str(i), 'align': 'center'})
                  #with ui.row().style('font-size: 5.25em;'):
                  if table.get('title'):
                      ui.markdown(f'## {table.get("title")}').classes('mx-auto')
                  ui.table(columns=columns, rows=rows, row_key='name').classes('w-full').classes('my-table').classes('my-table-header')#.add_slot('header', '<th style="font-size: 1.25em">{{ props.row.name }}</th>')#.style('overflow-x: visible')
            

def highlight_greater(x):
    r = '#ffc9c9'
    b = '#a5d8ff'

    m1 = x['FIRST SET'] > x['LAST SET']
    m2 = x['PRESSURE'] > x['NO PRESSURE']

    df1 = pd.DataFrame('background-color: ', index=x.index, columns=x.columns)
    #rewrite values by boolean masks
    df1['FIRST SET'] = np.where(x['FIRST SET'] > x['LAST SET'], 'background-color: {}'.format(b), np.where(x['FIRST SET'] < x['LAST SET'], 'background-color: {}'.format(r), df1['FIRST SET']))
    df1['LAST SET'] = np.where(x['LAST SET'] > x['FIRST SET'], 'background-color: {}'.format(b), np.where(x['LAST SET'] < x['FIRST SET'], 'background-color: {}'.format(r), df1['LAST SET']))
    
    df1['PRESSURE'] = np.where(x['PRESSURE'] > x['NO PRESSURE'], 'background-color: {}'.format(b), np.where(x['PRESSURE'] < x['NO PRESSURE'], 'background-color: {}'.format(r), df1['PRESSURE']))
    df1['NO PRESSURE'] = np.where(x['NO PRESSURE'] > x['PRESSURE'], 'background-color: {}'.format(b), np.where(x['NO PRESSURE'] < x['PRESSURE'], 'background-color: {}'.format(r), df1['NO PRESSURE']))
    
    df1['FIRST 4 GAMES'] = np.where(x['FIRST 4 GAMES'] > x['LAST 4 GAMES'], 'background-color: {}'.format(b), np.where(x['FIRST 4 GAMES'] < x['LAST 4 GAMES'], 'background-color: {}'.format(r), df1['FIRST 4 GAMES']))
    df1['LAST 4 GAMES'] = np.where(x['LAST 4 GAMES'] > x['FIRST 4 GAMES'], 'background-color: {}'.format(b), np.where(x['LAST 4 GAMES'] < x['FIRST 4 GAMES'], 'background-color: {}'.format(r), df1['LAST 4 GAMES']))
    return df1

with open('data_shots.json') as f:
    data_shots_all = json.load(f)

from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui, run
with open('movement_metadata.json') as f:
    data_movement_metadata = json.load(f)
    
with open('tour_movement.json') as f:
    tour_avg_movement_all = json.load(f)


def tab_report(data, selected_matches, report_names, image_dir, selected_player):
    
    with ui.tabs().classes('mx-auto') as tabs:
        ui.tab('x1', label='Duration')
        ui.tab('x2', label='Shot Movement')
        ui.tab('x3', label='Rally Length')
        ui.tab('x4', label='Shot Type')
        ui.tab('x5', label='Point Distance')
        # ui.tab('fh', label='FH')
        # ui.tab('bh', label='BH')
        # ui.tab('o', label='OFFENSIVE')
        ui.tab('x6', label='Sprints')
        ui.tab('x7', label='Heatmap')
        #ui.tab('x8', label='Player Load')
        ui.tab('x9', label='Longest points')
        ui.tab('x10', label='Fatigue')
        ui.tab('x11', label='Match Info')
    
    empty = False
    empty_ones = []
    for i, x in enumerate(selected_matches):
        if not x:
            empty = True
            empty_ones.append(str(i+1))

    
    if empty and selected_matches:
        ui.notify(f'Please configure every report. You forgot to configure report(s) {" AND ".join(empty_ones)}'.upper())
    if selected_matches and not empty:
        
        selected_matches = selected_matches[0]
        with ui.tab_panels(tabs, value='x1').classes('w-full'):
            with ui.tab_panel('x1').classes('mx-auto'):
                ui.label('Match Duration Info and Movement Patterns').classes('mx-auto').tailwind('font-bold')
                rows = []
                
                movement_patterns_data = movement_patterns[(movement_patterns.match_id.isin(selected_matches)) & (movement_patterns.player_name == selected_player)].drop(columns=['player_name'])
                if movement_patterns_data.empty:
                    ui.markdown('## No data for selection').classes('mx-auto')
                else:
                    
                    for k in ['forward_total', 'backward_total', 'left_total', 'right_total']:
                        movement_patterns_data[k.split('_')[0]] = movement_patterns_data[k] / movement_patterns_data['number_of_points']
                    movement_patterns_data = dict(movement_patterns_data.drop(columns=['match_id']).mean())
                    
                    for key in ['Match Duration (per match)', 'Match Effective Time (per match)', 'Effective Time / Match Duration', 'Total Distance Run (per match)', 'Average Speed', 'Number of strokes (per match)', 'Changes of direction (per point)', 'Longest Single Run']:
                        if key != 'path_to_games':
                            value = movement_patterns_data[key]
                            try:
                                if key in ['Number of strokes (per match)', 'Changes of direction (per point)']:
                                    value = int(round(value))
                                if key in ['Match Duration (per match)', 'Match Effective Time (per match)']:
                                    value = str(int(round(value))) + ' minutes'
                                if key in ['Effective Time / Match Duration']:
                                    value = str(int(round(value))) + '%'
                                if key in ['Longest Single Run', 'Total Distance Run (per match)']:
                                    value = str(round(value, 2)) + ' m'
                                if key in ['Average Speed']:
                                    value =  str(round(value, 2)) + ' m/s'
                            except:
                                print('VALUE:', value)
                            rows.append({
                                'Metric': key,
                                'Value': value
                            })
                    
                    for key in ['Time more than 1m inside the court', 'Time from 1m inside the BL to BL', 'Time from BL to 1m behind the BL', 'Time from 1m to 2m behind the BL', 'Time from 2m to 3m behind the BL', 'Time more than 3m behind the BL']:
                        if key != 'path_to_games':
                            try: 
                                valuex = str(int(round(movement_patterns_data[key]))) + '%'
                            except:
                                valuex = '0%'
                                for k in ['Time more than 1m inside the court', 'Time from 1m inside the BL to BL', 'Time from BL to 1m behind the BL', 'Time from 1m to 2m behind the BL', 'Time from 2m to 3m behind the BL', 'Time more than 3m behind the BL']:
                                    print(k, movement_patterns_data[k])
                            rows.append({
                                'Metric': key,
                                'Value': valuex
                            })

                    
                    ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Metric', 'Value']],
                    rows=rows,
                            ).classes('mx-auto')
                    
                    # ui.label('Movement patterns').classes('mx-auto').tailwind('font-bold')
                    # ui.table(
                    # columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Location', 'Perc of time in the location']],
                    # rows=[{'Location':k,  'Perc of time in the location': data['inside_movement'][k]} for k in data['inside_movement']],
                    #         ).classes('mx-auto')
                    with ui.row().classes('mx-auto'):
                        with ui.column():

                            ui.label('Number of moves in each direction (per point)').classes('mx-auto').tailwind('font-bold')
                            ui.table(
                            columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['forward', 'backward', 'left', 'right']],
                            rows=[{k: round(movement_patterns_data[k], 2) for k in ['forward', 'backward', 'left', 'right']}],
                        ).classes('mx-auto')
                        
                        with ui.row().classes('mx-auto'):
                            with ui.column():

                                ui.label('Number of moves in each direction (total)').classes('mx-auto').tailwind('font-bold')
                                ui.table(
                                columns=[{'name': col, 'label': col.split('_')[0], 'field': col, 'align': 'center'} for col in ['forward_total', 'backward_total', 'left_total', 'right_total']],
                                rows=[{k: round(movement_patterns_data[k]) for k in ['forward_total', 'backward_total', 'left_total', 'right_total']}],
                            ).classes('mx-auto')
            with ui.tab_panel('x2').classes('mx-auto'):
                data_movement = leaderboard_movement[(leaderboard_movement.sets == 'ALL') & (leaderboard_movement.match_id.isin(selected_matches)) & (leaderboard_movement.player_name == selected_player)]
                player_average = dict(leaderboard_movement[(leaderboard_movement.sets == 'ALL') & (leaderboard_movement.player_name == selected_player)][shot_movement_columns].mean())
                tour = 'ATP'
                if selected_player in ['OSAKA', 'SWIATEK']:
                    tour = 'WTA'
                tour_average_movement = tour_avg_movement_all[tour]
                create_nicegui_board(["movement_to_fh_avg_speed",
        "movement_to_fh_avg_acc",
        "movement_to_fh_avg_decc"], 'MOVEMENT TO THE FOREHAND', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_bh_avg_speed",
        "movement_to_bh_avg_acc",
        "movement_to_bh_avg_decc"], 'MOVEMENT TO THE BACKHAND', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_first_serve_speed",
        "movement_first_serve_acc",
        "movement_first_serve_decc"], 'RECOVERY SPEED AFTER 1ST SERVE', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_second_serve_speed",
        "movement_second_serve_acc",
        "movement_second_serve_decc"], 'RECOVERY SPEED AFTER 2ND SERVE', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_fh_direction_right_avg_speed",
        "movement_to_fh_direction_right_avg_acc",
        "movement_to_fh_direction_right_avg_decc"], 'HITTING FOREHANDS MOVING TO THE RIGHT (LEFT FOR LEFTIES)', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_bh_direction_right_avg_speed",
        "movement_to_bh_direction_right_avg_acc",
        "movement_to_bh_direction_right_avg_decc"], 'HITTING BACKHANDS MOVING TO THE LEFT (RIGHT FOR LEFTIES)', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_fh_direction_backward_avg_speed",
        "movement_to_fh_direction_backward_avg_acc",
        "movement_to_fh_direction_backward_avg_decc"], 'HITTING FOREHAND MOVING BACKWARD', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_fh_direction_forward_avg_speed",
        "movement_to_fh_direction_forward_avg_acc",
        "movement_to_fh_direction_forward_avg_decc"], 'HITTING FOREHAND MOVING FORWARD', data_movement, player_average, tour_average_movement)
                create_nicegui_board(["movement_to_bh_direction_backward_avg_speed",
        "movement_to_bh_direction_backward_avg_acc",
        "movement_to_bh_direction_backward_avg_decc"], 'HITTING BACKHAND MOVING BACKWARD', data_movement, player_average, tour_average_movement)
                create_nicegui_board([
                    'movement_to_bh_direction_forward_avg_speed',
                    'movement_to_bh_direction_forward_avg_acc',
        "movement_to_bh_direction_forward_avg_decc"], 'HITTING BACKHAND MOVING FORWARD', data_movement, player_average, tour_average_movement)
            with ui.tab_panel('x3').classes('mx-auto'):
                colors=['#008FD5', '#FF2700', '#77AB43']
                rally_length = pd.read_csv('rally_length.csv')
                rally_length = rally_length[(rally_length.match_id.isin(selected_matches)) & (rally_length.player_name == selected_player)][['rally_duration', 'acceleration_max', 'decelerations_max', 'speeds_avg', 'speeds_max']].groupby('rally_duration').mean().reset_index().to_dict('list')
                
                missing_10_plus = False
                for key in rally_length:
                    if len(rally_length[key]) > 2:
                        rally_length[key][1], rally_length[key][2] = rally_length[key][2], rally_length[key][1]
                    else:
                        missing_10_plus = True
                        pass
                
                rally_length['acceleration_max'].append(np.nan)
                rally_length['speeds_max'].append(np.nan)
                rally_length['speeds_avg'].append(np.nan)
                rally_length['decelerations_max'].append(np.nan)
                rally_length['rally_duration'].append('10+ rally duration')
                
                
                ui.markdown(f'## MAXIMUM ACCELERATION PER RALLY LENGTH').classes('mx-auto')
                keyx = 'acceleration_max'
                x1, x2, x3 = rally_length[keyx][0], rally_length[keyx][1], rally_length[keyx][2]
                r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))
                rally_ratio = [r1, r2, r3]
                for i in range(3):
                    with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                        with ui.row().classes('place-content-center').classes('w-2/12'):
                            ui.label(rally_length['rally_duration'][i].replace('rally shot', 'RALLY SHOTS')).classes('mx-auto')#.classes('w-2/12')#.classes('')
                        ui.linear_progress(rally_ratio[i], color=colors[i], show_value=False, size="20px").classes('w-8/12').props('rounded')
                        ui.label(str(round(rally_length[keyx][i], 2))+ ' ' + 'm/s2').classes('w-2/12')#.classes('mx-auto')#.classes('')
                ui.separator().classes('w-2/3').classes('mx-auto')

                ui.markdown(f'## MAXIMUM DECELERATION PER RALLY LENGTH').classes('mx-auto')
                keyx = 'decelerations_max'
                x1, x2, x3 = rally_length[keyx][0], rally_length[keyx][1], rally_length[keyx][2]
                r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))
                rally_ratio = [r1, r2, r3]
                for i in range(3):
                    with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                        with ui.row().classes('place-content-center').classes('w-2/12'):
                            ui.label(rally_length['rally_duration'][i].replace('rally shot', 'RALLY SHOTS')).classes('mx-auto')#.classes('w-2/12')#.classes('')
                        ui.linear_progress(rally_ratio[i], color=colors[i], show_value=False, size="20px").classes('w-8/12').props('rounded')
                        ui.label(str(round(rally_length[keyx][i], 2))+ ' ' + 'm/s2').classes('w-2/12')#.classes('mx-auto')#.classes('')
                ui.separator().classes('w-2/3').classes('mx-auto')

                ui.markdown(f'## MAXIMUM SPEED PER RALLY LENGTH').classes('mx-auto')
                keyx = 'speeds_max'
                x1, x2, x3 = rally_length[keyx][0], rally_length[keyx][1], rally_length[keyx][2]
                r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))
                rally_ratio = [r1, r2, r3]
                for i in range(3):
                    with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                        with ui.row().classes('place-content-center').classes('w-2/12'):
                            ui.label(rally_length['rally_duration'][i].replace('rally shot', 'RALLY SHOTS')).classes('mx-auto')#.classes('w-2/12')#.classes('')
                        ui.linear_progress(rally_ratio[i], color=colors[i],show_value=False, size="20px").classes('w-8/12').props('rounded')
                        ui.label(str(round(rally_length[keyx][i], 2))+ ' ' + 'm/s').classes('w-2/12')#.classes('mx-auto')#.classes('')
                ui.separator().classes('w-2/3').classes('mx-auto')

                ui.markdown(f'## AVERAGE SPEED PER RALLY LENGTH').classes('mx-auto')
                keyx = 'speeds_avg'
                x1, x2, x3 = rally_length[keyx][0], rally_length[keyx][1], rally_length[keyx][2]
                r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))
                rally_ratio = [r1, r2, r3]
                for i in range(3):
                    with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                        with ui.row().classes('place-content-center').classes('w-2/12'):
                            ui.label(rally_length['rally_duration'][i].replace('rally shot', 'RALLY SHOTS')).classes('mx-auto')#.classes('w-2/12')#.classes('')
                        ui.linear_progress(rally_ratio[i], color=colors[i], show_value=False, size="20px").classes('w-8/12').props('rounded')
                        ui.label(str(round(rally_length[keyx][i], 2))+ ' ' + 'm/s2').classes('w-2/12')#.classes('mx-auto')#.classes('')
                ui.separator().classes('w-2/3').classes('mx-auto')
            data_shots = data_shots_all[selected_player]
            with ui.tab_panel('x4').classes('mx-auto'):
                xd = defaultdict(list)
                for x in data_shots:
                    if x['match_id'] in selected_matches:
                        for k in x['shots_data_numbers']:
                            xd[k].append(x['shots_data_numbers'][k])
                
                #xd = data['shots_data_numbers']
                rows = []
                for key in xd:
                    rows.append({'Stroke': key, 'Number of Shots': sum(xd[key])})
                ui.table(
                columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Stroke', 'Number of Shots']],
                rows=rows,
                ).classes('mx-auto')#.classes('w-full')
            with ui.tab_panel('x5').classes('mx-auto'):
                #ui.add_head_html('<style>.my-table tbody td { font-size: 1.25em }</style>')
                #ui.add_head_html('<style>.my-table-header thead th { font-size: 1.25em }</style>')s
                xtotal = defaultdict(list)
                xmultiplier = defaultdict(list)
                for x in data_shots:
                    if x['match_id'] in selected_matches:
                        for k in x['distance_moved_per_point']:
                            xmultiplier[k].append(x['distance_moved_per_point'][k]['percentage']*x['distance_moved_per_point'][k]['total'])
                            xtotal[k].append(x['distance_moved_per_point'][k]['total'])
                
                if xtotal:
                    rows = []
                    for key in xtotal:
                        frequency = sum(xtotal[key])
                        if frequency:
                            win_perc = str(int(round(sum(xmultiplier[key]) / frequency))) + '%'
                        else:
                            win_perc = '0%'
                        rows.append({'Distance': key, 'Frequency': f"{frequency} ({win_perc}) win"})
                    ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Distance', 'Frequency']],
                    rows=rows,
                    ).classes('mx-auto')#.classes('w-1/3')
            with ui.tab_panel('x6').classes('mx-auto'):
                
                #ui.add_head_html('<style>.my-table tbody td { font-size: 1.25em }</style>')
                #ui.add_head_html('<style>.my-table-header thead th { font-size: 1.25em }</style>')s
                xtotal = defaultdict(list)
                xmultiplier = defaultdict(list)
                for x in data_shots:
                    if x['match_id'] in selected_matches:
                        for k in x['number_of_sprints']:
                            xmultiplier[k].append(x['number_of_sprints'][k]['percentage']*x['number_of_sprints'][k]['total'])
                            xtotal[k].append(x['number_of_sprints'][k]['total'])
                if xtotal:
                    rows = []
                    for key in xtotal:
                        frequency = sum(xtotal[key])
                        if frequency:
                            win_perc = str(int(round(sum(xmultiplier[key]) / frequency))) + '%'
                        else:
                            win_perc = '0%'
                        rows.append({'Speed': key, 'Number': f"{frequency} ({win_perc}) win"})
                    ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Speed', 'Number']],
                    rows=rows,
                    ).classes('mx-auto')
            with ui.tab_panel('x7').classes('mx-auto'):
                ui.image(image_dir + f'heatmap_serve.png').classes('mx-auto').classes('w-1/3')
                with ui.row().classes('no-wrap').classes('mx-auto'):
                    ui.image(image_dir + f'heatmap_first_serve.png').classes('mx-auto').classes('w-96')
                    ui.image(image_dir + f'heatmap_second_serve.png').classes('mx-auto').classes('w-96')
            # with ui.tab_panel('x8').classes('mx-auto'):
            #     ui.image(image_dir + 'player_load.png').classes('mx-auto').classes('w-1/2')
            with ui.tab_panel('x9').classes('mx-auto'):
                df_point = longest_point_all[longest_point_all.match_id.isin(selected_matches)]
                df_point['rnk'] = df_point['point_duration_time_x'].rank(ascending=False)
                df_point = df_point[df_point.rnk <= 15].sort_values('rnk', ascending=True).drop(columns=['rnk'])
                longest_point = json.loads(df_point.to_json(orient='records'))
                
                rows = []
                for l in longest_point:
                    rows.append({
                        'Match': l['match_id'],
                        'Point': l['SET_GAME_POINT'],
                        'Point Duration': str(round(l['point_duration_time_x'])) + ' s',
                        'Rally Length': str(l['rally_length']),
                        'Point Winner': l['PLAYER_WIN_NAME'],
                        'Server': l['server_name'],
                    })
                ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Match', 'Point', 'Point Duration', 'Rally Length', 'Point Winner', 'Server']],
                    rows=rows,
                    ).classes('mx-auto')
            with ui.tab_panel('x10').classes('mx-auto'):
                df_fatigue = fatigues[(fatigues.match_id.isin(selected_matches)) & (fatigues.player_name == selected_player)].drop(columns=['player_name']).groupby(['Features', 'match_segment'])['Value'].mean().round(2).reset_index()#
                df_fatigue['Value'] = df_fatigue['Value'].astype(str)
                df_fatigue = df_fatigue.pivot(index='Features', columns='match_segment', values='Value').reset_index().rename_axis(None, axis=1)
                df_fatigue_s = df_fatigue.style.apply(highlight_greater, axis=None)
                df_fatigue_s = df_fatigue_s.set_table_styles([{'selector': 'td', 'props': [('border-style','solid'),('border-width','1px')]},
                                                            {'selector': 'th', 'props': [('border-style','solid'),('border-width','1px'), ('text-align', 'center')]}])
                df_fatigue_s = df_fatigue_s.set_properties(**{'text-align': 'center'})
                df_fatigue_s.hide()


                #df_fatigue_s.hide_index_()
                #ui.image(image_dir + 'fatigue.png').classes('mx-auto').classes('w-1/2')
                ui.html(df_fatigue_s.to_html()).classes('mx-auto')
            with ui.tab_panel('x11').classes('mx-auto'):
                import re
                rows = []
                for match in selected_matches:
                    try:
                        pattern = re.compile(r'(.+?)_(\d{4})_(.+)')
                        # Use the pattern to match and extract the partssss
                        matches = pattern.match(match)
                        parts = matches.groups()
                        
                        tournament = parts[0].replace('_', ' ').strip().upper()
                        year = parts[1]
                        round_number, p1, p2 = parts[2].split('_')
                        rows.append(
                            {
                                'Tournament': tournament,
                                'Year': year,
                                'P1': p1,
                                'P2': p2,
                                'round': round_number
                            }
                        )
                    except:
                        continue
                ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Tournament', 'Year', 'P1', 'P2']],
                    rows=rows,
                    ).classes('mx-auto')
    

def crud_table( 
    data: list[dict],
    columns: list[dict],
    table_classes="",
    on_save: callable = None,
    on_change: callable = None,
    dialog = None,
    movement_data = None,
    image_dir = None,
    selected_player = None,
    tab_report = None,
    noe = None,
    i=None,
    buttonopener=None
    
) -> None:

    
    def handle_save():
        any_chosen = False
        for d in data:
            if d['SELECT']:
                any_chosen = True
                break
        if any_chosen:        
             noe.selected_matches[i] = [d['match_id'] for d in data if d['SELECT']]
            #tab_report.refresh(movement_data, [d['match_id'] for d in data if d['SELECT']], image_dir, selected_player=selected_player)
        else:
            noe.selected_matches[i] = [d['match_id'] for d in data]
            #tab_report.refresh(movement_data, [d['match_id'] for d in data], image_dir, selected_player=selected_player)
        dialog.close()
        buttonopener.props("color=green")
    
    ui.button("Apply", on_click=handle_save).classes('mx-auto')    
    with ui.element("table").classes(table_classes):
        # table header
        with ui.element("tr"):
            for c in columns:
                with ui.element("th"):
                    ui.label(c["name"])
            with ui.element("th"):
                ui.label("")

        # table body
        with ui.element("tbody") as tbody:
            for row_index, row in enumerate(data):
                with ui.element("tr"):
                    for col_spec in columns:
                        col_name = col_spec["name"]

                        cls = col_spec["ui_type"]
                        cls_parms = col_spec.get("parms", {})
                        if cls == ui.label:
                            cls_parms["text"] = row[col_name]  # avoid triggering on_change when binding
                        else:
                            cls_parms["value"] = row[col_name]  # avoid triggering on_change when binding

                        if on_change:
                            cls_parms["on_change"] = lambda event, r=row_index, c=col_name: on_change(
                                r=r, c=c, value=event.value
                            )

                        # finally, add the td cell with the nicegui control...
                        with ui.element("td").style(col_spec.get("td_style", "")):
                            if cls != ui.label and cls != ui.link:
                                cls(**cls_parms).props("dense").bind_value(row, col_name)
                            else:
                                cls(**cls_parms).props("dense")

                    # with ui.element("td").classes("text-right"):
                    #     ui.button(
                    #         icon="delete", on_click=lambda event, r=row_index: delete_row(r=r)
                    #     ).props("flat size=md dense")

            # # bottom row with add & save buttons
            # with ui.element("tr"):
            #     with ui.element("td").props(f"colspan={len(columns)+1}").classes("text-right"):
            #         ui.button(icon="add", on_click=add_row).props("flat size=md")


def crud_table_simple( 
    data: list[dict],
    columns: list[dict],
    table_classes="",
) -> None:

    
    
    
    
    with ui.element("table").classes(table_classes):
        # table headers
        with ui.element("tr").style(f'background-color: {"#696561"}; border-bottom: 1px solid white'):
            for c in columns:
                with ui.element("th"):
                    ui.label(c["name"]).style('font-size: 200%;')
                        
            with ui.element("th"):
                ui.label("")
                #ui.separator()
        # table body
        with ui.element("tbody") as tbody:
            for row_index, row in enumerate(data):
                with ui.element("tr").style(f'border-bottom: 1px solid white; height:"300%"'):
                    for col_spec in columns:
                        col_name = col_spec["name"]

                        cls = col_spec["ui_type"]
                        cls_parms = col_spec.get("parms", {})
                        if cls == ui.label or cls == ui.link:
                            if cls == ui.label:
                                cls_parms["text"] = row[col_name]  # avoid triggering on_change when binding
                            else:
                                cls_parms["text"] = 'LINK'
                                cls_parms["target"] = row[col_name]
                        else:
                            cls_parms["value"] = row[col_name]  # avoid triggering on_change when binding

                        

                        # finally, add the td cell with the nicegui control...
                        with ui.element("td").style(col_spec.get("td_style", "")):
                            if cls != ui.label and cls != ui.link:
                                cls(**cls_parms).props("dense").bind_value(row, col_name)
                            else:
                                cls(**cls_parms).props("dense").style('font-size: 150%;')
                #ui.separator()
                    # with ui.element("td").classes("text-right"):
                    #     ui.button(
                    #         icon="delete", on_click=lambda event, r=row_index: delete_row(r=r)
                    #     ).props("flat size=md dense")

            # # bottom row with add & save buttons
            # with ui.element("tr"):
            #     with ui.element("td").props(f"colspan={len(columns)+1}").classes("text-right"):
            #         ui.button(icon="add", on_click=add_row).props("flat size=md")
            



class Model1:
    filters = dict()
    def __init__(self, **entries):
        self.__dict__.update(entries)
        #filters = dict()

    @classmethod
    async def all(cls, db):
        return [cls(**item) for item in db[cls.__name__]]

    @classmethod
    async def filter(cls, db, **kwargs):
        #for k, v in kwargs.items():
        #   Model.filters[k] = v
        results = []
        for item in db[cls.__name__]:
            # Check if all key-value pairs in kwargs match the corresponding key-value pairs in the item
            match = True
            
            for k, v in kwargs.items():
                if k == 'YEAR':
                   
                    if 'Last 8 Weeks' in v:
                        if str(datetime.now() - timedelta(days=56)) <= item['DATE']:
                            continue
                    if 'Last 4 Weeks' in v:
                        if str(datetime.now() - timedelta(days=28)) <= item['DATE']:
                            continue
                    if not item[k] in v:
                        match = False

                else:
                    if not item[k] in v:
                        match = False
            
            if match:
                results.append(cls(**item))
        
        return results

class Model2:
    filters = dict()
    def __init__(self, **entries):
        self.__dict__.update(entries)
        #filters = dict()

    @classmethod
    async def all(cls, db):
        return [cls(**item) for item in db[cls.__name__]]

    @classmethod
    async def filter(cls, db, **kwargs):
        #for k, v in kwargs.items():
        #   Model.filters[k] = v
        results = []
        for item in db[cls.__name__]:
            # Check if all key-value pairs in kwargs match the corresponding key-value pairs in the item
            match = True
            
            for k, v in kwargs.items():
                if k == 'YEAR':
                   
                    if 'Last 8 Weeks' in v:
                        if str(datetime.now() - timedelta(days=56)) <= item['DATE']:
                            continue
                    if 'Last 4 Weeks' in v:
                        if str(datetime.now() - timedelta(days=28)) <= item['DATE']:
                            continue
                    if not item[k] in v:
                        match = False

                else:
                    if not item[k] in v:
                        match = False
            
            if match:
                results.append(cls(**item))
        
        return results

class Model3:
    filters = dict()
    def __init__(self, **entries):
        self.__dict__.update(entries)
        #filters = dict()

    @classmethod
    async def all(cls, db):
        return [cls(**item) for item in db[cls.__name__]]

    @classmethod
    async def filter(cls, db, **kwargs):
        #for k, v in kwargs.items():
        #   Model.filters[k] = v
        results = []
        for item in db[cls.__name__]:
            # Check if all key-value pairs in kwargs match the corresponding key-value pairs in the item
            match = True
            
            for k, v in kwargs.items():
                if k == 'YEAR':
                   
                    if 'Last 8 Weeks' in v:
                        if str(datetime.now() - timedelta(days=56)) <= item['DATE']:
                            continue
                    if 'Last 4 Weeks' in v:
                        if str(datetime.now() - timedelta(days=28)) <= item['DATE']:
                            continue
                    if not item[k] in v:
                        match = False

                else:
                    if not item[k] in v:
                        match = False
            
            if match:
                results.append(cls(**item))
        
        return results

                





# def create_nicegui_board_old(columns, title):
        
#         ui.markdown(f'## {title}').classes('mx-auto')
#         import random
#         ui.separator().classes('w-2/3').classes('mx-auto')
#         ui.markdown(f'### SPEED').classes('mx-auto')
#         for c in columns:
#             with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
#                 with ui.row().classes('place-content-center').classes('w-4/12'):
#                     ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
#                 ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
#                 ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
#         ui.separator().classes('w-2/3').classes('mx-auto')
#         ui.markdown(f'### ACCELERATION').classes('mx-auto')
#         for c in columns:
#             with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
#                 with ui.row().classes('place-content-center').classes('w-4/12'):
#                     ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
#                 ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
#                 ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
#         ui.separator().classes('w-2/3').classes('mx-auto')
#         ui.markdown(f'### DECELERATION').classes('mx-auto')
#         for c in columns:
#             with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
#                 with ui.row().classes('place-content-center').classes('w-4/12'):
#                     ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
#                 ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
#                 ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
#       ui.separator().classes('w-2/3').classes('mx-auto')

def create_nicegui_board(columns, title, data_movement_df, player_average, tour_avg_movement):
        data_movement = data_movement_df[columns].mean()
        
        ui.markdown(f'## {title}').classes('mx-auto')
        import random
        #ui.separator().classes('w-2/3').classes('mx-auto'
        for c, desc, metric in zip(columns, ['AVG SPEED', 'AVG ACCELERATION', 'AVG DECELERATION'], ['m/s', 'm/s2', 'm/s2']):
            
            ui.markdown(f'### {desc}').classes('mx-auto')
            
            x1, x2, x3 = data_movement[c], player_average[c], tour_avg_movement[c]
            r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))

            
            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-2/12'):
                    ui.label('MATCH AVERAGE').classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(r1, show_value=False, color='#008FD5', size="20px").classes('w-8/12').props('rounded')
                ui.label(str(round(data_movement[c], 2))+ ' ' + metric).classes('w-2/12')#.classes('mx-auto')#.classes('')
            
            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-2/12'):
                    ui.label('PLAYER AVERAGE').classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(r2, color='#77AB43', show_value=False, size="20px").classes('w-8/12').props('rounded')
                ui.label(str(round(player_average[c], 2)) + ' ' + metric).classes('w-2/12')#.classes('mx-auto')#.classes('')

            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-2/12'):
                    ui.label('TOUR AVERAGE').classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(r3, color='#FF2700', show_value=False, size="20px").classes('w-8/12').props('rounded')
                ui.label(str(round(tour_avg_movement[c], 2))+ ' ' + metric).classes('w-2/12')#.classes('mx-auto')#.classes('')
            
        ui.separator().classes('w-2/3').classes('mx-auto')



# in reality users passwords would obviously need to be hashed
passwords = {'marin': '1s23', 'bhaddassssssssssdmssssssssssassssssssssfssssssssssssssssssasssvssf': 'goldenset1232'}

unrestricted_page_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to the all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


#app.add_middleware(AuthMiddleware)

def init(fastapi_app: FastAPI) -> None:

    @ui.page('/')
    async def show():
        ui.label('Hello, FastAPI!')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )

    @ui.page('/match_new_list/{prefix}', response_timeout=15, dark=True)
    async def match_new_list(prefix: str):
        import re
        from glob import glob
        #list_of_matches = glob(f'matches_new2/{prefix}*')
        #list_of_matches = ['_'.join(x.split('/')[-1].split('_')[1:]) for x in list_of_matches]
        #pattern = re.compile(r'(.+?)_(\d{4})_(.+)')
        with open('post_match_metadata.json') as f:
            list_of_matches = json.load(f)[prefix]
        crud_table_simple_refreshable = ui.refreshable(crud_table_simple)
        data = []
        ui.markdown(f'# {prefix}').classes('mx-auto')
        ui.markdown(f'# LIST OF POST MATCH REPORTS').classes('mx-auto')
        tournaments = set()
        opponents = set()
        list_of_matches = sorted(list_of_matches, key=lambda d: d['DATE'])
        for row in list_of_matches[::-1]:
            tournaments.add(row['TOURNAMENT'])
            opponents.add(row['OPPONENT'])
            report_link = f"https://gsapostmatch.azurewebsites.net/gui/match_new/{prefix}_{row['match_id']}"
            data.append({'TOURNAMENT': row['TOURNAMENT'], 'YEAR': row['YEAR'], 'ROUND': row['ROUND'].upper(), 'OPPONENT': row['OPPONENT'], 'REPORT LINK': report_link, 'SURFACE': row['SURFACE']})
            # data['link'] = 'https://gsapostmatch.azurewebsites.net/gui/match_new/MEDVEDEV_Miami_2024_SF_Medvedev_Sinner'
        #ui.label(str(data))
        columns = [{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in data[0].keys()]
        #ui.table(columns=columns, rows=data, row_key='name').classes('w-1/2').classes('mx-auto')#.add_slot('header', '<th style="font-size: 1.25em">{{ props.row.name }}</th>')#.style('overflow-x: visible')
        columns = [
               
                {
                    "name": "OPPONENT",
                    "ui_type": ui.label,
                },
                {
                    "name": "TOURNAMENT",
                    "ui_type": ui.label,
                },
                {
                    "name": "YEAR",
                    "ui_type": ui.label,
                },
                
                
                {
                    "name": "ROUND",
                    "ui_type": ui.label,
                },
                 {
                    "name": "REPORT LINK",
                    "ui_type": ui.link,
                    "default_value": False
                },
                
            ]
        
        async def on_company_change_simple():
            opponents = selected_opponents.value
            tournaments = sel_tournament.value
            surfaces = selected_surfaces.value
            filters = dict()
            filtered_data = []
            

            for row in data:
                if tournaments:
                    if not row['TOURNAMENT'] in tournaments:
                        continue
                if opponents:
                    if not row['OPPONENT'] in opponents:
                        continue
                if surfaces:
                    if not row['SURFACE'] in surfaces:
                        continue
                filtered_data.append(row)

                    

            
            crud_table_simple_refreshable.refresh(columns=columns, data=filtered_data, table_classes="text-center w-1/2 mx-auto")

            
            
            
        
        with ui.row().classes('w-1/2 mx-auto'):
            sel_tournament = ui.select(label='Tournaments', options=sorted(list(tournaments)), multiple=True, on_change=on_company_change_simple).classes('w-40').props('use-chips').props('rounded outlined').props('popup-content-style="height: 200px"')
            selected_opponents = ui.select(label='Opponents', options=sorted(list(set(opponents))), with_input=True, multiple=True, on_change=on_company_change_simple).classes('w-40').props('use-chips').props('rounded outlined')
            selected_surfaces = ui.select(label='Surfaces', options=sorted(list(set(['hard', 'clay', 'grass']))), with_input=True, multiple=True, on_change=on_company_change_simple).classes('w-40').props('use-chips').props('rounded outlined')
        crud_table_simple_refreshable(columns=columns, data=data, table_classes="text-center w-1/2 mx-auto")
        



    @ui.page('/match_new/{match_str}', response_timeout=15)
    async def main_page_new(match_str: str):
        class ChosenSet:
            def __init__(self):
                self.chosen_set = 'ALL'
        class SelTab:
            def __init__(self):
                self.number = None
        
        
        selected_tab = SelTab()
        chosen_set_object = ChosenSet()
        with open(f'matches_new2/{match_str}/movement.json') as f:
            dm = json.load(f)
        match = '_'.join(match_str.split('_')[1:])

        
        
        #image_dir = f'matches_new2/{match_str}/'
        image_dir = f'https://operationslakedb.blob.core.windows.net/gsa-post-match/{match_str}/'
        images = {
            'first_return': image_dir + 'first_return.png',
            'first_serve': image_dir + 'first_serve.png',
            'second_serve': image_dir + 'second_serve.png',
            'second_return': image_dir + 'second_return.png',
            'second_return': image_dir + 'second_return.png',
            'return_depth': image_dir + 'return_depth.png',
            'return_dir_ad': image_dir + 'return_dir_ad.png',
            'return_dir_deuce': image_dir + 'return_dir_deuce.png',
            'serve_placement': image_dir + 'serve_placement.png',

        }
        pretty_dict, data1_all, data2_all, data_order = await run.cpu_bound(main3, [dm['selected_player_name']], [dm['opponent_name']], [match])
        
        df_games = pd.read_csv(f"matches_new2/{match_str}/{dm['path_to_games']}")
        if not 'combined' in match_str.lower():
            import re
            pattern = re.compile(r'(\D+)(\d{4})(.+)')

            # Use the pattern to match and extract the partssss
            matches = pattern.match(match)
            parts = matches.groups()
            tournament = parts[0].replace('_', ' ').strip().upper()
            year = parts[1]
            ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
            ui.markdown('# Post match report').classes('mx-auto')
            ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()} - {tournament} {year}').classes('mx-auto')
        else:
            ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
            ui.markdown('# Combined report').classes('mx-auto')
            #ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()}').classes('mx-auto')
            
        ui.add_head_html('''
        <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
            <style>
            .progress-label {
            float: left;
            margin-right: 1em;
            
        }
                        .progress-label-right {
            float: right;
            margin-left: 1em;
                        
        }
            .progress {
                position: relative;
                        
            }

            .progress-bar-right {
                position: absolute;
                right: 0;
            }
                        
            

            .progress-value2 {
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                color: #020101; /* Adjust the color as needed */
            }
            </style>
                        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

                        ''')


        #ui.label('')
        
        
        with ui.tabs().classes('mx-auto') as tabs:
                ui.tab('s1', label='1st Serve')
                ui.tab('s2', label='2nd Serve')
                ui.tab('r1', label='1st Return')
                ui.tab('r2', label='2nd Return')
                ui.tab('gs', label='Groundstrokes')
                # ui.tab('fh', label='FH')
                # ui.tab('bh', label='BH')
                # ui.tab('o', label='OFFENSIVE')
                ui.tab('m', label='MOVEMENT')
                ui.tab('ms', label='SHOT MOVEMENT')
                ui.tab('o', label='OTHER')
                #ui.tab('v', label='Video')
        ui.label('SELECT SET').classes('mx-auto')
        @ui.refreshable
        def report_view():
                
                data1 = data1_all[chosen_set_object.chosen_set]
                data2 = data2_all[chosen_set_object.chosen_set]
                
                #ui.label('chosen set'  + toggle.value).classes('mx-auto')
                
                def to_int(x, y):
                    try:
                        if x + y == 0:
                            return 50
                        result = round(100*x / (x+y))
                        if np.isnan(result):
                            return 50
                        else:
                            return int(result)
                    except:
                        print(x, y)
                        return 50


                with ui.tab_panels(tabs).classes('w-full').bind_value(selected_tab, 'number'):
                    with ui.tab_panel('s1'):
                        active_tab_test = 's1'
                        #ui.label('Main Content')
                        items = dict()
                        for key in data_order['serve']:
                            #if '1st' in key.lower():
                            if True:
                                try:
                                    items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                                except:
                                    c = 1 
                                    
                        serve_new_html(ui, dm, '1st Serve', None, items, images, chosen_set_object.chosen_set)
                    with ui.tab_panel('s2'):
                        active_tab_test = 's2'
                        items = dict()
                        for key in data_order['serve_2nd']:
                            #if '2nd' in key.lower():
                            if True:
                                #print(items)
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        serve_new_html_2nd(ui, dm, '2nd Serve', items, images, chosen_set_object.chosen_set)
                    with ui.tab_panel('r1'):
                        active_tab_test = 'r1'
                        items = dict()
                        for key in data_order['return']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        return_new_html(ui, dm, '1st Return Quality', items, images, chosen_set_object.chosen_set)
                    with ui.tab_panel('o'):
                        active_tab_test = 'o'
                        items = dict()
                        for key in data_order['other']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        other_new_html(ui, dm, 'OTHER', items, images, chosen_set_object.chosen_set)
                    with ui.tab_panel('r2'):
                        active_tab_test = 'r2'
                        items = dict()
                        for key in data_order['return_2nd']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        return_new_html2(ui, dm, '2nd Return Quality', items, images, chosen_set_object.chosen_set)
                    
                    with ui.tab_panel('m'):
                        active_tab_test = 'm'
                        items = dict()
                        for key in data_order['return_2nd']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        movement_new_html(ui, dm, df_games)
                    with ui.tab_panel('gs'):
                        active_tab_test = 'gs'
                        items = dict()
                        for key in data_order['groundstroke_table']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        groundstroke_new_html(ui, dm, 'GS Table', items)
                    with ui.tab_panel('ms'):
                        active_tab_test = 'ms'
                        items = dict()
                        for key in data_order['movement']:
                            #if '1st' in key.lower():
                            if True:
                                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        shot_movement_new_html(ui, dm, 'SHOT MOVEMENT', items)
                    
                    # with ui.tab_panel('fh'):
                    #     items = dict()
                    #     for key in data_order['groundstroke_table']:
                    #         #if '1st' in key.lower():
                    #         if True:
                    #           items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                    #     fh_html(ui, dm, 'FH table', items)
                    # with ui.tab_panel('bh'):
                    #     items = dict()
                    #     for key in data_order['groundstroke_table']:
                            
                    #         if True:
                    #           items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                    #     bh_html(ui, dm, 'BH table', items)
                #ui.html('<h1 class="text-center">Item Comparison</h1>')
                if selected_tab.number:
                    
                    tabs.set_value(selected_tab.number)
                else:
                    tabs.set_value('s1')
        def update_ui(e):
                chosen_set_object.chosen_set = e.value
                report_view.refresh()
        if 'sets' in dm:  
            toggle = ui.toggle(dm['sets'], value='ALL', on_change=lambda e: update_ui(e)).classes('mx-auto')
        else:
            toggle = ui.toggle(['ALL', '1', '2', '3'], value='ALL', on_change=lambda e: update_ui(e)).classes('mx-auto')
        report_view()

    
                
    @ui.page('/movement_report/{match_str}', response_timeout=15)
    async def movement_page(match_str: str):
        class MatchData1(Model1):
            pass

        class MatchData2(Model2):
            pass

        class MatchData3(Model3):
            pass
        class MatchData4(Model3):
            pass
        MatchDatas = [MatchData1, MatchData2, MatchData3]
        class NumberOfElements:
            def __init__(self):
                self.number = 1
                self.selected_matches = []
                self.report_names = []
        noe = NumberOfElements()
        crud_table_refreshable = ui.refreshable(crud_table)
        crud_table_refreshables = [ui.refreshable(crud_table), ui.refreshable(crud_table), ui.refreshable(crud_table)]
        tab_report_refreshable = ui.refreshable(tab_report)
        selected_player = match_str.split('_')[0]
        db = {'MatchData1': sorted(data_movement_metadata[selected_player], key=lambda x: x['DATE'], reverse=True),
              'MatchData2': sorted(data_movement_metadata[selected_player], key=lambda x: x['DATE'], reverse=True),
              'MatchData3': sorted(data_movement_metadata[selected_player], key=lambda x: x['DATE'], reverse=True),
              'MatchData4': sorted(data_movement_metadata[selected_player], key=lambda x: x['DATE'], reverse=True)}
        
        def set_report_name(value, i):
            noe.report_names[i] = value

        
        
        @ui.refreshable
        async def button_view(x):
            noe.number = x
            noe.selected_matches = [[]]*x
            noe.report_names = [f'Report {y+1}' for y in range(x)]
            dialogs = []
            buttonopeners = []
            selected_surfaces_list = []
            selected_years_list = []
            selected_opponents_list = []
            async def on_company_change(i, dialoger,matchdata):
                opponents = selected_opponents_list[i].value
                surfaces = selected_surfaces_list[i].value
                years = selected_years_list[i].value
                
                #tournaments = selected_tournaments.value
                filters = dict()
                
                if opponents:
                    filters['OPPONENT'] = opponents
        
                if surfaces:
                    filters['SURFACE'] = surfaces
                
                if years:
                    filters['YEAR'] = years
                
                #if tournaments:
                #    filters['TOURNAMENT'] = tournaments


                

                matches = await matchdata.filter(db,**filters)
                
                
                rows = [
                    {
                        'SELECT': False,
                        'OPPONENT': m.OPPONENT,
                        'YEAR': m.YEAR,
                        'TOURNAMENT': m.TOURNAMENT,
                        'SURFACE': m.SURFACE,
                        'match_id': m.match_id,
                    } for m in matches
                ]

                columns = [
                    {
                        "name": "SELECT",
                        "ui_type": ui.checkbox,
                        "default_value": False
                    },
                    {
                        "name": "OPPONENT",
                        "ui_type": ui.label,
                    },
                    {
                        "name": "TOURNAMENT",
                        "ui_type": ui.label,
                    },
                    {
                        "name": "YEAR",
                        "ui_type": ui.label,
                    },
                    
                    
                    {
                        "name": "SURFACE",
                        "ui_type": ui.label,
                    },
                    
                ]
                
                crud_table_refreshables[i].refresh(rows, columns, table_classes="text-center w-full", dialog=dialoger, movement_data=data, image_dir=image_dir, selected_player=selected_player, tab_report=tab_report_refreshable, noe=noe, i=i, buttonopener=buttonopeners[i])
            with ui.row().classes('mx-auto'):
                for i in range(x):
                    with ui.column():
                        ui.input(label=f'Enter Report Name', placeholder=f'Enter Report Name', on_change=lambda e, i=i: set_report_name(e.value, i)).classes('mx-auto')
                        buttonopener = ui.button(f'CHOOSE MATCHES', color='white', icon='filter_list').classes('mx-auto')
                    with ui.dialog() as dialog, ui.card():
                        
                        with ui.row().classes('w-full'):
                            selected_surfaces = ui.select(label='Surfaces', options=surfaces, multiple=True, on_change=lambda i=i,dialog=dialog,matchdata=MatchDatas[i]: on_company_change(i, dialog,matchdata)).classes('w-40').props('use-chips').props('rounded outlined')
                            selected_years = ui.select(label='Seasons', options=years, multiple=True, on_change=lambda i=i,dialog=dialog,matchdata=MatchDatas[i]: on_company_change(i,dialog,matchdata)).classes('w-40').props('use-chips').props('rounded outlined')
                            selected_opponents = ui.select(label='Opponents', options=list(set(opponents)), with_input=True, multiple=True, on_change=lambda i=i,dialog=dialog,matchdata=MatchDatas[i]: on_company_change(i,dialog,matchdata)).classes('w-40').props('use-chips').props('rounded outlined')
                            selected_surfaces_list.append(selected_surfaces)
                            selected_years_list.append(selected_years)
                            selected_opponents_list.append(selected_opponents)
                            #selected_tournaments = ui.select(label='Tournaments', options=list(set(tournaments)), with_input=True, multiple=True, on_change=on_company_change).classes('w-40').props('use-chips').props('rounded outlined')
                            #ui.button("Apply").classes('w-40').props("size=lg")#.props('outline rounded')
                        matches = await MatchDatas[i].all(db=db)
                        
                        rows = [
                            {
                                'SELECT': False,
                                'OPPONENT': m.OPPONENT,
                                'YEAR': m.YEAR,
                                'TOURNAMENT': m.TOURNAMENT,
                                'SURFACE': m.SURFACE,
                                'match_id': m.match_id
                            } for m in matches
                        ]

                        columns = [
                            {
                                "name": "SELECT",
                                "ui_type": ui.checkbox,
                                "default_value": False
                            },
                            {
                                "name": "OPPONENT",
                                "ui_type": ui.label,
                            },
                            {
                                "name": "TOURNAMENT",
                                "ui_type": ui.label,
                            },
                            {
                                "name": "YEAR",
                                "ui_type": ui.label,
                            },
                            
                            
                            {
                                "name": "SURFACE",
                                "ui_type": ui.label,
                            },
                            
                        ]

                        
                        crud_table_refreshables[i](rows, columns, table_classes="text-center mx-auto w-full", dialog=dialog, movement_data=data, image_dir=image_dir, selected_player=selected_player, tab_report=tab_report_refreshable, noe=noe, i=i, buttonopener=buttonopener)                       
                    #ui.label(f'Label {i}!')
                    
                    dialogs.append(dialog)
                    buttonopener.on('click', dialog.open)
                    buttonopeners.append(buttonopener)

        
        opponents = []
        for x in await MatchData1.all(db):
            opponents.append(x.OPPONENT)
        opponents = sorted(opponents)
        tournaments = set()
        for x in await MatchData1.all(db):
            tournaments.add(x.TOURNAMENT)
        tournaments = list(tournaments)
        
        surfaces = {surface: surface for surface in ['clay', 'grass', 'hard']}
        years = {str(year): str(year) for year in range(2018, 2025)}
        years['Last 8 Weeks'] = 'Last 8 Weeks'
        years['Last 4 Weeks'] = 'Last 4 Weeks'
        image_dir = f'https://operationslakedb.blob.core.windows.net/he-movement-report/{selected_player}_movement/'
        
        
        
                #with ui.element('q-footer').classes('p-4'):
                #    ui.button('Test')
        
        ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
        #ui.markdown(f'# {data["report_title"]}').classes('mx-auto')
        ui.markdown(f'# {selected_player} MOVEMENT REPORT').classes('mx-auto')
        ui.markdown(f'#### SELECT NUMBER OF REPORTS').classes('mx-auto')
        report_toggle = ui.toggle({1: '1', 2: '2', 3: '3'}, value=1, on_change=lambda e: button_view.refresh(e.value)).classes('mx-auto')#.bind_value(noe, 'number')
        await button_view(1)
        ui.button('GENERATE REPORT', on_click=lambda: tab_report_refreshable.refresh(data, noe.selected_matches, noe.report_names, image_dir, selected_player), color='white').classes('mx-auto')
        tab_report_refreshable(data, [], [], image_dir, selected_player)
        
                
            
                


            
       

                
            
            
    


    @ui.page('/login')
    def login() -> Optional[RedirectResponse]:
        def try_login() -> None:  # local funcstionssssss to avoid passing username and password as arguments
            if passwords.get(username.value) == password.value:
                app.storage.user.update({'username': username.value, 'authenticated': True})
                ui.open(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
            else:
                ui.notify('Wrong username or password', color='negative')

        if app.storage.user.get('authenticated', False):
            return RedirectResponse('/')
        with ui.card().classes('absolute-center'):
            username = ui.input('Username').on('keydown.enter', try_login)
            password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
            ui.button('Log in', on_click=try_login)

        ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )
        #ui.markdown('# Below the html')
        #ui.run(host='0.0.0.0', port=8507, native=False, storage_secret='test')