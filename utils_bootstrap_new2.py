



import numpy as np
from jinja2 import Environment, BaseLoader


def movement_new_html(ui, movement_json, df):
    #df1 = df[['Game Description', 'Distance covered per point', 'Average movement speed', 'Serve Speed avg']]
    ui.label('Match Duration Information').classes('mx-auto').classes('font-bold')
    for key in movement_json['Movement_data']:
        if key != 'path_to_games':
            ui.label(f'- {key}: {movement_json["Movement_data"][key]}').classes('mx-auto')
    ui.label('').classes('mx-auto')
    movement_columns = ['Game Description', 'Distance covered per point', 'Average movement speed']
    for x in ['Average deceleration', 'Average acceleration']:
        if x in df.columns:
            movement_columns.append(x)
    def replace_game_str(x):
        x = 'Games ' + x.split(' ')[0]
        if x == 'Games 1-6':
           return 'First 6 Games'
        return x
    df['Game Description New'] = df['Game Description'].apply(replace_game_str)
    df1 = df[movement_columns]
    df2 = df[['Game Description New', 'Serve Speed Avg', 'Forehand Speed Avg', 'Backhand Speed Avg (without slices)', 'Backhand Speed Avg (with slices)']]
    
    ui.label('Movement Analysis over Six-Game Intervals').classes('mx-auto').classes('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df1.columns],
    rows=df1.to_dict('records'),
).classes('mx-auto')
    ui.label('Shot Analysis over Six-Game Intervals').classes('mx-auto').classes('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df2.columns],
    rows=df2.to_dict('records'),
).classes('mx-auto')#.classes('w-full md:w-1/2')
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja_nicegui(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    #ui_table_jinja_nicegui(ui, movement_json, items, x)
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')
    xd = movement_json['shots_data_numbers']
    rows = []
    for key in xd:
        rows.append({'Stroke': key, 'Number of Shots': xd[key]})
    ui.label('Stroke quantifications').classes('mx-auto').classes('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Stroke', 'Number of Shots']],
    rows=rows,
    ).classes('mx-auto')#.classes('w-full')

    with ui.row().classes('mx-auto'):
      with ui.column().classes('mx-auto'):
        xd = movement_json['distance_moved']
        rows = []
        for key in xd:
            rows.append({'Distance': key, 'Percentage': xd[key]})
        ui.label('Distance quantifications with percentages').classes('mx-auto').classes('font-bold')
        ui.table(
        columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Distance', 'Percentage']],
        rows=rows,
        ).classes('mx-auto')#.classes('w-full')
      with ui.column().classes('mx-auto'):
        xd = movement_json.get('distance_moved_per_point')
        if xd:
          rows = []
          for key in xd:
              rows.append({'Distance': key, 'Frequency': xd[key]})
          ui.label('Distance per point with win percentage').classes('mx-auto').classes('font-bold')
          ui.table(
          columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Distance', 'Frequency']],
          rows=rows,
          ).classes('mx-auto')
      with ui.column().classes('mx-auto'):
        xd = movement_json.get('number_of_sprints')
        if xd:
          rows = []
          for key in xd:
              rows.append({'Speed': key, 'Number': xd[key]})
          ui.label('Number of Sprints').classes('mx-auto').classes('font-bold')
          ui.table(
          columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Speed', 'Number']],
          rows=rows,
          ).classes('mx-auto')
      
    
    #ui.image('movement_visual.png').classes('mx-auto').classes('w-full md:w-1/2')
