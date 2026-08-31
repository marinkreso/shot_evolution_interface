from nicegui import ui
from utils_bootstrap_new import *
from utils_bootstrap_new2 import *
from report_util_new import main2, main3
from fastapi import FastAPI
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import json
import pandas as pd
from datetime import datetime, timedelta
#img = Image.open('GSAfulllogssso-white.png')asss



#ui.image(img).classes('w-64').classes('mx-auto')s

#df = #load_df()s


from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui, run
with open('movement_metadata.json') as f:
    data_movement = json.load(f)
    db = {'MatchData': sorted(data_movement, key=lambda x: x['DATE'], reverse=True)}

@ui.refreshable
def tab_report(data, selected_matches, image_dir):
    print('SELECTED MATCHES', selected_matches)
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
    if selected_matches:
        with ui.tab_panels(tabs, value='x1').classes('w-full'):
            with ui.tab_panel('x1').classes('mx-auto'):
                ui.label('Match Duration Info and Movement Patterns').classes('mx-auto').tailwind('font-bold')
                rows=[]
                for key in data['basic_info']:
                    if key != 'path_to_games':
                        rows.append({
                            'Metric': key,
                            'Value': data['basic_info'][key ]
                        })
                for key in data['inside_movement']:
                    if key != 'path_to_games':
                        rows.append({
                            'Metric': key,
                            'Value': data['inside_movement'][key ]
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
                        columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in list(data['number_of_moves_in_each_direction_per_point'].keys())],
                        rows=[{k: data['number_of_moves_in_each_direction_per_point'][k] for k in data['number_of_moves_in_each_direction_per_point']}],
                    ).classes('mx-auto')
                    
                    with ui.column():
                        ui.label('Number of moves in each direction (total)').classes('mx-auto').tailwind('font-bold')
                        ui.table(
                        columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in list(data['number_of_moves_in_each_direction_total'].keys())],
                        rows=[{k: data['number_of_moves_in_each_direction_total'][k] for k in data['number_of_moves_in_each_direction_total']}],
                    ).classes('mx-auto')
            with ui.tab_panel('x2').classes('mx-auto'):
                create_nicegui_board(["movement_to_fh_avg_speed",
        "movement_to_fh_avg_acc",
        "movement_to_fh_avg_decc"], 'MOVEMENT TO THE FOREHAND')
                create_nicegui_board(["movement_to_bh_avg_speed",
        "movement_to_bh_avg_acc",
        "movement_to_bh_avg_decc"], 'MOVEMENT TO THE BACKHAND')
                create_nicegui_board(["movement_first_serve_speed",
        "movement_first_serve_acc",
        "movement_first_serve_decc"], 'RECOVERY SPEED AFTER 1ST SERVE')
                create_nicegui_board(["movement_second_serve_speed",
        "movement_second_serve_acc",
        "movement_second_serve_decc"], 'RECOVERY SPEED AFTER 2ND SERVE')
                create_nicegui_board(["movement_to_fh_direction_right_avg_speed",
        "movement_to_fh_direction_right_avg_acc",
        "movement_to_fh_direction_right_avg_decc"], 'HITTING FOREHANDS MOVING TO THE RIGHT (LEFT FOR LEFTIES)')
                create_nicegui_board(["movement_to_bh_direction_right_avg_speed",
        "movement_to_bh_direction_right_avg_acc",
        "movement_to_bh_direction_right_avg_decc"], 'HITTING BACKHANDS MOVING TO THE LEFT (RIGHT FOR LEFTIES)')
                create_nicegui_board(["movement_to_fh_direction_backward_avg_speed",
        "movement_to_fh_direction_backward_avg_acc",
        "movement_to_fh_direction_backward_avg_decc"], 'HITTING FOREHAND MOVING BACKWARD')
                create_nicegui_board(["movement_to_fh_direction_backward_avg_speed",
        "movement_to_fh_direction_backward_avg_acc",
        "movement_to_fh_direction_backward_avg_decc"], 'HITTING FOREHAND MOVING BACKWARD')
                create_nicegui_board(["movement_to_fh_direction_forward_avg_speed",
        "movement_to_fh_direction_forward_avg_acc",
        "movement_to_fh_direction_forward_avg_decc"], 'HITTING FOREHAND MOVING FORWARD')
                create_nicegui_board(["movement_to_bh_direction_backward_avg_speed",
        "movement_to_bh_direction_backward_avg_acc",
        "movement_to_bh_direction_backward_avg_decc"], 'HITTING BACKHAND MOVING BACKWARD')
                create_nicegui_board([
                    'movement_to_bh_direction_backward_avg_speed',
                    'movement_to_bh_direction_backward_avg_acc',
        "movement_to_bh_direction_forward_avg_decc"], 'HITTING BACKHAND MOVING FORWARD')
            with ui.tab_panel('x3').classes('mx-auto'):
                colors=['#008FD5', '#FF2700', '#77AB43']
                rally_length = data['rally_length']
                
                ui.markdown(f'## MAXIMUM ACCELERATION PER RALLY LENGTH').classes('mx-auto')
                keyx = 'acceleration_max'
                x1, x2, x3 = rally_length[keyx][0], rally_length[keyx][1], rally_length[keyx][2]
                r1, r2, r3 = (abs(x1) / max([abs(x1), abs(x2), abs(x3)]), abs(x2) / max([abs(x1), abs(x2), abs(x3)]), abs(x3) / max([abs(x1), abs(x2), abs(x3)]))
                rally_ratio = [r1, r2, r3]
                for i in range(3):
                    with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                        with ui.row().classes('place-content-center').classes('w-2/12'):
                            ui.label(rally_length['rally_duration'][i]).classes('mx-auto')#.classes('w-2/12')#.classes('')
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
                            ui.label(rally_length['rally_duration'][i]).classes('mx-auto')#.classes('w-2/12')#.classes('')
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
                            ui.label(rally_length['rally_duration'][i]).classes('mx-auto')#.classes('w-2/12')#.classes('')
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
                            ui.label(rally_length['rally_duration'][i]).classes('mx-auto')#.classes('w-2/12')#.classes('')
                        ui.linear_progress(rally_ratio[i], color=colors[i], show_value=False, size="20px").classes('w-8/12').props('rounded')
                        ui.label(str(round(rally_length[keyx][i], 2))+ ' ' + 'm/s2').classes('w-2/12')#.classes('mx-auto')#.classes('')
                ui.separator().classes('w-2/3').classes('mx-auto')
            with ui.tab_panel('x4').classes('mx-auto'):
                xd = data['shots_data_numbers']
                rows = []
                for key in xd:
                    rows.append({'Stroke': key, 'Number of Shots': xd[key]})
                ui.table(
                columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Stroke', 'Number of Shots']],
                rows=rows,
                ).classes('mx-auto')#.classes('w-full')
            with ui.tab_panel('x5').classes('mx-auto'):
                #ui.add_head_html('<style>.my-table tbody td { font-size: 1.25em }</style>')
                #ui.add_head_html('<style>.my-table-header thead th { font-size: 1.25em }</style>')
                xd = data.get('distance_moved_per_point')
                if xd:
                    rows = []
                    for key in xd:
                        rows.append({'Distance': key, 'Frequency': xd[key]})
                    ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Distance', 'Frequency']],
                    rows=rows,
                    ).classes('mx-auto')#.classes('w-1/3')
            with ui.tab_panel('x6').classes('mx-auto'):
                xd = data.get('number_of_sprints')
                if xd:
                    rows = []
                    for key in xd:
                        rows.append({'Speed': key, 'Number': xd[key]})
                    ui.table(
                    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Speed', 'Number']],
                    rows=rows,
                    ).classes('mx-auto')
            with ui.tab_panel('x7').classes('mx-auto'):
                ui.image(image_dir + 'heatmap_serve.png').classes('mx-auto').classes('w-1/3')
                with ui.row().classes('no-wrap').classes('mx-auto'):
                    ui.image(image_dir + 'heatmap_first_serve.png').classes('mx-auto').classes('w-96')
                    ui.image(image_dir + 'heatmap_second_serve.png').classes('mx-auto').classes('w-96')
            # with ui.tab_panel('x8').classes('mx-auto'):
            #     ui.image(image_dir + 'player_load.png').classes('mx-auto').classes('w-1/2')
            with ui.tab_panel('x9').classes('mx-auto'):
                longest_point = data['longest_point']
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
                ui.image(image_dir + 'fatigue.png').classes('mx-auto').classes('w-1/2')
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

