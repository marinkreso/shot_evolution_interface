"""Post-match report page (/gui/match_new/{id}), ported from frontend.py.

The page UI is unchanged; only the surrounding plumbing was cleaned up:
no database, match visuals load from Azure blob storage (public URLs), and the
per-match data comes from the local matches_new2/ folder.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from nicegui import run
from nicegui import ui as _ui

from report_util_new import main3
from utils_bootstrap_new2 import *


class _UiCompat:
    """NiceGUI 3.x shim for page code written against 1.x: ui.html was unsanitized."""

    def __getattr__(self, name):
        return getattr(_ui, name)

    @staticmethod
    def html(content='', **kwargs):
        kwargs.setdefault('sanitize', False)
        return _ui.html(content, **kwargs)


ui = _UiCompat()

with open('post_match_metadata_with_hash.json') as f:
    post_match_hashes = json.load(f)

match_id_dict = dict()
for player in post_match_hashes:
    for match_data in post_match_hashes[player]:
        match_id_dict[match_data['hash_id']] = f"{match_data['PLAYER'].replace('-', ' ')}_{match_data['match_id']}"


@ui.page('/gui/match_new/{match_str}', response_timeout=15, dark=False, favicon='https://operationslakedb.blob.core.windows.net/gsa-post-match/fav.png')
async def main_page_new(match_str: str):
    if not '_' in match_str:
        if match_str not in match_id_dict:
            ui.label(f'REPORT NOT FOUND: {match_str}').classes('mx-auto mt-16 text-2xl')
            ui.label('PLEASE CHECK THAT THE LINK WAS COPIED COMPLETELY.').classes('mx-auto text-lg')
            return
        match_str = match_id_dict[match_str]
    if not Path(f'matches_new2/{match_str}').exists():
        ui.label(f'REPORT NOT FOUND: {match_str}').classes('mx-auto mt-16 text-2xl')
        return
    sel_playerx = match_str.split('_')[0]
    ui.page_title(sel_playerx + ' POST MATCH')
    
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
    sel_playerx = match_str.split('_')[0]
    ui.colors(accent='#6AD4DD')
    #with ui.page_sticky(x_offset=18, y_offset=18):
    with ui.page_sticky(position='top-left').classes('z-50'):
        ui.button(icon='arrow_back', on_click=lambda: ui.navigate.to('/')).props('fab')



    
    
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
        'heatmap_first_return': image_dir + 'first_return_fig.png',
        'heatmap_second_return': image_dir + 'second_return_fig.png',
        'heatmap_first_splus': image_dir + 'first_splus_fig.png',
        'heatmap_second_splus': image_dir + 'second_splus_fig.png',
        'heatmap_rallies': image_dir + 'rallies_fig.png'

    }
    pretty_dict, data1_all, data2_all, data_order = await run.io_bound(main3, [dm['selected_player_name']], [dm['opponent_name']], [match])
    #fprint('DATA1 ALL', data1_all)

    # reference averages (rendered by ui_table_jinja_nicegui when the toggle is on)
    from averages import compute_averages
    _avg_keys = sorted({k for key_list in data_order.values() for k in key_list})
    _avg_p1 = await run.io_bound(compute_averages, dm['selected_player_name'], match, _avg_keys)
    _avg_p2 = await run.io_bound(compute_averages, dm['opponent_name'], match, _avg_keys)

    def _pretty_averages(avg):
        if not avg:
            return None
        return {
            'year': {pretty_dict.get(k, k): avg['year'][k] for k in _avg_keys},
            'year_label': avg['year_label'],
            'top10': {pretty_dict.get(k, k): avg['top10'][k] for k in _avg_keys},
            'top10_label': avg['top10_label'],
        }

    dm['_averages'] = {'p1': _pretty_averages(_avg_p1), 'p2': _pretty_averages(_avg_p2)}
    dm['_show_averages'] = False

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
        .sticky-controls {
            position: sticky;
            top: 0;
            z-index: 40;
            background-color: #ffffff;
            padding-bottom: 4px;
        }
        .body--dark .sticky-controls {
            background-color: #121212;
        }
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
    
    
    with ui.column().classes('w-full items-center sticky-controls').style('gap: 0.25rem;') as sticky_controls:
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
                if sel_playerx == 'NAVARRO':
                    ui.tab('heat', label='MOVEMENT HEATMAP')
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
                                if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                                if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
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
                            if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
                    serve_new_html_2nd(ui, dm, '2nd Serve', items, images, chosen_set_object.chosen_set)
                with ui.tab_panel('r1'):
                    active_tab_test = 'r1'
                    items = dict()
                    for key in data_order['return']:
                        #if '1st' in key.lower():
                        if True:
                            items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                            if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
                    return_new_html(ui, dm, '1st Return Quality', items, images, chosen_set_object.chosen_set)
                if sel_playerx == 'NAVARRO':
                    with ui.tab_panel('heat'):
                        ui.image(images['heatmap_rallies']).classes('w-1/2').classes('mx-auto')
                        ui.image(images['heatmap_first_return']).classes('w-1/2').classes('mx-auto')
                        ui.image(images['heatmap_second_return']).classes('w-1/2').classes('mx-auto')
                        ui.image(images['heatmap_first_splus']).classes('w-1/2').classes('mx-auto')
                        ui.image(images['heatmap_second_splus']).classes('w-1/2').classes('mx-auto')
                        

                with ui.tab_panel('o'):
                    active_tab_test = 'o'
                    items = dict()
                    for key in data_order['other']:
                        #if '1st' in key.lower():
                        if True:
                            items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                            if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
                    other_new_html(ui, dm, 'OTHER', items, images, chosen_set_object.chosen_set)
                with ui.tab_panel('r2'):
                    active_tab_test = 'r2'
                    items = dict()
                    for key in data_order['return_2nd']:
                        #if '1st' in key.lower():
                        if True:
                            items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                            if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
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
                            if data2[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                    items[pretty_dict.get(key, key)]['p1'] = np.nan
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
    def _toggle_averages(e):
        dm['_show_averages'] = e.value
        report_view.refresh()

    with sticky_controls:
        if 'sets' in dm:
            toggle = ui.toggle(dm['sets'], value='ALL', on_change=lambda e: update_ui(e)).classes('mx-auto')
        else:
            toggle = ui.toggle(['ALL', '1', '2', '3'], value='ALL', on_change=lambda e: update_ui(e)).classes('mx-auto')
        ui.switch('SHOW AVERAGES', on_change=_toggle_averages).classes('mx-auto')
    report_view()


            