def bh_new_html(ui,movement_json, x, items):
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja_nicegui(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    ui_table_jinja_nicegui(ui, movement_json, items, x)
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')

# Radar overview of movement avg speeds, oriented like standing at the
# baseline looking down the court:
# net at the top, baseline at the bottom, forehand side to the right,
# backhand side to the left, forward movement near the top of each side.
_RADAR_AXES_CLOCKWISE = [
    ('Recovery 1st serve', 'movement_first_serve_speed'),
    ('Fhand moving fwd', 'movement_to_fh_direction_forward_avg_speed'),
    ('Move to forehand', 'movement_to_fh_avg_speed'),
    ('Fhand moving right', 'movement_to_fh_direction_right_avg_speed'),
    ('Fhand moving back', 'movement_to_fh_direction_backward_avg_speed'),
    ('Recovery 2nd serve', 'movement_second_serve_speed'),
    ('Bhand moving back', 'movement_to_bh_direction_backward_avg_speed'),
    ('Bhand moving left', 'movement_to_bh_direction_right_avg_speed'),
    ('Move to backhand', 'movement_to_bh_avg_speed'),
    ('Bhand moving fwd', 'movement_to_bh_direction_forward_avg_speed'),
]


def movement_radar(ui, movement_json, items):
    def val(key, side):
        try:
            return round(float(items[key][side]), 2)
        except (KeyError, TypeError, ValueError):
            return 0
    # ECharts lays radar indicators out counterclockwise from the top, so keep
    # the top axis and reverse the rest to get the clockwise court layout
    axes = [_RADAR_AXES_CLOCKWISE[0]] + _RADAR_AXES_CLOCKWISE[:0:-1]
    p1_vals = [val(k, 'p1') for _, k in axes]
    p2_vals = [val(k, 'p2') for _, k in axes]
    mx = max(p1_vals + p2_vals + [1])
    mx = float(np.ceil(mx * 2)) / 2  # round up to the next 0.5
    p1_name = movement_json['selected_player_name']
    p2_name = movement_json['opponent_name']
    ui.html('<h1 class="text-center">MOVEMENT OVERVIEW (AVG SPEED)</h1>').classes('text-2xl').classes('mx-auto')
    ui.label('net ↑ · forehand side → · backhand side ← · baseline ↓').classes('mx-auto text-xs text-gray-500')
    ui.echart({
        'legend': {'data': [p1_name, p2_name], 'top': 0},
        'radar': {
            'indicator': [{'name': name, 'max': mx} for name, _ in axes],
            'radius': '65%',
            'center': ['50%', '55%'],
            'startAngle': 90,
            'splitNumber': 3,
            'axisName': {'color': '#555', 'fontSize': 10},
        },
        'series': [{
            'type': 'radar',
            'data': [
                {'value': p1_vals, 'name': p1_name,
                 'itemStyle': {'color': '#28a745'}, 'lineStyle': {'color': '#28a745'},
                 'areaStyle': {'color': 'rgba(40,167,69,0.12)'}},
                {'value': p2_vals, 'name': p2_name,
                 'itemStyle': {'color': '#dc3545'}, 'lineStyle': {'color': '#dc3545'},
                 'areaStyle': {'color': 'rgba(220,53,69,0.12)'}},
            ],
        }],
    }).classes('mx-auto w-full md:w-2/3').style('height: 460px')


def shot_movement_new_html(ui,movement_json, x, items):
    movement_radar(ui, movement_json, items)
    # all_items = [
    # "movement_to_bh_direction_forward_avg_speed",
    # "movement_to_bh_direction_forward_avg_acc",
    # "movement_to_bh_direction_forward_avg_decc",
    # "movement_to_bh_direction_backward_avg_speed",
    # "movement_to_bh_direction_backward_avg_acc",
    # "movement_to_bh_direction_backward_avg_decc",
    # "movement_to_bh_direction_right_avg_speed",
    # "movement_to_bh_direction_right_avg_acc",
    # "movement_to_bh_direction_right_avg_decc" ]
    #import json
    #with open('items_movement.json', 'w') as f:
    #   json.dump(items, f)
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_fh_avg_speed",
    "movement_to_fh_avg_acc",
    "movement_to_fh_avg_decc"]}, 'MOVEMENT TO THE FOREHAND')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_bh_avg_speed",
    "movement_to_bh_avg_acc",
    "movement_to_bh_avg_decc"]}, 'MOVEMENT TO THE BACKHAND')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_first_serve_speed",
    "movement_first_serve_acc",
    "movement_first_serve_decc"]}, 'RECOVERY SPEED AFTER 1ST SERVE')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_second_serve_speed",
    "movement_second_serve_acc",
    "movement_second_serve_decc"]}, 'RECOVERY SPEED AFTER 2ND SERVE')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_fh_direction_right_avg_speed",
    "movement_to_fh_direction_right_avg_acc",
    "movement_to_fh_direction_right_avg_decc"]}, 'HITTING FOREHANDS MOVING TO THE RIGHT (LEFT FOR LEFTIES)')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_fh_direction_backward_avg_speed",
    "movement_to_fh_direction_backward_avg_acc",
    "movement_to_fh_direction_backward_avg_decc"]}, 'HITTING FOREHAND MOVING BACKWARD')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_fh_direction_forward_avg_speed",
    "movement_to_fh_direction_forward_avg_acc",
    "movement_to_fh_direction_forward_avg_decc"]}, 'HITTING FOREHAND MOVING FORWARD')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_bh_direction_right_avg_speed",
    "movement_to_bh_direction_right_avg_acc",
    "movement_to_bh_direction_right_avg_decc"]}, 'HITTING BACKHANDS MOVING TO THE LEFT (RIGHT FOR LEFTIES)')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_bh_direction_backward_avg_speed",
    "movement_to_bh_direction_backward_avg_acc",
    "movement_to_bh_direction_backward_avg_decc"]}, 'HITTING BACKHAND MOVING BACKWARD')
    ui_table_jinja_movement(ui, movement_json, {x: items[x] for x in ["movement_to_bh_direction_forward_avg_speed",
    "movement_to_bh_direction_forward_avg_acc",
    "movement_to_bh_direction_forward_avg_decc"]}, 'HITTING BACKHAND MOVING FORWARD')
    