@ui.refreshable
def crud_table( 
    data: list[dict],
    columns: list[dict],
    table_classes="",
    on_save: callable = None,
    on_change: callable = None,
    dialog = None,
    movement_data = None,
    image_dir = None
) -> None:

    
    def handle_save():
        any_chosen = False
        for d in data:
            if d['SELECT']:
                any_chosen = True
                break
        if any_chosen:         
            tab_report.refresh(movement_data, [d['match_id'] for d in data if d['SELECT']], image_dir)
        else:
            tab_report.refresh(movement_data, [d['match_id'] for d in data], image_dir)
        dialog.close()
    
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
                            if cls != ui.label:
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
            



class Model:
    filters = dict()
    def __init__(self, **entries):
        self.__dict__.update(entries)
        #filters = dict()

    @classmethod
    async def all(cls):
        return [cls(**item) for item in db[cls.__name__]]

    @classmethod
    async def filter(cls, **kwargs):
        #for k, v in kwargs.items():
        #   Model.filters[k] = v
        #return [cls(**item) for item in db[cls.__name__] if all(item[k] == v for k, v in kwargs.items())]
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


                


class MatchData(Model):
    pass


def create_nicegui_board_old(columns, title):
        ui.markdown(f'## {title}').classes('mx-auto')
        import random
        ui.separator().classes('w-2/3').classes('mx-auto')
        ui.markdown(f'### SPEED').classes('mx-auto')
        for c in columns:
            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-4/12'):
                    ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
                ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
        ui.separator().classes('w-2/3').classes('mx-auto')
        ui.markdown(f'### ACCELERATION').classes('mx-auto')
        for c in columns:
            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-4/12'):
                    ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
                ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
        ui.separator().classes('w-2/3').classes('mx-auto')
        ui.markdown(f'### DECELERATION').classes('mx-auto')
        for c in columns:
            with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
                with ui.row().classes('place-content-center').classes('w-4/12'):
                    ui.label(c).classes('mx-auto')#.classes('w-2/12')#.classes('')
                ui.linear_progress(random.uniform(0.4, 0.8), show_value=False, size="20px").classes('w-6/12').props('rounded')
                ui.label(round(data_movement[c], 2)).classes('w-2/12')#.classes('mx-auto')#.classes('')
        ui.separator().classes('w-2/3').classes('mx-auto')
