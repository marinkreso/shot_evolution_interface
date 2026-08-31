



from jinja2 import Environment, BaseLoader


def movement_html(ui, movement_json, df):
    #df1 = df[['Game Description', 'Distance covered per point', 'Average movement speed', 'Serve Speed avg']]
    ui.label('Match Duration Information').classes('mx-auto').tailwind('font-bold')
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
    df['Game Description'] = df['Game Description'].apply(replace_game_str)
    df1 = df[movement_columns]
    df2 = df[['Game Description', 'Serve Speed Avg', 'Forehand Speed Avg', 'Backhand Speed Avg (without slices)', 'Backhand Speed Avg (with slices)']]
    
    ui.label('Movement Analysis over Six-Game Intervals').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df1.columns],
    rows=df1.to_dict('records'),
).classes('mx-auto')
    ui.label('Shot Analysis over Six-Game Intervals').classes('mx-auto').tailwind('font-bold')
    ui.table(
    columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in df2.columns],
    rows=df2.to_dict('records'),
).classes('mx-auto')#.classes('w-1/2')
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    #ui_table_jinja(ui, movement_json, items, x)
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')
    xd = movement_json['shots_data_numbers']
    rows = []
    for key in xd:
        rows.append({'Stroke': key, 'Number of Shots': xd[key]})
    ui.label('Stroke quantifications').classes('mx-auto').tailwind('font-bold')
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
        ui.label('Distance quantifications with percentages').classes('mx-auto').tailwind('font-bold')
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
          ui.label('Distance per point with win percentage').classes('mx-auto').tailwind('font-bold')
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
          ui.label('Number of Sprints').classes('mx-auto').tailwind('font-bold')
          ui.table(
          columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Speed', 'Number']],
          rows=rows,
          ).classes('mx-auto')
      
    
    #ui.image('movement_visual.png').classes('mx-auto').classes('w-1/2')
def bh_html(ui,movement_json, x, items):
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    ui_table_jinja(ui, movement_json, items, x)
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')

def groundstroke_html(ui,movement_json, x, items):
    #items['table_title'] = 'BH TABLE'
    #ui_table_jinja(ui, movement_json, items, 'BH TABLE')
    #ui_table(ui)
    ui_table_jinja(ui, movement_json, items, x)
    #ui.html('<h1>BH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('8.png').classes('w-96').classes('mx-auto')
   
def fh_html(ui, movement_json, x, items):
    #ui_table(ui)
    ui_table_jinja(ui, movement_json, items, x)
    #ui.html('<h1>FH DANGEROUS LOCATIONS</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('7.png').classes('w-96').classes('mx-auto')

def return_html(ui, movement_json, returnx, items):
    ui_table_jinja(ui, movement_json, items, returnx)
    #with ui.row().classes('w-full no-wrap'):
    #  ui.image('1st_deuce_returns.png').classes('w-1/2')
    #  ui.image('1st_ad_returns.png').classes('w-1/2')
      #ui.label('Third column with some more text').classes('bg-blue-100 w-1/3')
    #ui.html('<h1>Return directions</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_percentages.png').classes('w-96').classes('mx-auto')
    #ui.html('<h1>Return rally</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_rally.png').classes('w-96').classes('mx-auto')

def return_html2(ui, movement_json, returnx, items):
    ui_table_jinja(ui, movement_json, items, returnx)
    #with ui.row().classes('w-full no-wrap'):
    #  ui.image('2nd_deuce_returns.png').classes('w-1/2')
    #  ui.image('2nd_ad_returns.png').classes('w-1/2')
      #ui.label('Third column with some more text').classes('bg-blue-100 w-1/3')
    #ui.html('<h1>Return directions</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_percentages.png').classes('w-96').classes('mx-auto')
    #ui.html('<h1>Return rally</h1>').classes('mx-auto').classes('text-2xl')
    #ui.image('return_rally.png').classes('w-96').classes('mx-auto')
  
def serve_html(ui, movement_json, serve, rally_win, items):
    #with ui.element('div').classes('text-center'):
    
#     ui.markdown('''
#     1ST SERVE WIN% BY DIRECTION
    
#       -  DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T 
#       -  AD: DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T       

# '''
        
#     ).classes('mx-auto').props('absolute-center')
    #ui_table(ui)

    ui_table_jinja(ui, movement_json, items, '1st Serve Quality')
    xd = movement_json.get('placement_first')
    if xd:
      ui.markdown(f'### 1st Serve Direction {movement_json.get("selected_player_name","Player" )}').classes('mx-auto').tailwind('font-bold')
      rows = []
      for key in xd:
          rows.append({'Serve Type': key, 'Perc of Serves': xd[key]})
      #ui.label('Serve direction').classes('mx-auto').tailwind('font-bold')
      ui.table(
      columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Serve Type', 'Perc of Serves']],
      rows=rows,
      ).classes('mx-auto')
    ui.markdown(f'### {movement_json.get("selected_player_name","Player" )} 1st Serve Placement < 40 cm of the side lines ').classes('mx-auto').tailwind('font-bold')
    ui.label(movement_json['1st_serve_placement'].upper()).classes('mx-auto')
    #ui.image('placement_first.png').classes('w-1/4').classes('mx-auto')
    #ui.image('serve_direction2.png').classes('w-1/2').classes('mx-auto')
    #ui.image('serve_rally.png').classes('w-96').classes('mx-auto')
    #ui.image('serve_placement2.png').classes('w-1/2').classes('mx-auto')

def serve_html_2nd(ui, movement_json, serve, items):
    #with ui.element('div').classes('text-center'):
    
#     ui.markdown('''
#     1ST SERVE WIN% BY DIRECTION
    
#       -  DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T 
#       -  AD: DEUCE: HIGHER WIN% SERVING WIDE V T HIGHER WIN% SERVING T V WIDE | ABOUT THE SAME WIN% WIDE V T       

# '''
        
#     ).classes('mx-auto').props('absolute-center')
    #ui_table(ui)

    ui_table_jinja(ui, movement_json, items, '2nd Serve Quality')
    xd = movement_json.get('placement_second')
    if xd:
      ui.markdown(f'### 2nd Serve Direction {movement_json.get("selected_player_name","Player" )}').classes('mx-auto').tailwind('font-bold')
      rows = []
      for key in xd:
          rows.append({'Serve Type': key, 'Perc of Serves': xd[key]})
      #ui.label('Serve direction').classes('mx-auto').tailwind('font-bold')
      ui.table(
      columns=[{'name': col, 'label': col, 'field': col, 'align': 'center'} for col in ['Serve Type', 'Perc of Serves']],
      rows=rows,
      ).classes('mx-auto')
    #ui.image('placement_second.png').classes('w-1/4').classes('mx-auto')
    #ui.image('serve_rally.png').classes('w-96').classes('mx-auto')
    #ui.image('serve_placement2.png').classes('w-1/2').classes('mx-auto')

def ui_table_jinja(ui, movement_json, items, table_title):
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
    ui.html(rtemplate.render(items=items, dm=movement_json)).classes('w-full').classes('mx-auto')

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

                 ''').classes('w-1/2').classes('mx-auto')