def groundstroke_new_html(ui,movement_json, x, items):
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja_nicegui(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    #it1 = ['rally winners per match', 'rally ue per match', 'BH Topspin / BH Slice ratio', 'FH CC / DTL ratio', 'BH CC / DTL ratio']
    it2 = ['BH CC SPEED', 'BH CC DEPTH', 'BH CC SPIN', 'BH DTL SPEED', 'FH CC SPEED', 'FH CC DEPTH', 'FH CC SPIN','FH DTL SPEED',   'BH DTL DEPTH', 'FH DTL DEPTH',  'BH DTL SPIN', 'FH DTL SPIN']
    
    winners_errors = ['FH IN PLAY %', 'BH IN PLAY %', 'WINNERS + FORCING ERRORS', 'FH WINNERS + FORCING ERRORS', 'BH WINNERS + FORCING ERRORS', 'UNFORCED ERRORS', 'FH ERRORS', 'BH ERRORS']
    location = ['% OF SHOTS HIT INSIDE THE COURT', '% OF SHOTS HIT FROM BEHIND THE BASELINE', '% OF SHOTS HIT FROM FURTHER BACK']
    conversion = ['FH FINISHING SHOTS ON EASY BALLS', 'BH FINISHING SHOTS ON EASY BALLS', 'FH ERRORS ON EASY BALLS', 'BH ERRORS ON EASY BALLS']
    cross_dtl_patterns = ['WIN% IN CROSS FH RALLIES', 'WIN% IN CROSS BH RALLIES', 'CHANGES OF DIRECTION FH DTL', 'CHANGES OF DIRECTION BH DTL', 'WIN% CHANGING DIRECTION FH DTL', 'WIN% CHANGING DIRECTION BH DTL']
    on_the_run = ['TIMES PLACING THE OPPONENT ON THE RUN TO FH', 'WIN% PLACING THE OPPONENT ON THE RUN TO FH' ,'TIMES PLACING THE OPPONENT ON THE RUN TO BH', 'WIN% PLACING THE OPPONENT ON THE RUN TO BH']
    dropshots_approaches = ['TIMES HITTING A DROP SHOT', 'WIN% ON DROP SHOTS', 'TIMES USING CROSS BH SLICE DEEP', 'WIN% USING CROSS BH SLICE DEEP', 'TIMES USING CROSS BH SLICE LOW SHORT ANGLE', 'WIN% USING CROSS BH SLICE LOW SHORT ANGLE', 'TIMES APPROACHING THE NET', 'WIN% APPROACHING THE NET']
      

    itfh = [x for x in it2 if 'fh' in x.lower()]
    itbh = [x for x in it2 if 'bh' in x.lower()]
    
    import json
    
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in winners_errors}, 'WINNERS & ERRORS')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in location}, 'LOCATION')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in conversion}, 'CONVERSION')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in cross_dtl_patterns}, 'CROSS AND DTL RALLY PATTERNS')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in on_the_run}, 'ON THE RUN')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in dropshots_approaches}, 'DROPSHOTS, SLICES, APPROACHES')

    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in itfh}, 'FH Stats')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in itbh}, 'BH Stats')
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')
   
def fh_new_html(ui, movement_json, x, items):
    #ui_table(ui)
    ui_table_jinja_nicegui(ui, movement_json, items, x)
    #ui.html('<h1>FH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('7.png').classes('w-96').classes('mx-auto')

def other_new_html(ui, movement_json, returnx, items, images, chosen_set):
    ui_table_jinja_nicegui(ui, movement_json, items, 'TYPE OF POINTS WON')