def create_nicegui_board(columns, title):
        ui.markdown(f'## {title}').classes('mx-auto')
        import random
        #ui.separator().classes('w-2/3').classes('mx-auto')
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
tour_avg_movement = {'movement_to_fh_avg_speed': 2.6651566031643523,
 'movement_to_fh_avg_acc': 5.16803680981595,
 'movement_to_fh_avg_decc': -4.345824991927672,
 'movement_to_bh_avg_speed': 2.485755656108597,
 'movement_to_bh_avg_acc': 5.215499245852186,
 'movement_to_bh_avg_decc': -4.5514781297134235,
 'movement_first_serve_speed': 1.3119587329264748,
 'movement_first_serve_acc': 5.103347863993026,
 'movement_first_serve_decc': -5.659678747940693,
 'movement_second_serve_speed': 1.3119587329264748,
 'movement_second_serve_acc': 4.852808896210873,
 'movement_second_serve_decc': -5.659678747940693,
 'movement_to_fh_direction_right_avg_speed': 2.750996168582376,
 'movement_to_fh_direction_right_avg_acc': 5.046992337164752,
 'movement_to_fh_direction_right_avg_decc': -3.640632183908046,
 'movement_to_fh_direction_forward_avg_speed': 2.8005866666666663,
 'movement_to_fh_direction_forward_avg_acc': 5.269964444444446,
 'movement_to_fh_direction_forward_avg_decc': -4.313057777777777,
 'movement_to_fh_direction_backward_avg_speed': 2.8953300733496334,
 'movement_to_fh_direction_backward_avg_acc': 5.218899755501222,
 'movement_to_fh_direction_backward_avg_decc': -4.113276283618582,
 'movement_to_bh_direction_forward_avg_speed': 2.873771266540643,
 'movement_to_bh_direction_forward_avg_acc': 5.454234404536863,
 'movement_to_bh_direction_forward_avg_decc': -4.4642816635160685,
 'movement_to_bh_direction_backward_avg_speed': 2.4166521739130435,
 'movement_to_bh_direction_backward_avg_acc': 4.848913043478261,
 'movement_to_bh_direction_backward_avg_decc': -4.709891304347827,
 'movement_to_bh_direction_right_avg_speed': 2.2670633971291867,
 'movement_to_bh_direction_right_avg_acc': 5.285556220095694,
 'movement_to_bh_direction_right_avg_decc': -4.830346889952153}
