from nicegui import ui
from utils_bootstrap_new import *
from utils_bootstrap_new2 import *
from report_util_new import main2, main3
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import json
import pandas as pd
#img = Image.open('GSAfulllogo-white.png')



#ui.image(img).classes('w-64').classes('mx-auto')

#df = #load_df()


from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui, run

# in reality users passwords would obviously need to be hashed
passwords = {'marin': '1s23', 'bhaddassdmsssssssssassssssssssfssssssssssssssssssasssvssf': 'goldenset1232'}

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


app.add_middleware(AuthMiddleware)

@ui.page('/movement/{player}')
def movement_report(player: str):
    ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
    ui.markdown(f'# Movement report').classes('mx-auto')
    ui.markdown(f'## {player} 2023 (4 matches)').classes('mx-auto')
    ui.image(f'movement/{player}/damien_visual.png').classes('w-1/2').classes('mx-auto')

    df1 = pd.read_parquet(f'movement/{player}/rally_duration_impact.parquet')
    df2 = pd.read_parquet(f'movement/{player}/rally_movement_change.parquet')
    df3 = pd.read_parquet(f'movement/{player}/rally_shot_type_impact.parquet')

    ui.label('Rally Duration Impact').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df1.columns],
    rows=df1.to_dict('records')).classes('mx-auto')

    ui.label('Movement Direction').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df2.columns],
    rows=df2.to_dict('records')).classes('mx-auto')

    ui.label('Point Outcome').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df3.columns],
    rows=df3.to_dict('records')).classes('mx-auto') 

@ui.page('/movement/{player}')
def movement_report(player: str):
    ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
    ui.markdown(f'# Movement report').classes('mx-auto')
    ui.markdown(f'## {player} 2023 (4 matches)').classes('mx-auto')
    ui.image(f'movement/{player}/damien_visual.png').classes('w-1/2').classes('mx-auto')

    df1 = pd.read_parquet(f'movement/{player}/rally_duration_impact.parquet')
    df2 = pd.read_parquet(f'movement/{player}/rally_movement_change.parquet')
    df3 = pd.read_parquet(f'movement/{player}/rally_shot_type_impact.parquet')

    ui.label('Rally Duration Impact').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df1.columns],
    rows=df1.to_dict('records')).classes('mx-auto')

    ui.label('Movement Direction').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df2.columns],
    rows=df2.to_dict('records')).classes('mx-auto')

    ui.label('Point Outcome').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df3.columns],
    rows=df3.to_dict('records')).classes('mx-auto') 



    

@ui.page('/match/{match_str}')
def main_page(match_str: str):
  
  with open(f'../matches/{match_str}/movement.json') as f:
      dm = json.load(f)
  match = '_'.join(match_str.split('_')[1:])
  pretty_dict, data1, data2, data_order = main2(selected_player_name=[dm['selected_player_name']], opponent_name=[dm['opponent_name']], matches=[match])
  df_games = pd.read_csv(f"matches/{match_str}/{dm['path_to_games']}")
  #print('---------------------------', match,match.split(r'_(\d{4})_'))
  import re
  pattern = re.compile(r'(\D+)(\d{4})(.+)')

  # Use the pattern to match and extract the parts
  matches = pattern.match(match)
  parts = matches.groups()
  tournament = parts[0].replace('_', ' ').strip().upper()
  year = parts[1]
  ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
  ui.markdown('# Post match report').classes('mx-auto')
  ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()} - {tournament} {year}').classes('mx-auto')
  ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <style>
@media screen and (orientation: portrait) {
  html {
    transform: rotate(-90deg);
    transform-origin: left top;
    width: 100vh;
    height: 100vw;
    overflow-x: hidden;
    position: absolute;
    top: 100%;
    left: 0;
  }
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
      
      ui.tab('v', label='Video')

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


  with ui.tab_panels(tabs, value='s1').classes('w-full'):
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
          serve_html(ui, dm, '1st Serve', None, items)
      with ui.tab_panel('s2'):
          items = dict()
          for key in data_order['serve_2nd']:
              #if '2nd' in key.lower():
              if True:
                #print(items)
                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
          serve_html_2nd(ui, dm, '2nd Serve', items)
      with ui.tab_panel('r1'):
          items = dict()
          for key in data_order['return']:
              #if '1st' in key.lower():
              if True:
                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
          return_html(ui, dm, '1st Return Quality', items)
      with ui.tab_panel('r2'):
          items = dict()
          for key in data_order['return_2nd']:
              #if '1st' in key.lower():
              if True:
                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
          return_html2(ui, dm, '2nd Return Quality', items)
      
      with ui.tab_panel('m'):
          items = dict()
          for key in data_order['return_2nd']:
              #if '1st' in key.lower():
              if True:
                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
          movement_html(ui, dm, df_games)
      with ui.tab_panel('gs'):
          items = dict()
          for key in data_order['groundstroke_table']:
              #if '1st' in key.lower():
              if True:
                items[pretty_dict.get(key, key)] = {'p1': data1[key], 'p2': data2[key], 'p1_perc': to_int(data1[key], data2[key])}
          groundstroke_html(ui, dm, 'GS Table', items)
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
  with open(f'../matches_new/{match_str}/movement.json') as f:
      dm = json.load(f)
  match = '_'.join(match_str.split('_')[1:])
  image_dir = f'../matches_new/{match_str}/'
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
  df_games = pd.read_csv(f"../matches_new/{match_str}/{dm['path_to_games']}")
  
  import re
  pattern = re.compile(r'(\D+)(\d{4})(.+)')

  # Use the pattern to match and extract the partss
  matches = pattern.match(match)
  parts = matches.groups()
  tournament = parts[0].replace('_', ' ').strip().upper()
  year = parts[1]
  ui.image('gsa_logo_smaller.png').classes('w-1/4').classes('mx-auto')
  ui.markdown('# Post match report').classes('mx-auto')
  ui.markdown(f'### {dm["selected_player_name"].upper()} VS {dm["opponent_name"].upper()} - {tournament} {year}').classes('mx-auto')
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
          

@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
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


  #ui.markdown('# Below the html')
ui.run(host='0.0.0.0', port=8508, native=False, storage_secret='test')