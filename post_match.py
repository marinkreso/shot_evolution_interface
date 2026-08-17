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

from averages import compute_averages
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
    from urllib.parse import quote
    portal_url = f'https://portal.goldensetanalytics.com/{quote(sel_playerx)}'
    with ui.page_sticky(position='top-left').classes('z-50'):
        ui.button(icon='arrow_back', on_click=lambda: ui.navigate.to(portal_url)).props('fab')



    
    
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
    if 'ALL' not in data1_all or 'ALL' not in data2_all:
        ui.label(f'REPORT DATA NOT AVAILABLE FOR: {match_str}').classes('mx-auto mt-16 text-2xl')
        ui.label('THE LEADERBOARD HAS NO ROWS FOR THIS MATCH.').classes('mx-auto text-lg')
        return

    # reference averages, keyed by RAW stat key (pretty labels collide between
    # tabs, e.g. 'Win%' is used by both 2nd-serve and 2nd-return stats)
    _avg_keys = sorted({k for key_list in data_order.values() for k in key_list})

    def _both_averages():
        return (compute_averages(dm['selected_player_name'], match, _avg_keys),
                compute_averages(dm['opponent_name'], match, _avg_keys))

    _avg_p1, _avg_p2 = await run.io_bound(_both_averages)
    dm['_averages'] = {'p1': _avg_p1, 'p2': _avg_p2}
    dm['_show_averages'] = True  # averages view is the default (falls back to plain rows when a report has no averages)

    df_games = pd.read_csv(f"matches_new2/{match_str}/{dm['path_to_games']}")
    if not 'combined' in match_str.lower():
        import re
        # find the year anywhere in the id: tournament names may end in a digit
        # (e.g. Adelaide1_2022_...), which breaks a leading \D+ pattern
        year_match = re.search(r'(20\d{2})', match)
        if year_match:
            tournament = match[:year_match.start()].replace('_', ' ').strip().upper()
            year = year_match.group(1)
            title_suffix = f' - {tournament} {year}'
        else:
            title_suffix = ''
        ui.image('gsa_logo_smaller.png').classes('w-2/3 md:w-1/4').classes('mx-auto')
        ui.markdown('# Post match report').classes('mx-auto')
        ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()}{title_suffix}').classes('mx-auto')
    else:
        ui.image('gsa_logo_smaller.png').classes('w-2/3 md:w-1/4').classes('mx-auto')
        ui.markdown('# Combined report').classes('mx-auto')
        #ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()}').classes('mx-auto')
        
    ui.add_head_html('''
    <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <style>
        /* layout for the SHOW AVERAGES stat rows (rendered in utils_bootstrap_new2):
           phones show the name above with the sides split half/half;
           md+ is side | name | side */
        .avg-stat-row { display: flex; flex-wrap: wrap; align-items: flex-start; width: 100%; margin: 0 auto; row-gap: 6px; column-gap: 12px; }
        .avg-name { width: 100%; order: 0; display: flex; justify-content: center; text-align: center; font-size: 12px; }
        .avg-stack { display: flex; flex-direction: column; gap: 2px; width: 100%; }
        .avg-left { order: 1; width: calc(50% - 6px); }
        .avg-right { order: 2; width: calc(50% - 6px); }
        @media (min-width: 768px) {
            .avg-stat-row { flex-wrap: nowrap; width: 83.3333%; align-items: center; column-gap: 0; }
            .avg-name { width: 16.6667%; order: 1; font-size: 16px; }
            .avg-left, .avg-right { width: 41.6667%; }
            .avg-left { order: 0; }
            .avg-right { order: 2; }
        }
        /* three bars per side: this match / player year avg / top-10 avg */
        .gsa-bar { position: relative; flex: 1 1 auto; min-width: 0; height: 14px; background: #e9ecef; border-radius: 4px; }
        .gsa-bar .gsa-fill { position: absolute; top: 0; bottom: 0; left: 0; border-radius: 4px; }
        .gsa-bar.reverse .gsa-fill { left: auto; right: 0; }
        .gsa-bar.ref { height: 9px; }
        .gsa-value.ref { font-weight: 400; font-size: 11px; color: #868e96; }
        .gsa-caption { margin-bottom: 5px; }
        .gsa-value { flex: 0 0 2.6rem; font-size: 0.875rem; font-weight: 600; }
        .gsa-caption { font-size: 11px; color: #868e96; line-height: 1.2; }
        .gsa-bar-row { display: flex; align-items: center; gap: 8px; width: 100%; flex-wrap: nowrap; }
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
    # Tabs are built lazily: only the visible tab is rendered, visited tabs are
    # kept until the set / averages selection changes (then everything rebuilds).
    lazy_tabs = {'fill': None}

    @ui.refreshable
    def report_view():
            chosen = chosen_set_object.chosen_set
            if chosen not in data1_all or chosen not in data2_all:
                chosen = 'ALL'  # a set can exist in movement.json but not in the leaderboard
            data1 = data1_all[chosen]
            data2 = data2_all[chosen]

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

            averages = dm.get('_averages') or {}

            def build_items(order_key, mark_missing=True, swallow_errors=False):
                items = dict()
                for key in data_order[order_key]:
                    try:
                        item = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
                        # attach reference averages by RAW key here: pretty labels
                        # collide across tabs, so they cannot be used as lookup keys
                        item['avg'] = {
                            side: {'year': avg['year'].get(key), 'year_label': avg['year_label'],
                                   'top10': avg['top10'].get(key), 'top10_label': avg['top10_label']}
                            for side, avg in averages.items() if avg
                        }
                        items[pretty_dict.get(key, key)] = item
                        if mark_missing:
                            if data2[key + '_total'] == 0:
                                items[pretty_dict.get(key, key)]['p2'] = np.nan
                            if data1[key + '_total'] == 0:
                                items[pretty_dict.get(key, key)]['p1'] = np.nan
                    except:
                        if not swallow_errors:
                            raise
                return items

            def build_heat():
                for img_key in ['heatmap_rallies', 'heatmap_first_return', 'heatmap_second_return',
                                'heatmap_first_splus', 'heatmap_second_splus']:
                    ui.image(images[img_key]).classes('w-full md:w-1/2').classes('mx-auto')

            builders = {
                's1': lambda: serve_new_html(ui, dm, '1st Serve', None, build_items('serve', swallow_errors=True), images, chosen_set_object.chosen_set),
                's2': lambda: serve_new_html_2nd(ui, dm, '2nd Serve', build_items('serve_2nd'), images, chosen_set_object.chosen_set),
                'r1': lambda: return_new_html(ui, dm, '1st Return Quality', build_items('return'), images, chosen_set_object.chosen_set),
                'r2': lambda: return_new_html2(ui, dm, '2nd Return Quality', build_items('return_2nd'), images, chosen_set_object.chosen_set),
                'gs': lambda: groundstroke_new_html(ui, dm, 'GS Table', build_items('groundstroke_table')),
                'm': lambda: movement_new_html(ui, dm, df_games),
                'ms': lambda: shot_movement_new_html(ui, dm, 'SHOT MOVEMENT', build_items('movement', mark_missing=False)),
                'o': lambda: other_new_html(ui, dm, 'OTHER', build_items('other')),
            }
            if sel_playerx == 'NAVARRO':
                builders['heat'] = build_heat

            current = selected_tab.number if selected_tab.number in builders else 's1'
            built = {current}
            panels = {}
            with ui.tab_panels(tabs).classes('w-full').bind_value(selected_tab, 'number'):
                for tab_id, builder in builders.items():
                    with ui.tab_panel(tab_id) as panel:
                        panels[tab_id] = panel
                        if tab_id == current:
                            builder()

            def fill_tab(tab_id):
                if tab_id in built or tab_id not in builders:
                    return
                with panels[tab_id]:
                    builders[tab_id]()
                built.add(tab_id)

            lazy_tabs['fill'] = fill_tab
            tabs.set_value(current)

    tabs.on_value_change(lambda e: lazy_tabs['fill'] and lazy_tabs['fill'](e.value))

    def update_ui(e):
            chosen_set_object.chosen_set = e.value
            report_view.refresh()
    with sticky_controls:
        # only offer sets that actually have leaderboard rows for both players
        set_options = [s for s in dm.get('sets', ['ALL', '1', '2', '3'])
                       if s in data1_all and s in data2_all] or ['ALL']
        toggle = ui.toggle(set_options, value='ALL', on_change=lambda e: update_ui(e)).classes('mx-auto')
    report_view()


            