data_movement = {'movement_to_fh_avg_speed': 2.4791169451073984,
 'movement_to_fh_avg_acc': 4.644701670644392,
 'movement_to_fh_avg_decc': -3.270167064439141,
 'movement_to_bh_avg_speed': 2.187366771159875,
 'movement_to_bh_avg_acc': 4.371332288401255,
 'movement_to_bh_avg_decc': -3.742742946708464,
 'movement_first_serve_speed': 1.0289913544668587,
 'movement_first_serve_acc': 2.967406340057637,
 'movement_first_serve_decc': -3.1531967213114753,
 'movement_second_serve_speed': 1.0289913544668587,
 'movement_second_serve_acc': 3.1367213114754096,
 'movement_second_serve_decc': -3.1531967213114753,
 'movement_to_fh_direction_right_avg_speed': 2.8003906250000004,
 'movement_to_fh_direction_right_avg_acc': 4.457265625,
 'movement_to_fh_direction_right_avg_decc': -2.5866406250000002,
 'movement_to_fh_direction_forward_avg_speed': 2.9307200000000004,
 'movement_to_fh_direction_forward_avg_acc': 4.971280000000001,
 'movement_to_fh_direction_forward_avg_decc': -3.5845599999999993,
 'movement_to_fh_direction_backward_avg_speed': 2.402680412371134,
 'movement_to_fh_direction_backward_avg_acc': 4.690721649484536,
 'movement_to_fh_direction_backward_avg_decc': -3.352474226804124,
 'movement_to_bh_direction_forward_avg_speed': 2.8656818181818178,
 'movement_to_bh_direction_forward_avg_acc': 4.877215909090909,
 'movement_to_bh_direction_forward_avg_decc': -3.9270454545454543,
 'movement_to_bh_direction_backward_avg_speed': 1.756605504587156,
 'movement_to_bh_direction_backward_avg_acc': 3.4888073394495414,
 'movement_to_bh_direction_backward_avg_decc': -3.853211009174312,
 'movement_to_bh_direction_right_avg_speed': 2.051844660194175,
 'movement_to_bh_direction_right_avg_acc': 4.975922330097087,
 'movement_to_bh_direction_right_avg_decc': -4.27326860841424}