def return_new_html(ui, movement_json, returnx, items, images, chosen_set):
    ui.markdown(f'### 1st Return'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['first_return']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['first_return'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    return_first_table = {x: items[x] for x in items if x in ['In%', 'In% - pressure points', f'In% - break points', 'Return Win %', 'Win% - Pressure points', 'Win% - Break points', 'FH Return In%', 'BH Return In%']}
    ui_table_jinja_nicegui(ui, movement_json, return_first_table, returnx.upper())
    ui.markdown(f'### 1ST RETURNS: DEPTH AND SPEED'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['return_depth']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['return_depth'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    return_first_table = {x: items[x] for x in items if x not in ['In%', 'In% - pressure points', f'In% - break points', 'Return Win %', 'Win% - Pressure points', 'Win% - Break points', 'FH Return In%', 'BH Return In%']}
    ui_table_jinja_nicegui(ui, movement_json, return_first_table, 'RETURN CHARACTER')
    #with ui.row().classes('w-full no-wrap flex-nowrap'):
    #  ui.image('1st_deuce_returns.png').classes('w-full md:w-1/2')
    #  ui.image('1st_ad_returns.png').classes('w-full md:w-1/2')
      #ui.label('Third column with some more text').classes('bg-blue-100 w-1/3')
    #ui.html('<h1>Return directions</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_percentages.png').classes('w-96').classes('mx-auto')
    #ui.html('<h1>Return rally</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_rally.png').classes('w-9').classes('mx-auto')

def return_new_html2(ui, movement_json, returnx, items, images, chosen_set):
    
    ui.markdown(f'### 2nd Return'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['second_return']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['second_return'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    columns_first = ['In%', 'Win%', 'FH Return In%', 'BH Return In%', '% of good 2nd returns that extended the point (5+) or player won the point', '% of deep returns']
    
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in items if x in columns_first}, 'Return Quality')
    ui.markdown(f'### 2nd Deuce Return Direction'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['return_dir_deuce']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['return_dir_deuce'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    ui.markdown(f'### 2nd Ad Return Direction'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['return_dir_ad']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['return_dir_ad'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    ui_table_jinja_nicegui(ui, movement_json, {x: items[x] for x in items if x not in columns_first}, 'Return Character')
    ui.label('Aggresive returns = Returner won the point under 5 shots').classes('mx-auto')
    #with ui.row().classes('w-full no-wrap flex-nowrap'):
    #  ui.image('2nd_deuce_returns.png').classes('w-full md:w-1/2')
    #  ui.image('2nd_ad_returns.png').classes('w-full md:w-1/2')
      #ui.label('Third column with some more text').classes('bg-blue-100 w-1/3')
    #ui.html('<h1>Return directions</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_percentages.png').classes('w-96').classes('mx-auto')
    #ui.html('<h1>Return rally</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_rally.png').classes('w-96').classes('mx-auto')
  
def serve_new_html(ui, movement_json, serve, rally_win, items, images, chosen_set):
    #with ui.element('div').classes('text-center'):
    
#     ui.markdown('''
#     1ST SERVE WIN% BY DIRECTION
    
#       -  DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T 
#       -  AD: DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T       

# '''
        
#     ).classes('mx-auto').props('absolute-center')
    #ui_table(ui)

    ui.markdown(f'### 1st Serve Direction {movement_json.get("selected_player_name","Player" )}'.upper()).classes('mx-auto').classes('font-bold')
    #ui.image('1stServe.png').classes('mx-auto').classes('w-1/4')
    if chosen_set == 'ALL':
      ui.image(images['first_serve']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['first_serve'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    #ui.image('Serve1.jpg').classes('mx-auto').classes('w-full md:w-1/2')
    ui_table_jinja_nicegui(ui, movement_json, items, serve)
    ui.markdown(f'### {movement_json.get("selected_player_name","Player" )} 1st Serve Placement < 40 cm of the side lines '.upper()).classes('mx-auto').classes('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Serve Direction', 'Placement%']],
    #rows=[{'Serve Direction': 'DEUCE W', 'Placement%': '20%'}, {'Serve Direction': 'DEUCE T', 'Placement%': '12%'}, {'Serve Direction': 'AD W', 'Placement%': '19%'}, {'Serve Direction': 'AD T', 'Placement%': '7%'}],
    #).classes('mx-auto')
    rows=[{'Serve Direction': 'DEUCE W', 'Placement%': movement_json['placement_first']['1st DEUCE W']}, 
      {'Serve Direction': 'DEUCE T', 'Placement%': movement_json['placement_first']['1st DEUCE T']}, 
      {'Serve Direction': 'AD W', 'Placement%': movement_json['placement_first']['1st AD W']}, 
      {'Serve Direction': 'AD T', 'Placement%': movement_json['placement_first']['1st AD T']}],
    ).classes('mx-auto')
    if chosen_set == 'ALL':
      ui.image(images['serve_placement']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['serve_placement'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    #ui.markdown(f'### RALLY LENGTH STATISTICS'.upper()).classes('mx-auto').classes('font-bold')
    #ui.image('1stServe.png').classes('mx-auto').classes('w-1/4')
    #ui.image('rally_length_0373d014-a19d-4ae6-b0ba-aaece44913d3.png').classes('mx-auto').classes('w-full md:w-1/2')
    #ui.image('placement_first.png').classes('w-1/4').classes('mx-auto')
    #ui.image('serve_direction2.png').classes('w-full md:w-1/2').classes('mx-auto')
    #ui.image('serve_rally.png').classes('w-96').classes('mx-auto')
    #ui.image('serve_placement2.png').classes('w-full md:w-1/2').classes('mx-auto')

def serve_new_html_2nd(ui, movement_json, serve, items, images, chosen_set):
    #with ui.element('div').classes('text-center'):
    
#     ui.markdown('''
#     1ST SERVE WIN% BY DIRECTION
    
#       -  DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T 
#       -  AD: DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T       

# '''
        
#     ).classes('mx-auto').props('absolute-center')
    #ui_table(ui)

    
    ui_table_jinja_nicegui(ui, movement_json, items, '2nd Serve Quality'.upper())
    xd = movement_json.get('placement_second')
    ui.markdown(f'### 2nd Serve Direction {movement_json.get("selected_player_name","Player".upper() )}'.upper()).classes('mx-auto').classes('font-bold')
    if chosen_set == 'ALL':
      ui.image(images['second_serve']).classes('mx-auto').classes('w-full md:w-1/2')
    else:
       ui.image(images['second_serve'].replace('.png', f'_{chosen_set}.png')).classes('mx-auto').classes('w-full md:w-1/2')
    # if xd:
    #   ui.markdown(f'### 2nd Serve Direction {movement_json.get("selected_player_name","Player" )}').classes('mx-auto').classes('font-bold')
    #   rows = []
    #   for key in xd:
    #       rows.append({'Serve Type': key, 'Perc of Serves': xd[key]})
    #   #ui.label('Serve direction').classes('mx-auto').classes('font-bold')
    #   ui.table(
    #   columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Serve Type', 'Perc of Serves']],
    #   rows=rows,
    #   ).classes('mx-auto')
    
    # ui.markdown(f'### 2nd Serve Placement'.upper()).classes('mx-auto').classes('font-bold')
    # ui.image('serve_placement.png').classes('mx-auto').classes('w-1/4')
    # ui.markdown(f'### RALLY LENGTH STATISTICS'.upper()).classes('mx-auto').classes('font-bold')
    # #ui.image('1stServe.png').classes('mx-auto').classes('w-1/4')
    # ui.image('rally_length_dd348f8d-48f0-4b75-a2f6-df9ac3284af7.png').classes('mx-auto').classes('w-full md:w-1/2')
    #ui.image('placement_second.png').classes('w-1/4').classes('mx-auto')
    #ui.image('serve_rally.png').classes('w-96').classes('mx-auto')
    #ui.image('serve_placement2.png').classes('w-full md:w-1/2').classes('mx-auto')

def ui_table_jinja(ui, mj, items, table_title):
    ui.html(f'<h1 class="text-center">{table_title}</h1>').classes('text-2xl').classes('mx-auto')
    

    x = '''

<div class="container mt-4">
  
  
  <table class="table text-center">
    <thead>
      <tr>
        <th style="width: 5%"></th>
        <th style="width: 35%;color:#28a745">{{ dm.selected_player_name }}</th>
        <th style="width: 20%"></th>
        <th style="width: 35%;color:#dc3545">{{ dm.opponent_name }}</th>
        <th style="width: 5%"></th>
      </tr>
    </thead>
    <tbody>
      {% for key, item in items.items() %}
      <tr>
        
        <td>
            <h4 class="progress-label-right">{{item.p1}}</h4>
            </td>
        <td> 
            
            
            <div class="progress flex-row-reverse">
                <div class="progress-bar bg-success" role="progressbar" style="width: {{item.p1_perc}}%"  aria-valuenow="{{item.p1_perc}}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            
        </td>
        <td>
          {{ key }}
        </td>
            
        <td>
        
          <div class="progress">
                <div class="progress-bar bg-danger" role="progressbar" style="width: {{100 - item.p1_perc}}%"  aria-valuenow="{{100 - item.p1_perc}}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
          
            <td>
            
            <h4 class="progress-label">{{item.p2}}</h4>
            
            </td>
         
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

                 '''
    rtemplate = Environment(loader=BaseLoader()).from_string(x)
    ui.html(rtemplate.render(items=items, dm=mj)).classes('w-full').classes('mx-auto')

def _avg_fmt(v):
    import numpy as np
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return 'NA'
    r = round(float(v), 1)
    return str(int(r)) if r == int(r) else str(r)


def _bullet_bar(ui, fill, color, reverse):
    with ui.element('div').classes('gsa-bar' + (' reverse' if reverse else '')):
        ui.element('div').classes('gsa-fill').style(f'width: {fill * 100:.1f}%; background: {color};')



def _row_fills(key, item):
    """Bar fill fractions for a stat row: (p1_fill, p2_fill, avg_fill_fn)."""
    import numpy as np
    is_pct = ('%' in key or 'offensive serve' in key.lower() or 'defensive serve' in key.lower())
    p1, p2 = item['p1'], item['p2']
    if is_pct:
        p1_fill = 0 if np.isnan(p1) else p1 / 100
        p2_fill = 0 if np.isnan(p2) else p2 / 100
    else:
        p1_fill = 0 if np.isnan(p1) else item['p1_perc'] / 100
        p2_fill = 0 if np.isnan(p2) else 1 - (item['p1_perc'] / 100)

    def _avg_fill(v):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return 0
        if is_pct:
            return max(0.0, min(1.0, float(v) / 100))
        try:
            denom = float(p1) + float(p2)
        except (TypeError, ValueError):
            return 0
        if not denom or np.isnan(denom):
            return 0
        return max(0.0, min(1.0, float(v) / denom))

    return p1_fill, p2_fill, _avg_fill


_SIDE_COLORS = {'p1': '#28a745', 'p2': '#dc3545'}


def _render_row_with_averages(ui, movement_json, key, item):
    """Three bars per side (match / player's year-surface avg / tour top-10
    avg) with a small description under each bar and the value at its end."""
    import numpy as np
    p1_fill, p2_fill, _avg_fill = _row_fills(key, item)
    item_avgs = item.get('avg') or {}

    def _valid(v):
        return v is not None and not (isinstance(v, float) and np.isnan(v))

    def _bar_with_label(fill, value_text, color, label, reverse, ref):
        bar_ref_cls = ' ref' if ref else ''
        with ui.element('div').classes('gsa-bar-row'):
            def draw_bar():
                with ui.element('div').classes('gsa-bar' + bar_ref_cls + (' reverse' if reverse else '')):
                    ui.element('div').classes('gsa-fill').style(f'width: {fill * 100:.1f}%; background: {color};')
            if reverse:  # player side: bar fills toward the center, value beside it
                draw_bar()
                ui.label(value_text).classes('gsa-value').style('text-align: left;')
            else:
                ui.label(value_text).classes('gsa-value').style('text-align: right;')
                draw_bar()
        ui.label(label).classes('gsa-caption w-full').style(f"text-align: {'left' if reverse else 'right'};")

    def _side(side_key, player_name, value, fill, reverse):
        color = _SIDE_COLORS[side_key]
        value_text = 'NA' if (isinstance(value, float) and np.isnan(value)) else value
        avg = item_avgs.get(side_key)
        _bar_with_label(fill, value_text, color, 'THIS MATCH', reverse, ref=False)
        if not avg:
            return
        # year_label comes as e.g. '2026 HARD AVG' -> 'TSITSIPAS AVG HARD 2026'
        label_parts = str(avg.get('year_label', '')).split()
        year_desc = f'{player_name} AVG {label_parts[1]} {label_parts[0]}' if len(label_parts) >= 3 else f'{player_name} AVG'
        if _valid(avg.get('year')):
            _bar_with_label(_avg_fill(avg['year']), _avg_fmt(avg['year']), color, year_desc, reverse, ref=True)
        if _valid(avg.get('top10')):
            _bar_with_label(_avg_fill(avg['top10']), _avg_fmt(avg['top10']), color, 'TOP 10 AVG', reverse, ref=True)
        # best wins: player's side only
        best = avg.get('best') if side_key == 'p1' else None
        if _valid(best):
            _bar_with_label(_avg_fill(best), _avg_fmt(best), color, f'{player_name} BEST WINS AVG', reverse, ref=True)

    # layout comes from the .avg-* CSS in the page head: phones show
    # name above with sides split half/half; md+ is side | name | side
    with ui.element('div').classes('avg-stat-row'):
        with ui.element('div').classes('avg-name'):
            ui.label(key)
        with ui.element('div').classes('avg-stack avg-left'):
            _side('p1', str(movement_json.get('selected_player_name', 'PLAYER')).upper(), item['p1'], p1_fill, reverse=True)
        with ui.element('div').classes('avg-stack avg-right'):
            _side('p2', str(movement_json.get('opponent_name', 'OPPONENT')).upper(), item['p2'], p2_fill, reverse=False)


def ui_table_jinja_nicegui(ui, movement_json, items, table_title):
    ui.html(f'<h1 class="text-center">{table_title}</h1>').classes('text-2xl').classes('mx-auto')
    

    ui.separator().classes('w-full md:w-10/12').classes('mx-auto')

    # with ui.row().classes('w-full md:w-2/3 no-wrap flex-nowrap').classes('mx-auto'):
    #     #ui.label(movement_json['selected_player_name']).classes('w-6/12').style('color: #28a745').classes('mx-auto')
    #     ui.label('').style('color: #28a745').classes('mx-auto').classes('w-1/12')
    #     ui.label(movement_json['selected_player_name']).style('color: #28a745').classes('w-4/12').classes('justify-start')
    #     ui.label('').style('color: #28a745').classes('mx-auto').classes('w-2/12')
    #     ui.label(movement_json['opponent_name']).style('color: #dc3545').classes('w-4/12').classes('justify-start')
    #     ui.label('').style('color: #28a745').classes('mx-auto').classes('w-2/12')
    #     #ui.label('').classes('w-8/12')
    #     #ui.label(movement_json['opponent_name']).classes('w-6/12').style('color: #dc3545').classes('mx-auto')

    with ui.row().classes('w-full md:w-2/3 no-wrap flex-nowrap').classes('mx-auto'):
      ui.label('').classes('w-1/12')
      ui.label(movement_json['selected_player_name']).classes('w-4/12').style('color: #28a745').style('text-align: left;')
      ui.label('').classes('w-2/12')
      ui.label(movement_json['opponent_name']).classes('w-4/12').style('color: #dc3545').style('text-align: right;')
      ui.label('').classes('w-1/12')

    first_avg = next((it.get('avg') for it in items.values() if it.get('avg')), None)
    show_avgs = bool(movement_json.get('_show_averages') and first_avg)

    for key, item in items.items():
      import numpy as np
      if show_avgs:
        ui.separator().classes('w-full md:w-10/12').classes('mx-auto')
        _render_row_with_averages(ui, movement_json, key, item)
      elif not ('%' in key or 'offensive serve' in key.lower() or 'defensive serve' in key.lower()):
        ui.separator().classes('w-full md:w-10/12').classes('mx-auto')
        with ui.row().classes('w-full md:w-10/12 no-wrap flex-nowrap').classes('mx-auto'):
            if np.isnan(item['p1']):
              ui.linear_progress(0, color='#28a745', show_value=False, size="20px").classes('w-4/12').props('reverse').props('rounded')
              ui.label('NA').classes('w-1/12').style('text-align: left;')  #.classes('')
            else:
              ui.linear_progress(item['p1_perc'] / 100, color='#28a745', show_value=False, size="20px").classes('w-4/12').props('reverse').props('rounded')
              ui.label(item['p1']).classes('w-1/12').style('text-align: left;')  #.classes('')

            with ui.row().classes('w-2/12').classes('place-content-center'):
                ui.label(key).style('text-align: center;').classes('w-full text-xs md:text-base')#.classes('')
            if np.isnan(item['p2']):
              ui.label('NA').classes('w-1/12').style('text-align: right;')#.classes('')
              ui.linear_progress(0, color='#dc3545', show_value=False, size="20px").classes('w-4/12').props('rounded')
            else:
              ui.label(item['p2']).classes('w-1/12').style('text-align: right;')#.classes('')
              ui.linear_progress(1 - (item['p1_perc'] / 100), color='#dc3545', show_value=False, size="20px").classes('w-4/12').props('rounded')
      else:
         ui.separator().classes('w-full md:w-10/12').classes('mx-auto')
         with ui.row().classes('w-full md:w-10/12 no-wrap flex-nowrap').classes('mx-auto'):
            if np.isnan(item['p1']):
              ui.linear_progress(0, color='#28a745', show_value=False, size="20px").classes('w-4/12').props('reverse').props('rounded')
              ui.label('NA').classes('w-1/12').style('text-align: left;')  #.classes('')
            else:
              ui.linear_progress(item['p1'] / 100, color='#28a745', show_value=False, size="20px").classes('w-4/12').props('reverse').props('rounded')
              ui.label(item['p1']).classes('w-1/12').style('text-align: left;')  #.classes('')
            with ui.row().classes('w-2/12').classes('place-content-center'):
                ui.label(key).style('text-align: center;').classes('w-full text-xs md:text-base')#.classes('')
            if np.isnan(item['p2']):
              ui.label('NA').classes('w-1/12').style('text-align: right;')#.classes('')
              ui.linear_progress(0, color='#dc3545', show_value=False, size="20px").classes('w-4/12').props('rounded')
            else:
              ui.label(item['p2']).classes('w-1/12').style('text-align: right;')#.classes('')
              ui.linear_progress((item['p2'] / 100), color='#dc3545', show_value=False, size="20px").classes('w-4/12').props('rounded')
         

    with ui.column().classes('h-8 border'):
       ui.space()

def ui_table_jinja_movement(ui, movement_json, items, table_title):
    new_items = dict()
    for k in items:
       if 'speed' in k:
          new_items['AVG SPEED'] = items[k]
       elif 'acc' in k:
          new_items['AVG ACCELERATION'] = items[k]
       elif 'decc' in k:
          new_items['AVG DECELERATION'] = items[k]
    ui.html(f'<h1 class="text-center">{table_title}</h1>').classes('text-2xl').classes('mx-auto')
    

    x = '''

<div class="container mt-4">
  
  
  <table class="table text-center">
    <thead>
      <tr>
        <th style="width: 5%"></th>
        <th style="width: 35%;color:#28a745">{{ dm.selected_player_name }}</th>
        <th style="width: 20%"></th>
        <th style="width: 35%;color:#dc3545">{{ dm.opponent_name }}</th>
        <th style="width: 5%"></th>
      </tr>
    </thead>
    <tbody>
      {% for key, item in items.items() %}
      <tr>
        
        <td>
            <h4 class="progress-label-right">{{item.p1}}</h4>
            </td>
        <td> 
            
            
            <div class="progress flex-row-reverse">
                <div class="progress-bar bg-success" role="progressbar" style="width: {{item.p1_perc}}%"  aria-valuenow="{{item.p1_perc}}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            
        </td>
        <td>
          {{ key }}
        </td>
            
        <td>
        
          <div class="progress">
                <div class="progress-bar bg-danger" role="progressbar" style="width: {{100 - item.p1_perc}}%"  aria-valuenow="{{100 - item.p1_perc}}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
          
            <td>
            
            <h4 class="progress-label">{{item.p2}}</h4>
            
            </td>
         
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

                 '''
    rtemplate = Environment(loader=BaseLoader()).from_string(x)
    ui.html(rtemplate.render(items=new_items, dm=movement_json)).classes('w-full').classes('mx-auto')

def ui_table(ui):
    ui.html('<h1 class="text-center">2nd serve table</h1>').classes('text-2xl').classes('mx-auto')
    ui.html('''

<div class="container mt-4">
  
  
  <table class="table text-center">
    <thead>
      <tr>
        <th style="width: 5%"></th>
        <th style="width: 40%;color:#28a745">Coric</th>
        <th style="width: 10%"></th>
        <th style="width: 40%;color:#dc3545">Tsitsipas</th>
        <th style="width: 5%"></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        
        <td>
            <h4 class="progress-label-right">13</h4>
            </td>
        <td> 
            
            
            <div class="progress flex-row-reverse">
                <div class="progress-bar bg-success" role="progressbar" style="width: 52%"  aria-valuenow="52" aria-valuemin="0" aria-valuemax="100"></div>
                <span class="progress-value">52%</span>
              </div>
            
        </td>
        <td>
          Number of serves
        </td>
            
        <td>
        
          <div class="progress">
                <div class="progress-bar bg-danger" role="progressbar" style="width: 48%"  aria-valuenow="48" aria-valuemin="0" aria-valuemax="100"></div>
                <span class="progress-value">48%</span>
              </div>
          
            <td>
            
            <h4 class="progress-label">12</h4>
            
            </td>
         
        </td>
      </tr>
      <tr>
        <td>
            <h4 class="progress-label-right">3</h4>
            </td>
        <td> 
            
            
            <div class="progress flex-row-reverse">
                <div class="progress-bar bg-success w-75" role="progressbar"  aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                <span class="progress-value">75%</span>
              </div>
            
        </td>
        <td>
          Number of aces
        </td>
            
        <td>
        
          <div class="progress">
                <div class="progress-bar bg-danger w-25" role="progressbar"  aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                <span class="progress-value">25%</span>
              </div>
          
            <td>
            
            <h4 class="progress-label">1</h4>
            
            </td>
         
        </td>
      <tr>
       
      </tr>
    </tbody>
  </table>
</div>

                 ''').classes('w-full md:w-1/2').classes('mx-auto')