player_average = {'movement_to_fh_avg_speed': 2.4922675879396987,
 'movement_to_fh_avg_acc': 5.655021984924622,
 'movement_to_fh_avg_decc': -4.703592964824121,
 'movement_to_bh_avg_speed': 2.4154695534506088,
 'movement_to_bh_avg_acc': 5.714194857916103,
 'movement_to_bh_avg_decc': -4.735734776725304,
 'movement_first_serve_speed': 1.404591928251121,
 'movement_first_serve_acc': 5.30193273542601,
 'movement_first_serve_decc': -6.092759999999999,
 'movement_second_serve_speed': 1.404591928251121,
 'movement_second_serve_acc': 5.352533333333333,
 'movement_second_serve_decc': -6.092759999999999,
 'movement_to_fh_direction_right_avg_speed': 2.873361344537815,
 'movement_to_fh_direction_right_avg_acc': 5.571764705882353,
 'movement_to_fh_direction_right_avg_decc': -3.81110444177671,
 'movement_to_fh_direction_forward_avg_speed': 2.6273333333333335,
 'movement_to_fh_direction_forward_avg_acc': 5.493489583333333,
 'movement_to_fh_direction_forward_avg_decc': -4.541791666666667,
 'movement_to_fh_direction_backward_avg_speed': 2.6125686591276254,
 'movement_to_fh_direction_backward_avg_acc': 5.746300484652665,
 'movement_to_fh_direction_backward_avg_decc': -4.541421647819062,
 'movement_to_bh_direction_forward_avg_speed': 2.750975416336241,
 'movement_to_bh_direction_forward_avg_acc': 5.918517049960349,
 'movement_to_bh_direction_forward_avg_decc': -4.832616970658208,
 'movement_to_bh_direction_backward_avg_speed': 2.2923415492957746,
 'movement_to_bh_direction_backward_avg_acc': 5.328890845070423,
 'movement_to_bh_direction_backward_avg_decc': -4.687394366197183,
 'movement_to_bh_direction_right_avg_speed': 2.23203095684803,
 'movement_to_bh_direction_right_avg_acc': 5.834376172607881,
 'movement_to_bh_direction_right_avg_decc': -4.8887992495309565}
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
        print('HERE', match_str, 'SHIT', match)
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
        print('jfapofjapofjagopajgopagjapogjaopgjagopagjaogajgpoagj', data2_all, dm['opponent_name'])
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
                ui.tab('v', label='Video')
        ui.label('SELECT SET').classes('mx-auto')
        @ui.refreshable
        def report_view():
                print('CHOSEN SET', chosen_set_object.chosen_set)
                data1 = data1_all[chosen_set_object.chosen_set]
                data2 = data2_all[chosen_set_object.chosen_set]
                
                #ui.label('chosen set'  + toggle.value).classes('mx-auto')
                import numpy as np
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
                    with ui.tab_panel('v'):
                        if 'video' in dm:
                            ui.label('here are the videos').classes('mx-auto')
                            videos = dm['video']
                            folder = videos['name']
                            videos = videos['videos']
                            for video in videos:
                                ui.label(video.replace('.mp4', '')).classes('mx-auto')
                                ui.video(f'https://gsavideo.blob.core.windows.net/manualvideoclips/{folder}/{video}').classes('mx-auto').classes('w-1/2')
                        else:
                            ui.label('no videos yet').classes('mx-auto')
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
                                    #print('-------------', data1, data2[key])
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
                    print('SELTAB', selected_tab.number)
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
        async def on_company_change():
            opponents = selected_opponents.value
            surfaces = selected_surfaces.value
            years = selected_years.value
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


            

            matches = await MatchData.filter(**filters)
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
            #list_of_contracts.refresh(contracts)
            #multi_select.set_options(contract_ids, value=contract_ids)
            crud_table.refresh(rows, columns, table_classes="text-center w-full", dialog=dialog, movement_data=data, image_dir=image_dir)
        opponents = []
        for x in await MatchData.all():
            opponents.append(x.OPPONENT)
        opponents = sorted(opponents)
        tournaments = set()
        for x in await MatchData.all():
            tournaments.add(x.TOURNAMENT)
        tournaments = list(tournaments)
        
        surfaces = {surface: surface for surface in ['clay', 'grass', 'hard']}
        years = {str(year): str(year) for year in range(2021, 2025)}
        years['Last 8 Weeks'] = 'Last 8 Weeks'
        years['Last 4 Weeks'] = 'Last 4 Weeks'
        image_dir = f'https://operationslakedb.blob.core.windows.net/he-movement-report/MEDVEDEV_movement/'
        data = {'report_title': 'MEDVEDEV MOVEMENT REPORT', 
 'basic_info': {'Match Duration (per match)': '129 minutes',
  'Match Effective Time (per match)': '27 minutes',
  'Effective Time / Match Duration': '21%',
  'Total Distance Run (per match)': '2529 m',
  'Average Speed': '2.13 m/s',
  'Number of strokes (per match)': '518',
  'Changes of direction (per point)': 5.39,
  'Longest Single Run': '14 m'},
 'number_of_moves_in_each_direction_per_point': {'forward': 2.51,
  'backward': 1.29,
  'left': 1.87,
  'right': 2.14},
 'number_of_moves_in_each_direction_total': {'forward': 1720,
  'backward': 886,
  'left': 1286,
  'right': 1471},
 'inside_movement': {'Time more than 1m inside the court': '8%',
  'Time from 1m inside the BL to BL': '15%',
  'Time from BL to 1m behind the BL': '18%',
  'Time from 1m to 2m behind the BL': '19%',
  'Time from 2m to 3m behind the BL': '19%',
  'Time more than 3m behind the BL': '22%'},
 'rally_length': {'rally_duration': ['0-5 rally shot',
   '5-10 rally shot',
   '10+ rally shot'],
  'acceleration_max': [32.5, 29.9, 30.7],
  'decelerations_max': [29.5, 3.8, 4.8],
  'speeds_avg': [16.4, 6.8, 5.4],
  'speeds_max': [22.5, 13.7, 11.3]},
 'shots_data_numbers': {'1st Serve': 347,
  '2nd Serve': 122,
  'Forehand': 675,
  'Backhand': 912,
  'Forehand Return': 161,
  'Backhand Return': 134,
  'Volleys': 43},
 'distance_moved': {'0-1 m': '6% (82 times)',
  '1-2 m': '29% (377 times)',
  '2-3 m': '26% (337 times)',
  '3-4 m': '20% (258 times)',
  '4-5 m': '9% (114 times)',
  '5-10 m': '10% (130 times)'},
 'distance_moved_per_point': {'0-10 m': '321 times (49% win)',
  '11-25 m': '236 times (47% win)',
  '26-50 m': '114 times (53% win)',
  '51-75 m': '13 times (54% win)',
  '76-100 m': '2 times (50% win)',
  '101-500 m': '0 times'},
 'number_of_sprints': {'0 - 1 m/s': '940 times (48% win)',
  '1 - 1.5 m/s': '1088 times (49% win)',
  '1.5 - 2 m/s': '818 times (49% win)',
  '2 - 2.5 m/s': '535 times (49% win)',
  '2.5 - 3 m/s': '374 times (49% win)',
  '3 - 3.5 m/s': '169 times (53% win)',
  '3.5 - 4 m/s': '121 times (49% win)',
  '4 - 4.5 m/s': '59 times (49% win)',
  '4.5 - 5 m/s': '44 times (45% win)'},
 'longest_point': [{'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 53.632,
   'SET_GAME_POINT': '5_1_5',
   'rally_length': 40,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'SINNER'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 43.528,
   'SET_GAME_POINT': '3_10_4',
   'rally_length': 32,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'MEDVEDEV'},
  {'match_id': 'Miami_2024_SF_Medvedev_Sinner',
   'point_duration_time_x': 41.084,
   'SET_GAME_POINT': '2_6_5',
   'rally_length': 32,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'SINNER'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 38.273,
   'SET_GAME_POINT': '4_5_1',
   'rally_length': 28,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'SINNER'},
  {'match_id': 'Indian_Wells_2024_SF_Paul_Medvedev',
   'point_duration_time_x': 35.824,
   'SET_GAME_POINT': '3_6_14',
   'rally_length': 25,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'MEDVEDEV'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 35.181,
   'SET_GAME_POINT': '5_7_4',
   'rally_length': 27,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'SINNER'},
  {'match_id': 'Indian_Wells_2024_SF_Paul_Medvedev',
   'point_duration_time_x': 34.446,
   'SET_GAME_POINT': '2_9_3',
   'rally_length': 6,
   'PLAYER_WIN_NAME': 'PAUL',
   'server_name': 'MEDVEDEV'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 32.886,
   'SET_GAME_POINT': '5_5_4',
   'rally_length': 25,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'SINNER'},
  {'match_id': 'Dubai_2024_QF_Medvedev_Davidovich-Fokina',
   'point_duration_time_x': 32.243,
   'SET_GAME_POINT': '2_2_4',
   'rally_length': 23,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'DAVIDOVICH FOKINA'},
  {'match_id': 'Indian_Wells_2024_SF_Paul_Medvedev',
   'point_duration_time_x': 32.221,
   'SET_GAME_POINT': '3_7_4',
   'rally_length': 21,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'PAUL'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 30.505,
   'SET_GAME_POINT': '4_4_7',
   'rally_length': 25,
   'PLAYER_WIN_NAME': 'SINNER',
   'server_name': 'MEDVEDEV'},
  {'match_id': 'Dubai_2024_QF_Medvedev_Davidovich-Fokina',
   'point_duration_time_x': 28.486,
   'SET_GAME_POINT': '2_9_3',
   'rally_length': 20,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'MEDVEDEV'},
  {'match_id': 'Indian_Wells_2024_SF_Paul_Medvedev',
   'point_duration_time_x': 27.734,
   'SET_GAME_POINT': '2_8_2',
   'rally_length': 20,
   'PLAYER_WIN_NAME': 'PAUL',
   'server_name': 'PAUL'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 25.837,
   'SET_GAME_POINT': '1_3_3',
   'rally_length': 19,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'SINNER'},
  {'match_id': 'AO_2024_F_Sinner_Medvedev',
   'point_duration_time_x': 25.699,
   'SET_GAME_POINT': '2_6_4',
   'rally_length': 20,
   'PLAYER_WIN_NAME': 'MEDVEDEV',
   'server_name': 'SINNER'}],
   'matches': ['AO_2024_F_Sinner_Medvedev',
  'Miami_2024_SF_Medvedev_Sinner',
  'Indian_Wells_2024_SF_Paul_Medvedev',
  'Dubai_2024_QF_Medvedev_Davidovich-Fokina']}
        
        with ui.dialog() as dialog, ui.card().classes('w-screen h-screen'):
            with ui.row().classes('w-full'):
                selected_surfaces = ui.select(label='Surfaces', options=surfaces, multiple=True, on_change=on_company_change).classes('w-40').props('use-chips').props('rounded outlined')
                selected_years = ui.select(label='Seasons', options=years, multiple=True, on_change=on_company_change).classes('w-40').props('use-chips').props('rounded outlined')
                selected_opponents = ui.select(label='Opponents', options=list(set(opponents)), with_input=True, multiple=True, on_change=on_company_change).classes('w-40').props('use-chips').props('rounded outlined')
                #selected_tournaments = ui.select(label='Tournaments', options=list(set(tournaments)), with_input=True, multiple=True, on_change=on_company_change).classes('w-40').props('use-chips').props('rounded outlined')
                #ui.button("Apply").classes('w-40').props("size=lg")#.props('outline rounded')
            matches = await MatchData.all()
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
            
            crud_table(rows, columns, table_classes="text-center mx-auto", dialog=dialog, movement_data=data, image_dir=image_dir)
        
        ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
        #ui.markdown(f'# {data["report_title"]}').classes('mx-auto')
        ui.markdown(f'# MEDVEDEV MOVEMENT REPORT').classes('mx-auto')
        ui.button('SELECT MATCHES', on_click=dialog.open, color='white', icon='filter_list').classes('mx-auto')
        tab_report(data, [], image_dir)
        
                
            
                


            
       

                
            
            
    


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