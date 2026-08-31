#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import psycopg2
import os
import re
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
from azure_client import container_client, azure_upload_docx





# In[2]:


surfaces = ['hard']
# In[ ]:





# In[3]:


#pd.read_csv('deleted_jm_cerundolo.csv').to_sql('atp_matches_data', engine, if_exists='append', index=False)


# In[4]:


def load_data_all(player_name, opponent_name, selected_match_ids, tour, surfaces, years):
    years_str = [str(x) for x in years]
    def extract_year(match_id):
        x = re.findall(r"(?<!\d)\d{4,4}(?!\d)", match_id)
        if x:
            return x[0]
        return '1968'
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
    'ON_NET_Z',
    'PLAYER_HIT',
    'PLAYER_WIN',
    'PLAYER_WIN_NAME',
    'REBOUND_X',
    'REBOUND_X_abs',
    'REBOUND_Y',
    'REBOUND_Y_mirrored',
    'SET_GAME_POINT',
    'SPEED',
    'SPIN',
    'distance_from_base_line',
    'distance_from_sideline',
               'serve_direction_detailed',
    'game_no',
    'is_in_the_net',
    'is_last_shot',
    'is_shot_in',
    'match_id',
    'point_id',
    'rally_length',
    'serve_deuce_or_ad',
    'serve_direction',
    'serve_number',
    'set_no',
    'shot_no']
    # LOAD LIBRARIES AND CONNECT TO 
    

    
    df_all = None

    if years:
        selected_match_ids = [x for x in selected_match_ids if extract_year(x) in years_str]
    selected_match_ids = [x.replace("'", "''") for x in selected_match_ids]
    cols = ','.join(list(f'\"{x}\"' for x in usecols))
    if tour.lower() == 'atp':
        query  = "SELECT * FROM hawkeye_app.atp_all_data WHERE match_id IN (%s)" % (','.join([f"'{x}'" for x in selected_match_ids]))
    else:
        query = "SELECT * FROM hawkeye_app.wta_all_data WHERE match_id IN (%s)" % (','.join([f"'{x}'" for x in selected_match_ids]))
    user='marin'
    password='RV4vjA9xUxTjMc'
    host='gsa-pg-data-production.postgres.database.azure.com'
    port='5432'
    database='hawkeye'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')
    df = pd.read_sql(query, engine)

    
    df['point_no'] = df.point_id.apply(lambda x: float(x.split('_')[2]))
    df = df.sort_values(by=['match_id', 'set_no', 'game_no', 'point_no', 'serve_number', 'shot_no'])
    #df = pd.read_parquet('Berrettini.parquet')
    #df['time_for_shot'] = df['shot_time_end'] - df['shot_time_start']
    years_str = [str(x) for x in years]
    #if surfaces:
    #    df = df[df.surface.isin(surfaces)]
    
    #tournaments = [t.lower().replace(' ', '').replace('_', '') for t in tournaments]
    #tournaments = [t.lower() for t in tournaments]
    #if tournaments:
    #    df = df[df.match_id.str.contains.isin(tournaments)]

    #df = df[(df.match_id.str.contains('2022')) | (df.match_id.str.contains('2021')) | (df.match_id.str.contains('2023'))]
    #print(df.match_id.unique())
    #(df.match_id.unique())
    return df


# In[ ]:





# In[5]:





def calculate_distance_from_the_middle_at_BL(df):
    # We calculate the accuracy of the serve through the new metric called ball_distance_from_the_middle_at_BL
    # For each serve we calculate where (would) the ball crosses the base line. We use three points to fit this kvadratic curve. Kvadratic, so we can estimete the ball curve
    # For deuce serves values are negative and for ad positive. Small values close to 0 are serves crossing base line near the center of the court
    court_length = 11.89
    ball_distance_from_the_middle_at_BL = []
    for i, row in df.iterrows():        
        x1 = row['CONTACT_X']
        y1 = row['CONTACT_Y'] 
        x2 = 0
        if pd.isna(row['ON_NET_Y']):            
            y2 = row['NET_COORD_Y']            
        else:
            y2 = row['ON_NET_Y']
        
        if pd.isna(row['REBOUND_Y']):            
            x = [x1, x2]
            y = [y1, y2]        
        else:
            x3 = row['REBOUND_X']
            y3 = row['REBOUND_Y']
            x = [x1, x2, x3]
            y = [y1, y2, y3]
            
        #Check if any value is nan
        try:
            #print(any(xnone is None for xnone in x), any(xnone is None for xnone in y))
            if any(xnone is None for xnone in x) | any(xnone is None for xnone in y):
                ball_distance_from_the_middle_at_BL.append(np.nan)
            elif (np.isnan(y).any() | (np.isnan(x).any())):
                ball_distance_from_the_middle_at_BL.append(np.nan)
            else:
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)

                #Get y values at the base line
                if row['CONTACT_X'] == 0:
                    x4 = 0
                else:
                    x4 = row['CONTACT_X']/abs(row['CONTACT_X']) * -1 * court_length
                y4 = p(x4)
                ball_distance_from_the_middle_at_BL.append(y4)
        except:
            print('exc', x, y)
            raise Exception

    #Check for errors and correct noise values
    #Also addi mirrored value for combining deuce and ad serves
    if len(df) == len(ball_distance_from_the_middle_at_BL):
        df['ball_y_at_BL'] = ball_distance_from_the_middle_at_BL
        df['ball_y_at_BL_mirrored'] = np.where(df['CONTACT_X'] > 0, df['ball_y_at_BL'], df['ball_y_at_BL']*-1)
        return df
    else:
        print('ERROR!!!')


# In[ ]:





# In[7]:


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
from matplotlib import font_manager
from pathlib import Path
FONT_PATH = (Path(__file__).resolve().parent / "fonts" / "DIN Condensed Bold.ttf")
font_manager.fontManager.addfont(str(FONT_PATH))
rcParams['font.sans-serif'] = ['DIN Condensed']
rcParams['font.size'] = 18 #12


# In[8]:





# In[9]:


#tournaments_backup = pd.read_sql('he_tournaments', engine)


# In[10]:


#tournaments_backup.to_parquet('tournaments_backup.parquet')


# In[ ]:





# In[11]:


#atp_matches = pd.read_sql('atp_matches_data', engine)
#wta_matches =pd.read_sql('wta_matches_data', engine)


# In[12]:


#atp_tournaments = atp_matches['match_id'].str.split(r'_(\d{4})_').str[0]
#wta_tournaments = wta_matches['match_id'].str.split(r'_(\d{4})_').str[0]


# In[13]:


#tournaments = list(set(list(atp_tournaments.unique()) + list(wta_tournaments.unique()) ))


# In[ ]:





# In[14]:


#df = pd.DataFrame()


# In[15]:


#df['tournaments'] = tournaments


# In[16]:


#df.to_sql('he_tournaments', engine, if_exists='replace')


# In[ ]:





# In[17]:


#tourna


# In[ ]:





# In[ ]:





# In[18]:


#tournaments[tournaments.tournaments.str.contains('Winston')]


# In[ ]:





# In[ ]:





# In[19]:





# In[ ]:





# In[20]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[21]:



def get_locations_at_shot(df, column_name):
    at_shot_locations =[]
    for server_location_values in df[column_name].tolist():
        float_values = [float(x) for x in server_location_values.strip('][').split(', ')]
        if len(float_values) > 0:
            at_shot_locations.append(float_values[0])
        else:
            at_shot_locations.append(np.nan)
    return at_shot_locations

def get_locations_after_shot(df, column_name):
    at_shot_locations =[]
    for server_location_values in df[column_name].tolist():
        float_values = [float(x) for x in server_location_values.strip('][').split(', ')]
        if len(float_values) > 20:
            at_shot_locations.append(float_values[20])
        elif len(float_values) > 10:
            at_shot_locations.append(float_values[10])
        elif len(float_values) > 5:
            at_shot_locations.append(float_values[5])
        elif len(float_values) > 0:
            at_shot_locations.append(float_values[0])
        else:
            at_shot_locations.append(np.nan)
    return at_shot_locations

def plot_traces_second(df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    set_court_trajectory(ax)

    
    fig.suptitle(main_title)
    ax.set_title(title1)
    ax.invert_xaxis()
    counter = 0
    counter1 = 0
    df_shots_w = df_shots.dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        gradient = slope(loc_xs[0], loc_ys[0], loc_xs[-1], loc_ys[-1])
        if abs(gradient) > 0.26:
            counter = counter + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red, alpha=0.5)
        elif abs(gradient) < 0.24:
            counter1 = counter1 + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green, alpha=0.5)
        
    #Set legend
    #print(counter, counter1)
    red_patch = mpatches.Patch(color=c_red, label='Slice serves')
    green_patch = mpatches.Patch(color=c_green, label='Flat serves')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax.legend(handles=[green_patch, red_patch])
    fig.set_tight_layout(True)
    return fig



def plot_traces_first(df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    set_court_trajectory(ax)

    
    fig.suptitle(main_title)
    ax.set_title(title1)
    ax.invert_xaxis()
    counter = 0
    counter1 = 0
    df_shots_w = df_shots.dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        gradient = slope(loc_xs[0], loc_ys[0], loc_xs[-1], loc_ys[-1])
        if abs(gradient) > 0.29:
            counter = counter + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red, alpha=0.5)
        elif abs(gradient) < 0.28:
            counter1 = counter1 + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green, alpha=0.5)
        
    #Set legend
    #print(counter, counter1)
    red_patch = mpatches.Patch(color=c_red, label='Slice serves')
    green_patch = mpatches.Patch(color=c_green, label='Flat serves')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax.legend(handles=[green_patch, red_patch])
    fig.set_tight_layout(True)
    return fig

def plot_traces_second_t(df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    set_court_trajectory(ax)

    
    fig.suptitle(main_title)
    ax.set_title(title1)
    ax.invert_xaxis()
    counter = 0
    counter1 = 0
    df_shots_w = df_shots.dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        gradient = slope(loc_xs[0], loc_ys[0], loc_xs[-1], loc_ys[-1])
        if abs(gradient) > 0.26:
            counter = counter + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red, alpha=0.5)
        elif abs(gradient) < 0.24:
            counter1 = counter1 + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green, alpha=0.5)
        
    #Set legend
    #print(counter, counter1)
    red_patch = mpatches.Patch(color=c_red, label='Slice serves')
    green_patch = mpatches.Patch(color=c_green, label='Flat serves')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax.legend(handles=[green_patch, red_patch])
    fig.set_tight_layout(True)
    return fig

def plot_traces_first_t(df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    set_court_trajectory(ax)

    
    fig.suptitle(main_title)
    ax.set_title(title1)
    ax.invert_xaxis()
    counter = 0
    counter1 = 0
    df_shots_w = df_shots.dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        gradient = slope(loc_xs[0], loc_ys[0], loc_xs[-1], loc_ys[-1])
        if abs(gradient) > 0.29:
            counter = counter + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red, alpha=0.5)
        elif abs(gradient) < 0.28:
            counter1 = counter1 + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green, alpha=0.5)
        
    #Set legend
    #print(counter, counter1)
    red_patch = mpatches.Patch(color=c_red, label='Slice serves')
    green_patch = mpatches.Patch(color=c_green, label='Flat serves')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax.legend(handles=[green_patch, red_patch])
    fig.set_tight_layout(True)
    return fig

def plot_traces(selected_player_name, df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 11))
    set_court(ax[0])
    set_court(ax[1])
    
    fig.suptitle(main_title)
    ax[0].set_title(title1)
    ax[1].set_title(title2)
    ax[0].invert_xaxis()
    ax[1].invert_xaxis()
    
    df_shots_w = df_shots[df_shots['PLAYER_WIN_NAME'] == selected_player_name].dropna(subset=['shot_time_start'])
    df_shots_e = df_shots[df_shots['PLAYER_WIN_NAME'] != selected_player_name].dropna(subset=['shot_time_start'])
    df_shots_ace = df_shots[(df_shots['is_last_shot']==1) & (df_shots['is_shot_in'] == 1)].dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green) 
        
    for i,row in df_shots_ace.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_yellow)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_yellow) 
        
    
    for i,row in df_shots_e.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red)
        
    #Set legend
    red_patch = mpatches.Patch(color=c_red, label='Point lost')
    green_patch = mpatches.Patch(color=c_green, label='Point won')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax[0].legend(handles=[yellow_patch, green_patch, red_patch])
    
    
    df_shots_unreturned = df_shots[(df_shots['PLAYER_WIN_NAME'] == selected_player_name) & (df_shots['rally_length']<3)].dropna(subset=['shot_time_start'])
    df_shots_returned = df_shots[((df_shots['PLAYER_WIN_NAME'] != selected_player_name) & (df_shots['rally_length'] == 2)) | (df_shots['rally_length']>3)].dropna(subset=['shot_time_start'])
    for i,row in df_shots_unreturned.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[1].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
        ax[1].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green) 
        
    for i,row in df_shots_returned.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[1].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_orange)
        ax[1].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_orange) 
    
    #Set legend
    green_patch = mpatches.Patch(color=c_green, label='Unreturned serves')
    orange_patch = mpatches.Patch(color=c_orange, label='Returned serves')
    ax[1].legend(handles=[orange_patch, green_patch])

    fig.set_tight_layout(True)
    return fig

def set_court(ax, court_draw_width_start = -8.5, court_draw_width_end = 8.5):
    court_draw_height_end = 19 #17
    court_draw_height_start = -19 #-17
    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    
    linewidth = 3    
    court_width = 8.23
    court_length = 11.89
    court_width_doubles = 8.23 + 1.37 + 1.37
    
    net_post_x_left = -court_width_doubles/2 + 0.5
    net_post_x_right = court_width_doubles/2 - 0.5
    
    line_color = 'white'
    
    ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color) #net
    ax.plot([-court_width/2, -court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width/2, court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width_doubles/2, court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    
    
    light_grass = '#83a462'
    dark_grass = '#739655'
    # Number of stripes and their height
    surfacecode = SurfaceCode.HARD
    if surfacecode == SurfaceCode.GRASS:
        ax.set_facecolor('#83a462')# -> grass court
        num_stripes = 10
        stripe_width = abs(court_draw_width_start - court_draw_width_end) / num_stripes
        for i in range(num_stripes):
            x_start = court_draw_width_start + i*stripe_width
            x_end = x_start + stripe_width
            color = light_grass if i % 2 == 0 else dark_grass
            ax.axvspan(x_start, x_end, alpha=1, color=color)
            #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#83a462')
        stripe_height = (court_length - court_draw_height_end) / num_stripes
    else:
        alpha = 1
        ax.set_facecolor(court_color_x)# -> hard court
        #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#83a462')
        ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        #Behind the baseline
        ax.axhspan(court_length, court_length + 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
def get_ball_locations(row):
    loc_xs = []
    loc_ys = []
    loc_zs = []
    time_step = 0.05
    if np.isnan(row['shot_time_start']) or np.isnan(row['shot_time_end']):
        return None, None, None
    for t in np.arange(row['shot_time_start'], row['shot_time_end'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0'] + row['ArcSvaMatrix_x_1']*t + row['ArcSvaMatrix_x_2']*t**2 + row['ArcSvaMatrix_x_3']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0'] + row['ArcSvaMatrix_y_1']*t + row['ArcSvaMatrix_y_2']*t**2 + row['ArcSvaMatrix_y_3']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0'] + row['ArcSvaMatrix_z_1']*t + row['ArcSvaMatrix_z_2']*t**2 + row['ArcSvaMatrix_z_3']*t**3)
    if ((row['is_last_shot'] == 1) & (row['is_in_the_net'] == 0)):
        for t in np.arange(row['shot_time_end'], row['shot_time_end']+0.7, time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)
            
    if abs(row['shot_time_end'] - row['shot_time_start_next'])>0.002: #there is trace after bounce (no volley played on the next shot)
        for t in np.arange(row['shot_time_end'], row['shot_time_start_next'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)

        
    #Abs the x and mirror the y to get serves always from one side
    if loc_xs[0] > 0:
        loc_ys = [-1 * i for i in loc_ys]
        loc_xs = [-1 * i for i in loc_xs]
    
    if loc_xs[0] * loc_xs[-1] > 0:
        return None, None, None
    else:
        return loc_xs, loc_ys, loc_zs
    
def get_ball_locations_before_bounce(row):
    loc_xs = []
    loc_ys = []
    loc_zs = []
    time_step = 0.05
    if np.isnan(row['shot_time_start']) or np.isnan(row['shot_time_end']):
        return None, None, None
    for t in np.arange(row['shot_time_start'], row['shot_time_end'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0'] + row['ArcSvaMatrix_x_1']*t + row['ArcSvaMatrix_x_2']*t**2 + row['ArcSvaMatrix_x_3']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0'] + row['ArcSvaMatrix_y_1']*t + row['ArcSvaMatrix_y_2']*t**2 + row['ArcSvaMatrix_y_3']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0'] + row['ArcSvaMatrix_z_1']*t + row['ArcSvaMatrix_z_2']*t**2 + row['ArcSvaMatrix_z_3']*t**3)
    if ((row['is_last_shot'] == 1) & (row['is_in_the_net'] == 0)):
        for t in np.arange(row['shot_time_end'], row['shot_time_end']+0.7, time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)
        
    #Abs the x and mirror the y to get serves always from one side
    if loc_xs[0] > 0:
        loc_ys = [-1 * i for i in loc_ys]
        loc_xs = [-1 * i for i in loc_xs]
    
    if loc_xs[0] * loc_xs[-1] > 0:
        return None, None, None
    else:
        return loc_xs, loc_ys, loc_zs

def get_ball_locations_after_bounce(row):
    loc_xs = []
    loc_ys = []
    loc_zs = []
    time_step = 0.01
    if np.isnan(row['shot_time_start']) or np.isnan(row['shot_time_end']):
        return None, None, None
   

    if abs(row['shot_time_end'] - row['shot_time_start_next'])>0.002: #there is trace after bounce (no volley played on the next shot)
        for t in np.arange(row['shot_time_end'], row['shot_time_start_next'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)

        
    
    
    
    return loc_xs, loc_ys, loc_zs   


def slope(x1, y1, x2, y2):
        m = (y2-y1)/(x2-x1)
        return m
def set_court_trajectory(ax, court_draw_width_start = -8.5, court_draw_width_end = 8.5):
    #court_draw_width_start = -6.5
    #court_draw_width_end = 6.5
    court_draw_height_end = 17 #17
    court_draw_height_start = -17 #-17
    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    
    linewidth = 3    
    court_width = 8.23
    court_length = 11.89
    court_width_doubles = 8.23 + 1.37 + 1.37
    
    net_post_x_left = -court_width_doubles/2 + 0.5
    net_post_x_right = court_width_doubles/2 - 0.5
    
    line_color = 'white'
    
    ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color) #net
    ax.plot([-court_width/2, -court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width/2, court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width_doubles/2, court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    #Net post
    #ax.add_artist(Circle((net_post_x_left, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_artist(Circle((net_post_x_right, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_patch(Rectangle((net_post_x_left - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    #ax.add_patch(Rectangle((net_post_x_right - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    
#Court color
    #ax.set_facecolor(court_color_x)
    #Out of court color
    #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=0.8, color=out_of_court_color_x)
    #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=0.8, color=out_of_court_color_x)
    
    #Court color
    #ax.set_facecolor('#d45e3e')# -> clay court
    
    
    #Out of court color
    
    light_grass = '#83a462'
    dark_grass = '#739655'
    # Number of stripes and their height
    
    if surfacecode == SurfaceCode.GRASS:
        ax.set_facecolor('#83a462')# -> grass court
        num_stripes = 10
        stripe_width = abs(court_draw_width_start - court_draw_width_end) / num_stripes
        for i in range(num_stripes):
            x_start = court_draw_width_start + i*stripe_width
            x_end = x_start + stripe_width
            color = light_grass if i % 2 == 0 else dark_grass
            ax.axvspan(x_start, x_end, alpha=1, color=color)
            #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#83a462')
        stripe_height = (court_length - court_draw_height_end) / num_stripes
    else:
        alpha = 1
        ax.set_facecolor(court_color_x)# -> hard court
        ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        #Behind the baseline
        ax.axhspan(court_length, court_length + 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def plot_traces_first(df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    set_court_trajectory(ax)

    
    fig.suptitle(main_title)
    ax.set_title(title1)
    ax.invert_xaxis()
    counter = 0
    counter1 = 0
    df_shots_w = df_shots.dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        gradient = slope(loc_xs[0], loc_ys[0], loc_xs[-1], loc_ys[-1])
        if abs(gradient) > 0.29:
            counter = counter + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red, alpha=0.5)
        elif abs(gradient) < 0.28:
            counter1 = counter1 + 1
            #pass
            ax.plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
            ax.scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green, alpha=0.5)
        
    #Set legend
    #print(counter, counter1)
    red_patch = mpatches.Patch(color=c_red, label='Slice serves')
    green_patch = mpatches.Patch(color=c_green, label='Flat serves')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax.legend(handles=[green_patch, red_patch])
    fig.set_tight_layout(True)
    return fig

def plot_traces(selected_player_name, df_shots, court_draw_width_start=-6.5, court_draw_width_end=6.5, title1 = '', title2='', main_title = ''):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    c_yellow = '#FFFFDD'
    c_orange = '#ff8300'
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 11))
    set_court(ax[0])
    set_court(ax[1])
    
    fig.suptitle(main_title)
    ax[0].set_title(title1)
    ax[1].set_title(title2)
    ax[0].invert_xaxis()
    ax[1].invert_xaxis()
    
    df_shots_w = df_shots[df_shots['PLAYER_WIN_NAME'] == selected_player_name].dropna(subset=['shot_time_start'])
    df_shots_e = df_shots[df_shots['PLAYER_WIN_NAME'] != selected_player_name].dropna(subset=['shot_time_start'])
    df_shots_ace = df_shots[(df_shots['is_last_shot']==1) & (df_shots['is_shot_in'] == 1)].dropna(subset=['shot_time_start'])
    for i,row in df_shots_w.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green) 
        
    for i,row in df_shots_ace.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_yellow)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_yellow) 
        
    
    for i,row in df_shots_e.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[0].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_red)
        ax[0].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_red)
        
    #Set legend
    red_patch = mpatches.Patch(color=c_red, label='Point lost')
    green_patch = mpatches.Patch(color=c_green, label='Point won')
    yellow_patch = mpatches.Patch(color=c_yellow, label='Ace')
    ax[0].legend(handles=[yellow_patch, green_patch, red_patch])
    
    
    df_shots_unreturned = df_shots[(df_shots['PLAYER_WIN_NAME'] == selected_player_name) & (df_shots['rally_length']<3)].dropna(subset=['shot_time_start'])
    df_shots_returned = df_shots[((df_shots['PLAYER_WIN_NAME'] != selected_player_name) & (df_shots['rally_length'] == 2)) | (df_shots['rally_length']>3)].dropna(subset=['shot_time_start'])
    for i,row in df_shots_unreturned.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[1].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_green)
        ax[1].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_green) 
        
    for i,row in df_shots_returned.iterrows():
        loc_xs, loc_ys, loc_zs = get_ball_locations(row)
        if not loc_xs or not loc_ys:
            continue
        ax[1].plot([-1*x for x in loc_ys], [-1*x for x in loc_xs], c=c_orange)
        ax[1].scatter(row['REBOUND_Y_mirrored'], -1*row['REBOUND_X_abs'], color=c_orange) 
    
    #Set legend
    green_patch = mpatches.Patch(color=c_green, label='Unreturned serves')
    orange_patch = mpatches.Patch(color=c_orange, label='Returned serves')
    ax[1].legend(handles=[orange_patch, green_patch])

    fig.set_tight_layout(True)
    return fig

def set_court(ax, court_draw_width_start = -8.5, court_draw_width_end = 8.5):
    court_draw_height_end = 19 #17
    court_draw_height_start = -19 #-17
    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    
    linewidth = 3    
    court_width = 8.23
    court_length = 11.89
    court_width_doubles = 8.23 + 1.37 + 1.37
    
    net_post_x_left = -court_width_doubles/2 + 0.5
    net_post_x_right = court_width_doubles/2 - 0.5
    
    line_color = 'white'
    
    ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color) #net
    ax.plot([-court_width/2, -court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width/2, court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width_doubles/2, court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    
    
    light_grass = '#83a462'
    dark_grass = '#739655'
    # Number of stripes and their height
    surfacecode = SurfaceCode.HARD
    if surfacecode == SurfaceCode.GRASS:
        ax.set_facecolor('#83a462')# -> grass court
        num_stripes = 10
        stripe_width = abs(court_draw_width_start - court_draw_width_end) / num_stripes
        for i in range(num_stripes):
            x_start = court_draw_width_start + i*stripe_width
            x_end = x_start + stripe_width
            color = light_grass if i % 2 == 0 else dark_grass
            ax.axvspan(x_start, x_end, alpha=1, color=color)
            #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#83a462')
        stripe_height = (court_length - court_draw_height_end) / num_stripes
    else:
        alpha = 1
        ax.set_facecolor(court_color_x)# -> hard court
        #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#83a462')
        ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        #Behind the baseline
        ax.axhspan(court_length, court_length + 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
def get_ball_locations(row):
    loc_xs = []
    loc_ys = []
    loc_zs = []
    time_step = 0.05
    if np.isnan(row['shot_time_start']) or np.isnan(row['shot_time_end']):
        return None, None, None
    for t in np.arange(row['shot_time_start'], row['shot_time_end'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0'] + row['ArcSvaMatrix_x_1']*t + row['ArcSvaMatrix_x_2']*t**2 + row['ArcSvaMatrix_x_3']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0'] + row['ArcSvaMatrix_y_1']*t + row['ArcSvaMatrix_y_2']*t**2 + row['ArcSvaMatrix_y_3']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0'] + row['ArcSvaMatrix_z_1']*t + row['ArcSvaMatrix_z_2']*t**2 + row['ArcSvaMatrix_z_3']*t**3)
    if ((row['is_last_shot'] == 1) & (row['is_in_the_net'] == 0)):
        for t in np.arange(row['shot_time_end'], row['shot_time_end']+0.7, time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)
            
    if abs(row['shot_time_end'] - row['shot_time_start_next'])>0.002: #there is trace after bounce (no volley played on the next shot)
        for t in np.arange(row['shot_time_end'], row['shot_time_start_next'], time_step):
            loc_xs.append(row['ArcSvaMatrix_x_0_next'] + row['ArcSvaMatrix_x_1_next']*t + row['ArcSvaMatrix_x_2_next']*t**2 + row['ArcSvaMatrix_x_3_next']*t**3)
            loc_ys.append(row['ArcSvaMatrix_y_0_next'] + row['ArcSvaMatrix_y_1_next']*t + row['ArcSvaMatrix_y_2_next']*t**2 + row['ArcSvaMatrix_y_3_next']*t**3)
            loc_zs.append(row['ArcSvaMatrix_z_0_next'] + row['ArcSvaMatrix_z_1_next']*t + row['ArcSvaMatrix_z_2_next']*t**2 + row['ArcSvaMatrix_z_3_next']*t**3)

        
    #Abs the x and mirror the y to get serves always from one side
    if loc_xs[0] > 0:
        loc_ys = [-1 * i for i in loc_ys]
        loc_xs = [-1 * i for i in loc_xs]
    
    if loc_xs[0] * loc_xs[-1] > 0:
        return None, None, None
    else:
        return loc_xs, loc_ys, loc_zs

    


def slope(x1, y1, x2, y2):
        m = (y2-y1)/(x2-x1)
        return m
def set_court_trajectory(ax, court_draw_width_start = -8.5, court_draw_width_end = 8.5):
    #court_draw_width_start = -6.5
    #court_draw_width_end = 6.5
    court_draw_height_end = 17 #17
    court_draw_height_start = -17 #-17
    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    
    linewidth = 3    
    court_width = 8.23
    court_length = 11.89
    court_width_doubles = 8.23 + 1.37 + 1.37
    
    net_post_x_left = -court_width_doubles/2 + 0.5
    net_post_x_right = court_width_doubles/2 - 0.5
    
    line_color = 'white'
    
    ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color) #net
    ax.plot([-court_width/2, -court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width/2, court_width/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
    ax.plot([court_width_doubles/2, court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1*court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    #Net post
    #ax.add_artist(Circle((net_post_x_left, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_artist(Circle((net_post_x_right, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_patch(Rectangle((net_post_x_left - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    #ax.add_patch(Rectangle((net_post_x_right - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    
#Court color
    #ax.set_facecolor(court_color_x)
    #Out of court color
    #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=0.8, color=out_of_court_color_x)
    #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=0.8, color=out_of_court_color_x)
    
    #Court color
    #ax.set_facecolor('#d45e3e')# -> clay court
    
    
    #Out of court color
    
    light_grass = '#83a462'
    dark_grass = '#739655'
    # Number of stripes and their height
    surfacecode = SurfaceCode.HARD
    if surfacecode == SurfaceCode.GRASS:
        ax.set_facecolor('#83a462')# -> grass court
        num_stripes = 10
        stripe_width = abs(court_draw_width_start - court_draw_width_end) / num_stripes
        for i in range(num_stripes):
            x_start = court_draw_width_start + i*stripe_width
            x_end = x_start + stripe_width
            color = light_grass if i % 2 == 0 else dark_grass
            ax.axvspan(x_start, x_end, alpha=1, color=color)
            #ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#83a462')
        stripe_height = (court_length - court_draw_height_end) / num_stripes
    else:
        alpha = 1
        ax.set_facecolor(court_color_x)# -> hard court
        ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        #Behind the baseline
        ax.axhspan(court_length, court_length + 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
        ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=out_of_court_color_x, zorder = -999)
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[22]:





# In[23]:


#df_ryb = df


# In[ ]:




    
    



    
    






# In[25]:


from pdf_generator.models.enums import (
    Fonts,
    Color,
    CourtSide,
    ReturnDirection,
    ServeDirection,
    Offset,
    ShotType,
    SurfaceCode,
)

from pdf_generator.visuals.templates import serve_location_template, ColorPreset, good_returns_template

from pdf_generator.models.enums import (
    Fonts,
    Color,
    CourtSide,
    ReturnDirection,
    ServeDirection,
    Offset,
    ShotType,
    SurfaceCode,
)
surfacecode = SurfaceCode.HARD
from pdf_generator.visuals.templates import serve_location_template, ColorPreset, good_returns_template
def create_serve_visual(df, server, returner, serve_number):

    serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name == server)]
    ad_serves = serves[serves.serve_deuce_or_ad == 'ad']
    deuce_serves = serves[serves.serve_deuce_or_ad == 'deuce']

    deuce_serves_T = deuce_serves[deuce_serves.serve_direction == 'T']
    deuce_serves_W = deuce_serves[deuce_serves.serve_direction == 'W']
    deuce_serves_B = deuce_serves[deuce_serves.serve_direction == 'B']

    ad_serves_T = ad_serves[ad_serves.serve_direction == 'T']
    ad_serves_W = ad_serves[ad_serves.serve_direction == 'W']
    ad_serves_B = ad_serves[ad_serves.serve_direction == 'B']

    all_deuce_serves = len(deuce_serves_T) + len(deuce_serves_B) + len(deuce_serves_W)
    all_ad_serves = len(ad_serves_T) + len(ad_serves_B) + len(ad_serves_W)

    def get_ratio(x, y):
        if not y or np.isnan(y):
            return 0
        return int(round(100.0 * x / y))

    arrows_widths = [
        get_ratio(len(ad_serves_W), all_ad_serves),
        get_ratio(len(ad_serves_B), all_ad_serves),
        get_ratio(len(ad_serves_T), all_ad_serves),
        get_ratio(len(deuce_serves_T), all_deuce_serves),
        get_ratio(len(deuce_serves_B), all_deuce_serves),
        get_ratio(len(deuce_serves_W), all_deuce_serves),
    ]
    arrows_numbers= [f'{x}%' for x in arrows_widths]
    numbers = [len(ad_serves_W), len(ad_serves_B), len(ad_serves_T), len(deuce_serves_T), len(deuce_serves_B), len(deuce_serves_W)]
    pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME == server]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]

    court = serve_location_template(
        player_name=server,
        opponent_name=returner,
        serve_no='1st' if serve_number == 1 else '2nd',
        arrows_widths= arrows_widths,
        arrows_numbers= arrows_numbers,
        surface= surfacecode,
        numbers= numbers,
        pies_percentages=pies_percentages,
        preset=ColorPreset.ORANGE,
    )
    return court


# In[26]:


def create_return_visual(df, server, returner, serve_number):

    serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name == server)]
    ad_serves = serves[serves.serve_deuce_or_ad == 'ad']
    deuce_serves = serves[serves.serve_deuce_or_ad == 'deuce']

    deuce_serves_T = deuce_serves[deuce_serves.serve_direction == 'T']
    deuce_serves_W = deuce_serves[deuce_serves.serve_direction == 'W']
    deuce_serves_B = deuce_serves[deuce_serves.serve_direction == 'B']

    ad_serves_T = ad_serves[ad_serves.serve_direction == 'T']
    ad_serves_W = ad_serves[ad_serves.serve_direction == 'W']
    ad_serves_B = ad_serves[ad_serves.serve_direction == 'B']

    all_deuce_serves = len(deuce_serves_T) + len(deuce_serves_B) + len(deuce_serves_W)
    all_ad_serves = len(ad_serves_T) + len(ad_serves_B) + len(ad_serves_W)

    def get_ratio(x, y):
        if not y or np.isnan(y):
            return 0
        return int(round(100.0 * x / y))

    arrows_widths = [
        get_ratio(len(deuce_serves_T), all_deuce_serves),
        get_ratio(len(deuce_serves_B), all_deuce_serves),
        get_ratio(len(deuce_serves_W), all_deuce_serves),
        get_ratio(len(ad_serves_W), all_ad_serves),
        get_ratio(len(ad_serves_B), all_ad_serves),
        get_ratio(len(ad_serves_T), all_ad_serves),
        
    ]
    #arrows_widths = arrows_widths[::-1]
    
    arrows_numbers= [f'{x}%' for x in arrows_widths][::-1]
    numbers = [len(ad_serves_W), len(ad_serves_B), len(ad_serves_T), len(deuce_serves_T), len(deuce_serves_B), len(deuce_serves_W)][::-1]
    pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME != server]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]
    pies_percentages = pies_percentages[::-1]
    #print(arrows_widths)
    court = good_returns_template(
        player_name=returner,
        opponent_name=server,
        serve_no='1st' if serve_number == 1 else '2nd',
        arrows_widths= arrows_widths,
        arrows_numbers= arrows_numbers,
        surface= surfacecode,
        numbers= numbers,
        pies_percentages=pies_percentages,
        preset=ColorPreset.ORANGE,
    )
    return court

def create_return_visual(df, server, returner, serve_number):

    serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name == server)]
    serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name != returner)]
    ad_serves = serves[serves.serve_deuce_or_ad == 'ad']
    deuce_serves = serves[serves.serve_deuce_or_ad == 'deuce']

    deuce_serves_T = deuce_serves[deuce_serves.serve_direction == 'T']
    deuce_serves_W = deuce_serves[deuce_serves.serve_direction == 'W']
    deuce_serves_B = deuce_serves[deuce_serves.serve_direction == 'B']

    ad_serves_T = ad_serves[ad_serves.serve_direction == 'T']
    ad_serves_W = ad_serves[ad_serves.serve_direction == 'W']
    ad_serves_B = ad_serves[ad_serves.serve_direction == 'B']

    all_deuce_serves = len(deuce_serves_T) + len(deuce_serves_B) + len(deuce_serves_W)
    all_ad_serves = len(ad_serves_T) + len(ad_serves_B) + len(ad_serves_W)

    def get_ratio(x, y):
        if not y or np.isnan(y):
            return 0
        return int(round(100.0 * x / y))

    arrows_widths = [
        get_ratio(len(ad_serves_W), all_ad_serves),
        get_ratio(len(ad_serves_B), all_ad_serves),
        get_ratio(len(ad_serves_T), all_ad_serves),
        get_ratio(len(deuce_serves_T), all_deuce_serves),
        get_ratio(len(deuce_serves_B), all_deuce_serves),
        get_ratio(len(deuce_serves_W), all_deuce_serves),
    ]
    #arrows_widths = arrows_widths[::-1]
    
    arrows_numbers= [f'{x}%' for x in arrows_widths][::-1]
    arrows_widths = [
        get_ratio(len(deuce_serves_W), all_deuce_serves),
        get_ratio(len(deuce_serves_B), all_deuce_serves),
        get_ratio(len(deuce_serves_T), all_deuce_serves),
        get_ratio(len(ad_serves_T), all_ad_serves),
        get_ratio(len(ad_serves_B), all_ad_serves),
        get_ratio(len(ad_serves_W), all_ad_serves),
        
    ]
    numbers = [len(ad_serves_W), len(ad_serves_B), len(ad_serves_T), len(deuce_serves_T), len(deuce_serves_B), len(deuce_serves_W)][::-1]
    pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME != server]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]
    pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME == returner]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]
    pies_percentages = pies_percentages[::-1]
    #print(arrows_widths)
    court = good_returns_template(
        player_name=returner,
        opponent_name=server,
        serve_no='1st' if serve_number == 1 else '2nd',
        arrows_widths= arrows_widths,
        arrows_numbers= arrows_numbers,
        surface= surfacecode,
        numbers= numbers,
        pies_percentages=pies_percentages,
        preset=ColorPreset.ORANGE,
    )
    return court


# In[ ]:





# In[27]:
def create_serve_comparison(data, report_id):
    try:
        import os
        os.mkdir(str(report_id))
        basa_poc = str(report_id)
        player1 = data[0]['player']
        player2 = data[1]['player']
        matches1 =  data[0]['matches']
        matches2 = data[1]['matches']
        title1 = data[0]['name']
        title2 = data[1]['name']
        tour1 = data[0]['tour']
        tour2 = data[0]['tour']
        print('PLAYER 1')
        print(player1)
        print(matches1)
        print('PLAYER 2')
        print(player2)
        print(matches2)
        df1 =  load_data_all(player1, '', matches1, tour1, [], [])
        df2 =  load_data_all(player2, '', matches2, tour2, [], [])

        from pdf_generator.models.enums import (
        Fonts,
        Color,
        CourtSide,
        ReturnDirection,
        ServeDirection,
        Offset,
        ShotType,
        SurfaceCode,
    )

        from pdf_generator.visuals.templates import  serve_location_template, ColorPreset, good_returns_template
        def create_serve_visual(df, server, returner, serve_number):

            serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name == server)]
            ad_serves = serves[serves.serve_deuce_or_ad == 'ad']
            deuce_serves = serves[serves.serve_deuce_or_ad == 'deuce']

            deuce_serves_T = deuce_serves[deuce_serves.serve_direction == 'T']
            deuce_serves_W = deuce_serves[deuce_serves.serve_direction == 'W']
            deuce_serves_B = deuce_serves[deuce_serves.serve_direction == 'B']

            ad_serves_T = ad_serves[ad_serves.serve_direction == 'T']
            ad_serves_W = ad_serves[ad_serves.serve_direction == 'W']
            ad_serves_B = ad_serves[ad_serves.serve_direction == 'B']

            all_deuce_serves = len(deuce_serves_T) + len(deuce_serves_B) + len(deuce_serves_W)
            all_ad_serves = len(ad_serves_T) + len(ad_serves_B) + len(ad_serves_W)

            def get_ratio(x, y):
                if not y or np.isnan(y):
                    return 0
                return int(round(100.0 * x / y))

            arrows_widths = [
                get_ratio(len(ad_serves_W), all_ad_serves),
                get_ratio(len(ad_serves_B), all_ad_serves),
                get_ratio(len(ad_serves_T), all_ad_serves),
                get_ratio(len(deuce_serves_T), all_deuce_serves),
                get_ratio(len(deuce_serves_B), all_deuce_serves),
                get_ratio(len(deuce_serves_W), all_deuce_serves),
            ]
            arrows_numbers= [f'{x}%' for x in arrows_widths]
            numbers = [len(ad_serves_W), len(ad_serves_B), len(ad_serves_T), len(deuce_serves_T), len(deuce_serves_B), len(deuce_serves_W)]
            pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME == server]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]
            print('BEFORE TEMPLATE')
            court = serve_location_template(
                player_name=server,
                opponent_name=returner,
                serve_no='1st' if serve_number == 1 else '2nd',
                arrows_widths= arrows_widths,
                arrows_numbers= arrows_numbers,
                surface= surfacecode,
                numbers= numbers,
                pies_percentages=pies_percentages,
                preset=ColorPreset.ORANGE,
            )
            return court


        # In[29]:


        df = df2
        serve_number = 2
        server = player2
        serves = df[(df.serve_number == serve_number) & (df.is_shot_in == 1) & (df.shot_no == 1) & (df.server_name == server)]
        ad_serves = serves[serves.serve_deuce_or_ad == 'ad']
        deuce_serves = serves[serves.serve_deuce_or_ad == 'deuce']
        deuce_serves_T = deuce_serves[deuce_serves.serve_direction == 'T']
        deuce_serves_W = deuce_serves[deuce_serves.serve_direction == 'W']
        deuce_serves_B = deuce_serves[deuce_serves.serve_direction == 'B']

        ad_serves_T = ad_serves[ad_serves.serve_direction == 'T']
        ad_serves_W = ad_serves[ad_serves.serve_direction == 'W']
        ad_serves_B = ad_serves[ad_serves.serve_direction == 'B']

        all_deuce_serves = len(deuce_serves_T) + len(deuce_serves_B) + len(deuce_serves_W)
        all_ad_serves = len(ad_serves_T) + len(ad_serves_B) + len(ad_serves_W)

        def get_ratio(x, y):
            if not y or np.isnan(y):
                return 0
            return int(round(100.0 * x / y))

        arrows_widths = [
            get_ratio(len(ad_serves_W), all_ad_serves),
            get_ratio(len(ad_serves_B), all_ad_serves),
            get_ratio(len(ad_serves_T), all_ad_serves),
            get_ratio(len(deuce_serves_T), all_deuce_serves),
            get_ratio(len(deuce_serves_B), all_deuce_serves),
            get_ratio(len(deuce_serves_W), all_deuce_serves),
        ]
        arrows_numbers= [f'{x}%' for x in arrows_widths]
        numbers = [len(ad_serves_W), len(ad_serves_B), len(ad_serves_T), len(deuce_serves_T), len(deuce_serves_B), len(deuce_serves_W)]
        pies_percentages = [get_ratio(len(x[x.PLAYER_WIN_NAME == server]), len(x)) for x in [ad_serves_W, ad_serves_B, ad_serves_T, deuce_serves_T, deuce_serves_B, deuce_serves_W]]


        # In[30]:


        pies_percentages


        # In[31]:


        serves['won'] = serves.PLAYER_WIN_NAME == player2


        # In[32]:


        serves.groupby(['serve_deuce_or_ad', 'serve_direction'])['won'].mean()


        # In[33]:


        df2['won'] = df2.PLAYER_WIN_NAME == player1
        df2[(df2.serve_number == 2)
        & (df2.shot_no == 1)
            & (df2.server_name == player2)
        & (df2.is_shot_in == 1)
        ].groupby(['serve_deuce_or_ad', 'serve_direction'])['won'].mean()


        # In[ ]:





        # In[ ]:





        # In[ ]:





        # In[ ]:





        # In[ ]:





        # In[ ]:





        # In[34]:


        def process_code_for_detailed_serve(df, selected_player_name, tour):
            df_player_serves = df[((df['is_shot_serve']==1)&(df['PLAYER_HIT']==selected_player_name))] 
            df_player_serves = df_player_serves[df_player_serves['CONTACT_X_abs_from_baseline']<1.5]
            df_player_serves = df_player_serves[df_player_serves['CONTACT_X_abs_from_baseline']>-0.8]

            df_player_serves = df_player_serves[df_player_serves['SPEED'] > 90]
            df = df_player_serves
            
            if tour.upper() == 'ATP':
                range_prob_ad = pd.read_csv('NET_SERVE_DETAILED_AD_ATP.csv')
                range_prob_deuce = pd.read_csv('NET_SERVE_DETAILED_DEUCE_ATP.csv')
                speed_range_mapping = {
                120: '<140',
                140: '140-160',
                160: '160-180',
                180: '180-200',
                200: '>200'
                }
            else:
                range_prob_ad = pd.read_csv('NET_SERVE_DETAILED_AD.csv')
                range_prob_deuce = pd.read_csv('NET_SERVE_DETAILED_DEUCE.csv')
                speed_range_mapping = {
                120: '<140',
                140: '140-160',
                160: '160-180',
                180: '>180'
                }
            def apply_net_correction_wta(x):
                if not np.isnan(x['NET_COORD_Y_mirrored']) and x['is_shot_in'] == 0:
                    speed_range = x['SPEED'] // 20 * 20
                    if speed_range < 120:
                        speed_range = 120

                    if tour.upper() == 'ATP':
                        if speed_range > 200:
                            speed_range = 200
                    else:
                        if speed_range > 180:
                            speed_range = 180
                    speed_range = speed_range_mapping[speed_range]
                    position_range = ((x['NET_COORD_Y_mirrored']*100) // 30 * 30) / 100
                    if x['serve_deuce_or_ad'] == 'deuce':
                        range_prob = range_prob_deuce
                        if position_range > 0:
                            position_range = 0

                    else:
                        if position_range < -0.3:
                            position_range = -0.3
                        range_prob = range_prob_ad

                    serve_direction = range_prob[(range_prob['SPEED RANGE'] == speed_range) & (range_prob['Y POSITION'] == position_range)]
                    if serve_direction.empty:
                        #print(x['point_id'], x['SPEED'], x['NET_COORD_Y_mirrored'], speed_range, position_range, x['serve_deuce_or_ad'], 'SHIT!')
                        return 'ET'
                    else:
                        return np.random.choice(
                        serve_direction['serve_direction_detailed'].to_list(),
                        size=1,
                        p=serve_direction['prob'].to_list()
                    )[0]
                else:
                    return x['serve_direction_detailed']
            df['serve_direction_detailed'] = df.apply(apply_net_correction_wta, axis=1)
            return df
            


        # In[ ]:





        # In[35]:


        surfacecode = SurfaceCode.HARD


        # In[36]:


        # P1
        print('BASA POC START')
        import os
        
        create_serve_visual(df1, player1, 'OPPONENTS', 1).save(f'{basa_poc}/p11.png') # 1st serve
        create_serve_visual(df2, player2, 'OPPONENTS', 1).save(f'{basa_poc}/p12.png') # 1st serve
        print('BASA POC END')

        # In[37]:


        # P1
        create_serve_visual(df1, player1, 'OPPONENTS', 2).save(f'{basa_poc}/p_21.png') # 1st serve
        create_serve_visual(df2, player2, 'OPPONENTS', 2).save(f'{basa_poc}/p_22.png') # 1st serve


        # In[38]:


        create_serve_visual(df2, player2, 'OPPONENTS', 2)


        # In[ ]:





        # In[39]:


        df1['won'] = df1.PLAYER_WIN_NAME == player1
        df1[(df1.serve_number == 2)
        & (df1.shot_no == 1)
        & (df1.is_shot_in == 1)].won.mean()


        # In[40]:


        df['won'] = df.PLAYER_WIN_NAME == player1
        df[(df.serve_number == 2)
        & (df.shot_no == 1)
        & (df.is_shot_in == 1)].won.mean()


        # In[41]:


        df2['won'] = df2.PLAYER_WIN_NAME == player1
        df2[(df2.serve_number == 2)
        & (df2.shot_no == 1)
        & (df2.is_shot_in == 1)].groupby(['serve_deuce_or_ad', 'serve_direction'])['won'].mean()


        # In[ ]:





        # In[42]:


        df['won'] = df.PLAYER_WIN_NAME == player1
        df[(df.serve_number == 2)
        & (df.shot_no == 1)
        & (df.is_shot_in == 1)].groupby('match_id').won.mean()


        # In[ ]:





        # In[ ]:





        # In[43]:


        # P2
        def draw_court(title, wbt_lines = True, wbt_detailed_lines = False, grid = False, figsize=(8,8)):
            fig = plt.figure(figsize=figsize)
            #Set image params
            plt.xlim(-4.5, 4.5)
            plt.ylim(-12, 1)
            plt.xlabel('Court width from the center')
            plt.ylabel('Court length from net to baseline')
            plt.title(title)
            if grid:
                plt.grid()
            linewidth = 3
            #mark_size = mark_size
            #draw court
            plt.plot([-court_width/2, court_width/2], [0, 0], linewidth=linewidth, linestyle="--", c='black') #net
            plt.plot([-court_width/2, -court_width/2], [1, -court_length], linewidth=linewidth, linestyle="-", c='black') #sideline
            plt.plot([court_width/2, court_width/2], [1, -court_length], linewidth=linewidth, linestyle="-", c='black') #sideline
            plt.plot([-court_width/2, court_width/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c='black') #baseline
            plt.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c='black') #servisline
            
            plt.plot([0,0], [0, -6.40], linewidth=linewidth, linestyle="-", c='black') #servis center line
            plt.plot([0,0], [court_length-0.2, court_length], linewidth=linewidth, linestyle="-", c='black') #baseline center line   
            
            
            
            tunel_width = 1.37
            if wbt_lines:
                plt.plot([-tunel_width,-tunel_width], [0, -6.40], linewidth=0.5, linestyle="-", c='black') # for T servis
                plt.plot([tunel_width, tunel_width], [0, -6.40], linewidth=0.5, linestyle="-", c='black') # for T servis

                plt.plot([court_width/2 - tunel_width, court_width/2 - tunel_width], [0, -6.40], linewidth=0.5, linestyle="-", c='black') # for w servis
                plt.plot([-court_width/2 + tunel_width, -court_width/2 + tunel_width], [0, -6.40], linewidth=0.5, linestyle="-", c='black') # for w servis
                
                fontsize = 28
                plt.text(-3.70, -1.3, 'W', fontsize=fontsize)
                plt.text(-2.30, -1.3, 'B', fontsize=fontsize)
                plt.text(-0.9, -1.3, 'T', fontsize=fontsize)
                
                plt.text(3.15, -1.3, 'W', fontsize=fontsize)
                plt.text(1.85, -1.3, 'B', fontsize=fontsize)
                plt.text(0.5, -1.3, 'T', fontsize=fontsize)
            
            if wbt_detailed_lines:
                #plt.plot([(-court_width+1)/2, (court_width-1)/2], [-5.40, -5.40], linewidth=0.5, linestyle="-", c='black') #deepshallow
                plt.plot([(-court_width+1)/2, -0.4], [-5.40, -5.40], linewidth=0.5, linestyle="-", c='black') #deepshallow
                plt.plot([0.4, (court_width-1)/2], [-5.40, -5.40], linewidth=0.5, linestyle="-", c='black') #deepshallow
                T_near_the_line = 0.4
                linewidth_detailed = 0.8
                plt.plot([-court_width/2 + 6.40/2.5 + 0.1, -court_width/2 + 0.1], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for EW servis
                plt.plot([court_width/2 - 6.40/2.5 - 0.1, court_width/2 - 0.1], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for EW servis
                
                plt.plot([court_width/2 - tunel_width, court_width/2 - tunel_width], [-3.2, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for W servis
                plt.plot([-court_width/2 + tunel_width, -court_width/2 + tunel_width], [-3.2, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for W servis
                
                plt.plot([-tunel_width,-tunel_width], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for T servis
                plt.plot([tunel_width, tunel_width], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for T servis
                
                plt.plot([-T_near_the_line,-T_near_the_line], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for T servis
                plt.plot([T_near_the_line, T_near_the_line], [0, -6.40], linewidth=linewidth_detailed, linestyle="-", c='black') # for T servis
            
            return fig

        df1_detailed = process_code_for_detailed_serve(df1, player1, tour1)
        df2_detailed = process_code_for_detailed_serve(df2, player2, tour2)

        first_color = '#1f77b4'
        second_color = '#ff7f0e'
        third_color = '#2ca02c'
        forth_color = '#d62728'
        fifth_color = '#9467bd'
        from matplotlib import rcParams
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['DIN Condensed']
        rcParams['font.size'] =18

        from IPython.core.display import display, HTML
        from IPython.display import Markdown
        display(HTML("<style>.container { width:95% !important; }</style>"))
        pd.set_option('display.max_columns', 80)

        #variables to calculate bounce spot in/out
        court_width = 8.23
        court_length = 11.89 #this is for sure correct and checked with HE. if bounce is 11.90 it is out   #23.77 was before 
        center_line_width = 0.026
        #average_ball_impact_size = 0.055 #bedene zverev 1_7_5 point   #0.02
        ball_bounce_width = 0.026
        servis_box_length = 6.40 

        def round_robust(x, decimal=0):
            if x and not np.isnan(x):
                return round(x, decimal)
            else:
                return x
        mark_size = 18
            
        first_color = '#1f77b4'
        second_color = '#ff7f0e'
        second_color_short = '#f9A154'
        third_color = '#2ca02c'
        third_color_short = '#40F140'
        forth_color = '#d62728'
        forth_color_short = '#fA2B2D'
        fifth_color = '#9467bd'
        def plot_serve_placement(df, selected_player_name):
            df_1st_deuce_in = df[(df.serve_number == 1)
                                & (df.is_shot_in == 1)
                                & (df.serve_deuce_or_ad == 'deuce')]
            df_1st_ad_in = df[(df.serve_number == 1)
                                & (df.is_shot_in == 1)
                                & (df.serve_deuce_or_ad == 'ad')]
            title = selected_player_name + ' First serve distribution \n VW  W   B   T   VT     VT   T   B   W   VW'
            fig = draw_court(title, wbt_lines = False, wbt_detailed_lines=True) #plk
            #In
            plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='EW']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='EW']['REBOUND_X_abs']*(-1), c=first_color, s=mark_size)
            #plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='JT']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='JT']['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)

            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=second_color_short, s=mark_size)
            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=third_color_short, s=mark_size)
            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=forth_color_short, s=mark_size)

            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c='black', s=mark_size)

            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)

            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=second_color, s=mark_size)
            plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=third_color, s=mark_size)
            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), c=forth_color, s=mark_size)

            plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='ET']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='ET']['REBOUND_X_abs']*(-1), c=fifth_color, s=mark_size)

            plt.scatter(df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='EW']['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='EW']['REBOUND_X_abs']*(-1), c=fifth_color, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=second_color_short, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=third_color_short, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=forth_color_short, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=second_color, s=mark_size)
            plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=third_color, s=mark_size)



            plt.scatter(df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='ET']['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='ET']['REBOUND_X_abs']*(-1), c=first_color, s=mark_size)

            return fig
        fig1 = plot_serve_placement(df1_detailed, player1)
        fig2 = plot_serve_placement(df2_detailed, player2)
        fig1.savefig(f'{basa_poc}/p21.png')
        fig2.savefig(f'{basa_poc}/p22.png')


        # In[44]:


        # P3
        def robust_round(x):
            if x and not np.isnan(x):
                return round(x)
            else:
                return 'NA'
        def plot_in_perc(df, selected_player_name, serve_stat, tour):
            new_name_for_visuals = ''
            df_2nd_deuce = df[(df.serve_number == 2)
                            & (df.serve_deuce_or_ad == 'deuce')]
            df_2nd_ad = df[(df.serve_number == 2)
                            & (df.serve_deuce_or_ad == 'ad')]
            df_1st = df[df.serve_number == 1]
            df_1st_ad = df_1st[df_1st['serve_deuce_or_ad'] == 'ad']
            df_1st_ad['is_kick'] = False
            if tour.lower() == 'atp':
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['EW', 'JW'])) & (df_1st_ad.SPEED < 183)), 'is_kick'] = True
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['JB'])) & (df_1st_ad.SPEED < 192)), 'is_kick'] = True
            else:
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['EW', 'JW'])) & (df_1st_ad.SPEED < 160)), 'is_kick'] = True
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['JB'])) & (df_1st_ad.SPEED < 170)), 'is_kick'] = True

            df_1st_deuce = df_1st[df_1st['serve_deuce_or_ad'] == 'deuce']
            df_1st_deuce['is_kick'] = False
            if tour.lower() == 'atp':
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['ET', 'JT'])) & (df_1st_deuce.SPEED < 183)), 'is_kick'] = True
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['JB'])) & (df_1st_deuce.SPEED < 189)), 'is_kick'] = True
            else:
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['ET', 'JT'])) & (df_1st_deuce.SPEED < 160)), 'is_kick'] = True
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['JB'])) & (df_1st_deuce.SPEED < 170)), 'is_kick'] = True
                
            column_map = {
            'EW': 'VERY WIDE',
            'JW': 'WIDE',
            'JB': 'BODY',
            'JT': 'T',
            'ET': 'VERY T',
            }

            df_1st_deuce = df_1st_deuce[df_1st_deuce.is_kick == False]

            df_2nd_deuce['won'] = df_2nd_deuce.PLAYER_HIT == df_2nd_deuce.PLAYER_WIN_NAME

            df_2nd_ad['won'] = df_2nd_ad.PLAYER_HIT == df_2nd_ad.PLAYER_WIN_NAME
            table = []
            column_names = ['Serve directions', 'VW', 'W - deep', 'W - short', 'B - deep','B - short', 'T - deep', 'T - short', 'VT']
            table.append(['Serve Placement', 'Metric'] + [''])
            avg_win = []
            avg_in = []
            in_dict_deuce = dict()
            win_dict_deuce = dict()
            expected_win_deuce_dict = dict()
            for column in ['EW', 'JW', 'JB', 'JT', 'ET']:
                current_serve = df_1st_deuce[(df_1st_deuce.serve_direction_detailed == column)]
                current_serve['won'] = current_serve.PLAYER_WIN_NAME == current_serve.PLAYER_HIT
                if column in ['JW', 'JB', 'JT']:
                    current_serve_deep = current_serve[current_serve.REBOUND_X_abs > 5.4]
                    current_serve_short = current_serve[(current_serve.REBOUND_X_abs < 5.4) | (current_serve.REBOUND_X_abs.isna())]
                    avg_win.append(round_robust(current_serve_deep[current_serve_deep.is_shot_in == 1].won.mean()*100, 2))
                    win_dict_deuce[column + '-DEEP'] = round_robust(current_serve_deep[current_serve_deep.is_shot_in == 1].won.mean()*100, 2)
                    avg_in.append(round_robust(current_serve_deep.is_shot_in.mean()*100, 2))
                    in_dict_deuce[column + '-DEEP'] = round_robust(current_serve_deep.is_shot_in.mean()*100, 2)
                    avg_win.append(round_robust(current_serve_short[current_serve_short.is_shot_in == 1].won.mean()*100, 2))
                    win_dict_deuce[column + '-SHORT'] = round_robust(current_serve_short[current_serve_short.is_shot_in == 1].won.mean()*100, 2)
                    avg_in.append(round_robust(current_serve_short.is_shot_in.mean()*100, 2))
                    if len(current_serve_short):
                        in_dict_deuce[column + '-SHORT'] = round_robust(current_serve_short.is_shot_in.mean()*100, 0)
                    else:
                        in_dict_deuce[column + '-SHORT'] = None
                    table.append([column_map[column] + ' - DEEP', 
                                '\n'.join(['Win%', 'In%', 'Expected Win%',  'No. of serves'])] 
                                + ['\n'.join([str(round_robust(current_serve_deep[(current_serve_deep.is_shot_in == 1) ].won.mean()*100, 2)), 
                                                str(round_robust(current_serve_deep.is_shot_in.mean()*100, 2)), 
                                                str(round_robust((current_serve_deep.is_shot_in.mean()*current_serve_deep[(current_serve_deep.is_shot_in.isin([1])) ].won.mean() + (1-current_serve_deep.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)),
                                                str(len(current_serve_deep))])for k in range(1)]    )
                    table.append([column_map[column] + ' - SHORT', 
                                '\n'.join(['Win%', 'In%', 'Expected Win%', 'No. of serves'])] 
                                + ['\n'.join([str(round_robust(current_serve_short[(current_serve_short.is_shot_in == 1)].won.mean()*100, 2)), 
                                                str(round_robust(current_serve_short.is_shot_in.mean()*100, 2)), 
                                                str(round_robust((current_serve_short.is_shot_in.mean()*current_serve_short[(current_serve_short.is_shot_in.isin([1]))].won.mean() + (1-current_serve_short.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)), 
                                                str(len(current_serve_short))])for k in range(1)])

                    expected_win_deuce_dict[column + '-SHORT'] = round_robust((current_serve_short.is_shot_in.mean()*current_serve_short[(current_serve_short.is_shot_in.isin([1]))].won.mean() + (1-current_serve_short.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)
                    expected_win_deuce_dict[column + '-DEEP'] = round_robust((current_serve_deep.is_shot_in.mean()*current_serve_deep[(current_serve_deep.is_shot_in.isin([1])) ].won.mean() + (1-current_serve_deep.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)
                else:
                    avg_win.append(round_robust(current_serve[current_serve.is_shot_in == 1].won.mean()*100, 2))
                    avg_in.append(round_robust(current_serve.is_shot_in.mean()*100, 2))
                    in_dict_deuce[column] = round_robust(current_serve.is_shot_in.mean()*100, 2)
                    win_dict_deuce[column] = round_robust(current_serve[current_serve.is_shot_in == 1].won.mean()*100, 2)
                    table.append([column_map[column], 
                                '\n'.join(['Win%', 'In%', 'Expected Win%', 'No. of serves'])] 
                                                        + ['\n'.join([str(round_robust(current_serve[(current_serve.is_shot_in == 1) ].won.mean()*100, 2)), 
                                                                    str(round_robust(current_serve.is_shot_in.mean()*100, 2)), 
                                                                    str(round_robust((current_serve.is_shot_in.mean()*current_serve[(current_serve.is_shot_in.isin([1])) ].won.mean() + (1-current_serve.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)),
                                                                    str(len(current_serve))])for k in range(1)])
                    expected_win_deuce_dict[column] = round_robust((current_serve.is_shot_in.mean()*current_serve[(current_serve.is_shot_in.isin([1])) ].won.mean() + (1-current_serve.is_shot_in.mean())*df_2nd_deuce['won'].mean())*100, 2)


            #table.append(['Avg Win Rate'] + avg_win)
            #table.append(['Avg In Rate'] + avg_in)
            #display(HTML(tabulate.tabulate(table, tablefmt='html')))

            table = []
            column_names = ['Serve directions', 'VW', 'W - deep', 'W - short', 'B - deep','B - short', 'T - deep', 'T - short', 'VT']
            table.append(['Serve Placement', 'Metric'] + [''])
            avg_win = []
            avg_in = []
            in_dict_ad = dict()
            win_dict_ad = dict()
            expected_win_ad_dict = dict()
            df_1st_ad = df_1st_ad[df_1st_ad.is_kick == False]
            for column in ['EW', 'JW', 'JB', 'JT', 'ET']:
                current_serve = df_1st_ad[(df_1st_ad.serve_direction_detailed == column)]
                current_serve['won'] = current_serve.PLAYER_WIN_NAME == current_serve.PLAYER_HIT
                if column in ['JW', 'JB', 'JT']:
                    current_serve_deep = current_serve[current_serve.REBOUND_X_abs > 5.4]
                    current_serve_short = current_serve[(current_serve.REBOUND_X_abs < 5.4) | (current_serve.REBOUND_X_abs.isna())]
                    avg_win.append(round_robust(current_serve_deep[current_serve_deep.is_shot_in == 1].won.mean()*100, 2))
                    win_dict_ad[column + '-DEEP'] = round_robust(current_serve_deep[current_serve_deep.is_shot_in == 1].won.mean()*100, 2)
                    avg_in.append(round_robust(current_serve_deep.is_shot_in.mean()*100, 2))
                    in_dict_ad[column + '-DEEP'] = round_robust(current_serve_deep.is_shot_in.mean()*100, 2)
                    avg_win.append(round_robust(current_serve_short[current_serve_short.is_shot_in == 1].won.mean()*100, 2))
                    win_dict_ad[column + '-SHORT'] = round_robust(current_serve_short[current_serve_short.is_shot_in == 1].won.mean()*100, 2)
                    avg_in.append(round_robust(current_serve_short.is_shot_in.mean()*100, 2))
                    in_dict_ad[column + '-SHORT'] = round_robust(current_serve_short.is_shot_in.mean()*100)
                    table.append([column_map[column] + ' - DEEP', 
                                '\n'.join(['Win%', 'In%', 'Expected Win%',  'No. of serves'])] 
                                + ['\n'.join([str(round_robust(current_serve_deep[(current_serve_deep.is_shot_in == 1) ].won.mean()*100, 2)), 
                                                str(round_robust(current_serve_deep.is_shot_in.mean()*100, 2)), 
                                                str(round_robust((current_serve_deep.is_shot_in.mean()*current_serve_deep[(current_serve_deep.is_shot_in.isin([1])) ].won.mean() + (1-current_serve_deep.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)),
                                                str(len(current_serve_deep))])for k in range(1)])
                    table.append([column_map[column] + ' - SHORT', 
                                '\n'.join(['Win%', 'In%', 'Expected Win%', 'No. of serves'])] 
                                + ['\n'.join([str(round_robust(current_serve_short[(current_serve_short.is_shot_in == 1)].won.mean()*100, 2)), 
                                                str(round_robust(current_serve_short.is_shot_in.mean()*100, 2)), 
                                                str(round_robust((current_serve_short.is_shot_in.mean()*current_serve_short[(current_serve_short.is_shot_in.isin([1]))].won.mean() + (1-current_serve_short.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)), 
                                                str(len(current_serve_short))])for k in range(1)])
                    expected_win_ad_dict[column + '-SHORT'] = round_robust((current_serve_short.is_shot_in.mean()*current_serve_short[(current_serve_short.is_shot_in.isin([1]))].won.mean() + (1-current_serve_short.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)
                    expected_win_ad_dict[column + '-DEEP'] = round_robust((current_serve_deep.is_shot_in.mean()*current_serve_deep[(current_serve_deep.is_shot_in.isin([1])) ].won.mean() + (1-current_serve_deep.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)

                else:
                    avg_win.append(round_robust(current_serve[current_serve.is_shot_in == 1].won.mean()*100, 2))
                    win_dict_ad[column] = round_robust(current_serve[current_serve.is_shot_in == 1].won.mean()*100, 2)
                    avg_in.append(round_robust(current_serve.is_shot_in.mean()*100, 2))
                    in_dict_ad[column] = round_robust(current_serve.is_shot_in.mean()*100, 0)
                    table.append([column_map[column], 
                                '\n'.join(['Win%', 'In%', 'Expected Win%', 'No. of serves'])] 
                                                        + ['\n'.join([str(round_robust(current_serve[(current_serve.is_shot_in == 1) ].won.mean()*100, 2)), 
                                                                    str(round_robust(current_serve.is_shot_in.mean()*100, 2)), 
                                                                    str(round_robust((current_serve.is_shot_in.mean()*current_serve[(current_serve.is_shot_in.isin([1])) ].won.mean() + (1-current_serve.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)),
                                                                    str(len(current_serve))])for k in range(1)])

                    expected_win_ad_dict[column] = round_robust((current_serve.is_shot_in.mean()*current_serve[(current_serve.is_shot_in.isin([1])) ].won.mean() + (1-current_serve.is_shot_in.mean())*df_2nd_ad['won'].mean())*100, 2)
            #table.append(['Avg Win Rate'] + avg_win)
            #table.append(['Avg In Rate'] + avg_in)
            #display(HTML(tabulate.tabulate(table, tablefmt='html')))
            
            ## first_color = '#1f77b4'
            second_color = '#ff7f0e'
            second_color_short = '#f9A154'
            third_color = '#2ca02c'
            third_color_short = '#40F140'
            forth_color = '#d62728'
            forth_color_short = '#fA2B2D'
            fifth_color = '#9467bd'
            title = selected_player_name + f' First serve distribution (FLAT SERVES ONLY) {serve_stat.upper()}% \n {new_name_for_visuals} \n VW  W   B   T   VT     VT   T   B   W   VW'
            fig = draw_court(title, wbt_lines = False, wbt_detailed_lines=True) #plk
            #In

            #plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='EW']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='EW']['REBOUND_X_abs']*(-1), c=first_color, s=mark_size)
            #plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='JT']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='JT']['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)

            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=second_color_short, s=mark_size)
            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=third_color_short, s=mark_size)
            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=forth_color_short, s=mark_size)

            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c='black', s=mark_size)

            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)

            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JW') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=second_color, s=mark_size)
            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JB') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=third_color, s=mark_size)
            #plt.scatter(df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[(df_1st_deuce_in['serve_direction_detailed']=='JT') & (df_1st_deuce_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), c=forth_color, s=mark_size)

            #plt.scatter(df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='ET']['REBOUND_Y_mirrored']*(-1), df_1st_deuce_in[df_1st_deuce_in['serve_direction_detailed']=='ET']['REBOUND_X_abs']*(-1), c=fifth_color, s=mark_size)

            #plt.scatter(df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='EW']['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='EW']['REBOUND_X_abs']*(-1), c=fifth_color, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=second_color_short, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=third_color_short, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs < 5.4)]['REBOUND_X_abs']*(-1), c=forth_color_short, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JW') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=forth_color, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JT') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=second_color, s=mark_size)
            #plt.scatter(df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[(df_1st_ad_in['serve_direction_detailed']=='JB') & (df_1st_ad_in.REBOUND_X_abs > 5.4)]['REBOUND_X_abs']*(-1), c=third_color, s=mark_size)

            def robust_round(x):
                if x and not np.isnan(x):
                    return round(x)
                else:
                    return 'NA'
            if serve_stat == 'in':
                plt.text(-3.8, -5, f'{robust_round(in_dict_ad["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.2, -6, f'{robust_round(in_dict_ad["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.1, -5, f'{robust_round(in_dict_ad["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -6, f'{robust_round(in_dict_ad["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -5, f'{robust_round(in_dict_ad["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(in_dict_ad["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(in_dict_ad["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(in_dict_ad["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(in_dict_ad["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.20, -5.5, f'{robust_round(in_dict_ad["ET"])}%', ha="center", va="center", size=23, c='black')

                plt.text(3.8, -5, f'{robust_round(in_dict_deuce["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.2, -6, f'{robust_round(in_dict_deuce["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.1, -5, f'{robust_round(in_dict_deuce["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -6, f'{robust_round(in_dict_deuce["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -5, f'{robust_round(in_dict_deuce["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(in_dict_deuce["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(in_dict_deuce["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(in_dict_deuce["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(in_dict_deuce["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.3, -5.5, f'{robust_round(in_dict_deuce["ET"])}%', ha="center", va="center", size=23, c='black')
            elif serve_stat == 'expected win':
                plt.text(-3.8, -5, f'{robust_round(expected_win_ad_dict["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.2, -6, f'{robust_round(expected_win_ad_dict["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.1, -5, f'{robust_round(expected_win_ad_dict["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -6, f'{robust_round(expected_win_ad_dict["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -5, f'{robust_round(expected_win_ad_dict["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(expected_win_ad_dict["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(expected_win_ad_dict["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(expected_win_ad_dict["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(expected_win_ad_dict["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.20, -5.5, f'{robust_round(expected_win_ad_dict["ET"])}%', ha="center", va="center", size=23, c='black')

                plt.text(3.8, -5, f'{robust_round(expected_win_deuce_dict["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.2, -6, f'{robust_round(expected_win_deuce_dict["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.1, -5, f'{robust_round(expected_win_deuce_dict["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -6, f'{robust_round(expected_win_deuce_dict["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -5, f'{robust_round(expected_win_deuce_dict["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(expected_win_deuce_dict["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(expected_win_deuce_dict["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(expected_win_deuce_dict["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(expected_win_deuce_dict["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.3, -5.5, f'{robust_round(expected_win_deuce_dict["ET"])}%', ha="center", va="center", size=23, c='black')
            elif serve_stat == 'win':
                plt.text(-3.8, -5, f'{robust_round(win_dict_ad["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.2, -6, f'{robust_round(win_dict_ad["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-3.1, -5, f'{robust_round(win_dict_ad["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -6, f'{robust_round(win_dict_ad["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-2.1, -5, f'{robust_round(win_dict_ad["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(win_dict_ad["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(win_dict_ad["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -6, f'{robust_round(win_dict_ad["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.8, -5, f'{robust_round(win_dict_ad["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(-0.20, -5.5, f'{robust_round(win_dict_ad["ET"])}%', ha="center", va="center", size=23, c='black')

                plt.text(3.8, -5, f'{robust_round(win_dict_deuce["EW"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.2, -6, f'{robust_round(win_dict_deuce["JW-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(3.1, -5, f'{robust_round(win_dict_deuce["JW-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -6, f'{robust_round(win_dict_deuce["JB-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(2.1, -5, f'{robust_round(win_dict_deuce["JB-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(win_dict_deuce["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(win_dict_deuce["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -6, f'{robust_round(win_dict_deuce["JT-DEEP"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.8, -5, f'{robust_round(win_dict_deuce["JT-SHORT"])}%', ha="center", va="center", size=23, c='black')
                plt.text(0.3, -5.5, f'{robust_round(win_dict_deuce["ET"])}%', ha="center", va="center", size=23, c='black')



            #plt.scatter(df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='ET']['REBOUND_Y_mirrored']*(-1), df_1st_ad_in[df_1st_ad_in['serve_direction_detailed']=='ET']['REBOUND_X_abs']*(-1), c=first_color, s=mark_size)


            return fig
        
        plot_in_perc(df1_detailed, player1, 'in', tour1).savefig(f'{basa_poc}/p31.png')
        plot_in_perc(df1_detailed, player1, 'win', tour1).savefig(f'{basa_poc}/p61.png')
        plot_in_perc(df1_detailed, player1, 'expected win', tour1).savefig(f'{basa_poc}/p81.png')

        plot_in_perc(df2_detailed, player2, 'in', tour2).savefig(f'{basa_poc}/p32.png')
        plot_in_perc(df2_detailed, player2, 'win', tour2).savefig(f'{basa_poc}/p62.png')
        plot_in_perc(df2_detailed, player2, 'expected win', tour2).savefig(f'{basa_poc}/p82.png')


        # In[45]:


        # P7

        def max_speed_visual(df, selected_player_name, tour):
            df_1st = df[df.serve_number == 1]
            df_1st_ad = df_1st[df_1st['serve_deuce_or_ad'] == 'ad']
            df_1st_ad['is_kick'] = False
            if tour.lower() == 'atp':
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['EW', 'JW'])) & (df_1st_ad.SPEED < 183)), 'is_kick'] = True
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['JB'])) & (df_1st_ad.SPEED < 192)), 'is_kick'] = True
            else:
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['EW', 'JW'])) & (df_1st_ad.SPEED < 160)), 'is_kick'] = True
                df_1st_ad.loc[((df_1st_ad.serve_direction_detailed.isin(['JB'])) & (df_1st_ad.SPEED < 170)), 'is_kick'] = True

            df_1st_deuce = df_1st[df_1st['serve_deuce_or_ad'] == 'deuce']
            df_1st_deuce['is_kick'] = False
            if tour.lower() == 'atp':
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['ET', 'JT'])) & (df_1st_deuce.SPEED < 183)), 'is_kick'] = True
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['JB'])) & (df_1st_deuce.SPEED < 189)), 'is_kick'] = True
            else:
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['ET', 'JT'])) & (df_1st_deuce.SPEED < 160)), 'is_kick'] = True
                df_1st_deuce.loc[((df_1st_deuce.serve_direction_detailed.isin(['JB'])) & (df_1st_deuce.SPEED < 170)), 'is_kick'] = True
                
            title = selected_player_name + ' 1st Flat Serve in \n Average speed [km/h] \n (Max speed) [km/h]'
            fig = draw_court(title, wbt_lines = True)
            font = {'family': 'serif',
                    'color':  'black',
                    'weight': 'normal',
                    'size': 14,
                    }
            
            #In
            df_1st_deuce_W = df_1st_deuce[df_1st_deuce['serve_direction'] == 'W']
            df_1st_deuce_B = df_1st_deuce[df_1st_deuce['serve_direction'] == 'B']
            df_1st_deuce_T = df_1st_deuce[df_1st_deuce['serve_direction'] == 'T']
            
            df_1st_deuce_W = df_1st_deuce[df_1st_deuce['serve_direction'] == 'W']
            df_1st_deuce_B = df_1st_deuce[df_1st_deuce['serve_direction'] == 'B']
            df_1st_deuce_T = df_1st_deuce[df_1st_deuce['serve_direction'] == 'T']
            df_1st_ad_W = df_1st_ad[df_1st_ad['serve_direction'] == 'W']
            df_1st_ad_B = df_1st_ad[df_1st_ad['serve_direction'] == 'B']
            df_1st_ad_T = df_1st_ad[df_1st_ad['serve_direction'] == 'T']
        
            
            B_1st_in_deuce_T_speed_avg  = round(df_1st_deuce_T[df_1st_deuce_T.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_deuce_T_speed_max = round(df_1st_deuce_T[df_1st_deuce_T.is_kick == False]['SPEED'].max(), 1)
            B_1st_in_deuce_B_speed_avg = round(df_1st_deuce_B[df_1st_deuce_B.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_deuce_B_speed_max = round(df_1st_deuce_B[df_1st_deuce_B.is_kick == False]['SPEED'].max(), 1)
            B_1st_in_deuce_W_speed_avg = round(df_1st_deuce_W[df_1st_deuce_W.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_deuce_W_speed_max = round(df_1st_deuce_W[df_1st_deuce_W.is_kick == False]['SPEED'].max(), 1)

            B_1st_in_ad_T_speed_avg  = round(df_1st_ad_T[df_1st_ad_T.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_ad_T_speed_max = round(df_1st_ad_T[df_1st_ad_T.is_kick == False]['SPEED'].max(), 1)
            B_1st_in_ad_B_speed_avg = round(df_1st_ad_B[df_1st_ad_B.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_ad_B_speed_max = round(df_1st_ad_B[df_1st_ad_B.is_kick == False]['SPEED'].max(), 1)
            B_1st_in_ad_W_speed_avg = round(df_1st_ad_W[df_1st_ad_W.is_kick == False]['SPEED'].mean(), 1)
            B_1st_in_ad_W_speed_max = round(df_1st_ad_W[df_1st_ad_W.is_kick == False]['SPEED'].max(), 1)


            
            plt.text(3.0, -4.8, B_1st_in_deuce_W_speed_avg, fontdict=font)
            plt.text(2.9, -5.3, '(' + str(B_1st_in_deuce_W_speed_max) + ')', fontdict=font)

            plt.text(1.65, -4.8, B_1st_in_deuce_B_speed_avg, fontdict=font)
            plt.text(1.55, -5.3, '(' + str(B_1st_in_deuce_B_speed_max) + ')', fontdict=font)

            plt.text(0.25, -4.8, B_1st_in_deuce_T_speed_avg, fontdict=font)
            plt.text(0.15, -5.3, '(' + str(B_1st_in_deuce_T_speed_max) + ')', fontdict=font)

            plt.text(-3.85, -4.8, B_1st_in_ad_W_speed_avg, fontdict=font)
            plt.text(-3.95, -5.3, '(' + str(B_1st_in_ad_W_speed_max) + ')', fontdict=font)

            plt.text(-2.45, -4.8, B_1st_in_ad_B_speed_avg, fontdict=font)
            plt.text(-2.55, -5.3, '(' + str(B_1st_in_ad_B_speed_max) + ')', fontdict=font)

            plt.text(-1.15, -4.8, B_1st_in_ad_T_speed_avg , fontdict=font)
            plt.text(-1.25, -5.3, '(' + str(B_1st_in_ad_T_speed_max) + ')', fontdict=font)


            
            return fig
        max_speed_visual(df1_detailed, player1, tour1).savefig(f'{basa_poc}/p71.png')
        max_speed_visual(df2_detailed, player2, tour2).savefig(f'{basa_poc}/p72.png')

        #fig.savefig(folder_save_images + selected_player_initials + '; 1st serve speeds', bbox_inches='tight')


        # In[46]:


        # P9, 12

        create_return_visual(df1, 'OPPONENTS', player1, 1).save(f'{basa_poc}/p91.png')
        create_return_visual(df2, 'OPPONENTS', player2, 1).save(f'{basa_poc}/p92.png')
        create_return_visual(df1, 'OPPONENTS', player1, 2).save(f'{basa_poc}/p121.png')
        create_return_visual(df2, 'OPPONENTS', player2, 2).save(f'{basa_poc}/p122.png')


        # In[47]:


        def add_subplot_axes(ax,rect,axisbg='w'):
            fig = plt.gcf()
            box = ax.get_position()
            width = box.width    
            height = box.height
            inax_position  = ax.transAxes.transform(rect[0:2])
            transFigure = fig.transFigure.inverted()
            infig_position = transFigure.transform(inax_position)    
            x = infig_position[0]
            y = infig_position[1]
            width *= rect[2]
            height *= rect[3]  # <= Typo was here
            subax = fig.add_axes([x,y,width,height],facecolor=axisbg)
            x_labelsize = subax.get_xticklabels()[0].get_size()
            y_labelsize = subax.get_yticklabels()[0].get_size()
            x_labelsize *= rect[2]**0.5
            y_labelsize *= rect[3]**0.5
            subax.xaxis.set_tick_params(labelsize=x_labelsize)
            subax.yaxis.set_tick_params(labelsize=y_labelsize)
            return subax

        def set_embeded_graphs(ax):
            #For all embeded plots
            height = 0.10
            width = 0.16
            y_pos = 0.72
            
            #1
            x_pos = 0.22    
            rect = [x_pos,y_pos,width,height]
            subax1 = add_subplot_axes(ax,rect)
            
            #2
            x_pos = 0.42
            rect = [x_pos,y_pos,width,height]
            subax2 = add_subplot_axes(ax,rect)
            
            #3
            x_pos = 0.625
            rect = [x_pos,y_pos,width,height]
            subax3 = add_subplot_axes(ax,rect)
            
            all_axes = [subax1, subax2, subax3]
            
            for axis in all_axes:
                axis.get_xaxis().set_visible(False)
                axis.get_yaxis().set_visible(False)
                
            return subax1, subax2, subax3

        def set_embeded_graphs(ax):
            #For all embeded plots
            height = 0.10
            width = 0.16
            y_pos = 0.8
            
            #1
            x_pos = 0.154 # 0.23
            rect = [x_pos,y_pos,width,height]
            subax1 = add_subplot_axes(ax,rect)
            
            #2
            x_pos = 0.406 # 0.42
            rect = [x_pos,y_pos,width,height]
            subax2 = add_subplot_axes(ax,rect)
            
            #3
            x_pos = 0.66
            rect = [x_pos,y_pos,width,height]
            subax3 = add_subplot_axes(ax,rect)
            
            all_axes = [subax1, subax2, subax3]
            
            for axis in all_axes:
                axis.get_xaxis().set_visible(False)
                axis.get_yaxis().set_visible(False)
            return subax1, subax2, subax3

        def set_half_court(ax):
            court_draw_width_start = -6.5
            court_draw_width_end = 6.5
            court_draw_height_end = 8
            court_draw_height_start = -1
            ax.set_xlim((court_draw_width_start, court_draw_width_end))
            ax.set_ylim((court_draw_height_start, court_draw_height_end))
            
            linewidth = 3    
            court_width = 8.23
            court_length = 11.89
            court_width_doubles = 8.23 + 1.37 + 1.37
            
            net_post_x_left = -court_width_doubles/2 + 0.5
            net_post_x_right = court_width_doubles/2 - 0.5
            
            line_color = 'white'
            
            ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color) #net
            ax.plot([-court_width/2, -court_width/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
            ax.plot([court_width/2, court_width/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline
            ax.plot([court_width_doubles/2, court_width_doubles/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
            ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color) #sideline doubles
            ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
            #ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
            ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
            #ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
            ax.plot([0,0], [-1, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
            ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
            #ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
            
            #Net post
            #ax.add_artist(Circle((net_post_x_left, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
            #ax.add_artist(Circle((net_post_x_right, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
            #ax.add_patch(Rectangle((net_post_x_left - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
            #ax.add_patch(Rectangle((net_post_x_right - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
            
            court_color = '#62666d'
            around_court_color = '#bdc1c3'
            #surfaces = ['hard']
            if len(surfaces) != 1:
                #Court color
                ax.set_facecolor(court_color)
                #Out of court color
                ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=0.8, color=around_court_color)
                ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=0.8, color=around_court_color)
            else:
                if surfaces[0].lower() == 'grass':
                    light_grass = '#83a462'
                    dark_grass = '#739655'
                    ax.set_facecolor(light_grass)# -> grass court
                    num_stripes = 10
                    stripe_width = abs(court_draw_width_start - court_draw_width_end) / num_stripes
                    for i in range(num_stripes):
                        x_start = court_draw_width_start + i*stripe_width
                        x_end = x_start + stripe_width
                        color = light_grass if i % 2 == 0 else dark_grass
                        ax.axvspan(x_start, x_end, alpha=1, color=color, zorder = -999)
                else:
                    court_color = '#d45e3e' if surfaces[0].lower() == 'clay' else '#1F78B4'
                    around_court_color = '#d45e3e' if surfaces[0].lower() == 'clay' else '#78C0E8'
                    #Court color
                    ax.set_facecolor(court_color)
                    #Out of court color
                    ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=0.8, color=around_court_color)
                    ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=0.8, color=around_court_color)
            
            #Hide border
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            
            #Hide axes labels and ticks
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            
        def draw_serve_points(df_player_serves, ax, match_name, is_1st_serve, is_serve_deuce_side, selected_player_name):    
            c_green = '#A3FF74' #'#89E381'
            c_orange = '#FF7F00' #'#D27E24'
            c_red = '#E61A25' #'#C61A25' #'#BB2D3B'
            c_gray = '#7C8F9F'
            
            df_player_serves = df_player_serves[df_player_serves['SPEED'] > 20]
            
            if is_1st_serve:
                df_serve = df_player_serves[df_player_serves['FIRST_SERVE']==1]
            else:
                df_serve = df_player_serves[df_player_serves['SECOND_SERVE']==1]
            
            if is_serve_deuce_side:
                df_serve = df_serve[df_serve['serve_deuce_or_ad'] == 'deuce']
            else:
                df_serve = df_serve[df_serve['serve_deuce_or_ad'] == 'ad']
                
            if len(df_serve) == 0:
                print('NO DATA!')
                return
                
            df_serve_in = df_serve[df_serve['is_shot_in'] == 1]
            df_serve_not_in = df_serve[df_serve['is_shot_in'] == 0]
            df_serve_not_in_net_and_not_in = df_serve[(df_serve['is_shot_in'] == 0) & (df_serve['is_in_the_net'] == 0)]
            df_serve_in_net = df_serve[df_serve['is_in_the_net'] == 1]
            
            #Noise. If serve is in there should be Player_win_name
            df_serve_in = df_serve_in.dropna(subset=['PLAYER_WIN_NAME'])
            
            df_serve_in_win = df_serve_in[df_serve_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_in_lose = df_serve_in[~df_serve_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_W_in = df_serve_in[df_serve_in['serve_direction'] == 'W']
            df_serve_B_in = df_serve_in[df_serve_in['serve_direction'] == 'B']
            df_serve_T_in = df_serve_in[df_serve_in['serve_direction'] == 'T']
            df_serve_W = df_serve[df_serve['serve_direction'] == 'W']
            df_serve_B = df_serve[df_serve['serve_direction'] == 'B']
            df_serve_T = df_serve[df_serve['serve_direction'] == 'T']

            df_serve_W_in_win = df_serve_W_in[df_serve_W_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_W_in_lose = df_serve_W_in[~df_serve_W_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_B_in_win = df_serve_B_in[df_serve_B_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_B_in_lose = df_serve_B_in[~df_serve_B_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_T_in_win = df_serve_T_in[df_serve_T_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]
            df_serve_T_in_lose = df_serve_T_in[~df_serve_T_in['PLAYER_WIN_NAME'].str.contains(selected_player_name)]    

            
            #Draw court
            set_half_court(ax)

            #Draw points
            #Set params
            min_speed = min(df_serve['SPEED'].values)
            alpha = 0.7
            power = 1.05 #1.15   
            #Min speed is needed to make nicer markers, that differentiate more on the size (serve speed)
            if min_speed < 100:
                subtract_speed = 70        
            elif min_speed < 120:
                subtract_speed = 80
            elif min_speed < 140:
                subtract_speed = 100
            elif min_speed < 160:
                subtract_speed = 120
            elif min_speed < 180:
                subtract_speed = 140
            else: 
                subtract_speed = 160
            
            subtract_speed = min(80, min(df_serve['SPEED'], default=80) -5 ) #80 (-5 so that it is not size = 0 if serve is slower than 80)
            
            #Serves in win    
            #ax.scatter(df_serve_in_win['REBOUND_Y_mirrored'].values, df_serve_in_win['REBOUND_X_abs'].values, s = (df_serve_in_win['SPEED'] - subtract_speed)**power, label= selected_player_initials + ' won the point', c = c_green, alpha = alpha, edgecolors='black', zorder=11)        
            #Because random zorder we draw each point separately
            for i, row in df_serve_in_win.iterrows():        
                ax.scatter(row['REBOUND_Y_mirrored'], row['REBOUND_X_abs'], s = (row['SPEED'] - subtract_speed)**power, c = c_green, alpha = alpha, edgecolors='black', zorder=np.random.randint(11, 13))        
            #We draw one point again with label, because we need only 1 label
            for i, row in df_serve_in_win.head(1).iterrows():        
                ax.scatter(row['REBOUND_Y_mirrored'], row['REBOUND_X_abs'], s = (row['SPEED'] - subtract_speed)**power, label= selected_player_name[:3] + ' won the point', c = c_green, alpha = alpha, edgecolors='black', zorder=np.random.randint(11, 13))
            #Serves in lose
            ax.scatter(df_serve_in_lose['REBOUND_Y_mirrored'].values, df_serve_in_lose['REBOUND_X_abs'].values, s = (df_serve_in_lose['SPEED'] - subtract_speed)**power, label= selected_player_name[:3] + ' lost the point', c = c_orange, alpha = alpha, edgecolors='black', zorder=11)        
            #Serves out but not in net
            ax.scatter(df_serve_not_in_net_and_not_in['REBOUND_Y_mirrored'].values, df_serve_not_in_net_and_not_in['REBOUND_X_abs'].values, s = (df_serve_not_in_net_and_not_in['SPEED'] - subtract_speed)**power, label= 'Serve out', c = c_red, alpha = alpha, edgecolors='black', zorder=10)        
            #Serves in net
            ax.scatter(df_serve_in_net['NET_COORD_Y_mirrored'].values, [0]*len(df_serve_in_net), s = (df_serve_in_net['SPEED'] - subtract_speed)**power, label= 'Serve into net', c = c_gray, alpha = 1, edgecolors='black')        
            text_for_serves_in_net = str(len(df_serve_in_net)) + ' serves into net (' + str(int(round(100*len(df_serve_in_net)/len(df_serve), 0))) + '% of serves)'
            ax.text(0, -0.4, text_for_serves_in_net, fontsize=22, ha='center', va='center')
            
            
            #Legend
            if is_serve_deuce_side:
                location = 'upper right'
            else:
                location = 'upper left'
            lgnd = ax.legend(loc=location, fancybox=True, framealpha=0.7, fontsize=18)
            lgnd.legendHandles[0]._sizes = [400]
            lgnd.legendHandles[1]._sizes = [400]
            lgnd.legendHandles[2]._sizes = [400]
            try:
                lgnd.legendHandles[3]._sizes = [400]    
            except:
                pass
            ax.add_artist(lgnd)
            
            #We create second legend for speed
            #We need dummy points with speeds we want to show on the legend
            lower_speed_border = int(min_speed/10)*10
            max_speed = max(df_serve['SPEED'].values)
            upper_speed_border = int(max_speed/10)*10
            dummy_points_for_speed = []
            for i in range(lower_speed_border, upper_speed_border + 11, 20): #+10 so that we get also last value
                dummy_points_for_speed.append(ax.scatter(-100, -100, s = max(1, (i - subtract_speed))**power, label= str(i) + ' km/h', facecolors='none', edgecolors='black', linewidth=2))

            if is_serve_deuce_side:
                ax.legend(handles=dummy_points_for_speed, loc='upper left', bbox_to_anchor=(0.841,0.84), fancybox=True, framealpha=0.7, fontsize=18, labelspacing=0.6)
            else:
                ax.legend(handles=dummy_points_for_speed, loc='upper left', bbox_to_anchor=(0, 0.84), fancybox=True, framealpha=0.7, fontsize=18, labelspacing=0.6)

            
            
            
            #Title
            ax.add_patch(FancyBboxPatch((-3.8, 1.9), 7.6, 0.5, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
            #ax.add_patch(Rectangle((-3.8, 1.9), 7.5, 0.5, linewidth=1, edgecolor='white', facecolor='white', capstyle='round'))
            if is_1st_serve:
                title_text = selected_player_name + ' 1ST SERVE PLACEMENT'
            else:
                title_text = selected_player_name + ' 2ND SERVE PLACEMENT'
            ax.text(3.6, 2.13, title_text, fontsize=22, weight='bold')
            
            ax.text(3.6, 2.33, match_name, fontsize=16, weight='normal')
                
            if is_serve_deuce_side:
                side_text = 'DEUCE COURT'
            else:
                side_text = 'AD COURT'
            ax.text(-2.6, 2.1, side_text, fontsize=16)
            ax.text(-2.6, 2.30, str(len(df_serve)) + ' SERVES', fontsize=16)
            
            
            #Embeded graphs
            if is_serve_deuce_side == False:
                subax3, subax2, subax1 = set_embeded_graphs(ax)
                #subax1, subax2, subax3 = set_embeded_graphs(ax)
            #    temp = df_serve_T_in        
            #    df_serve_T_in = df_serve_W_in
            #    df_serve_W_in = temp
            else:
                subax1, subax2, subax3 = set_embeded_graphs(ax)
                
            
            #White Background squares
            ax.add_patch(FancyBboxPatch((-3.8, 0.15), 2.35, 1.65, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
            ax.add_patch(FancyBboxPatch((-1.2, 0.15), 2.35, 1.65, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
            ax.add_patch(FancyBboxPatch((1.45, 0.15), 2.35, 1.65, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
            
            all_in_serves = len(df_serve_W_in) + len(df_serve_B_in) + len(df_serve_T_in)
            if all_in_serves == 0:
                all_in_serves = np.nextafter(all_in_serves, 1)
                
            #Draw subgraph pies
            subax1.set_title('T Serve Win %', fontsize=18, y=1.2) #which serve it is
            if len(df_serve_T_in_win) > 0  or len(df_serve_T_in_lose) > 0:
                subax1.pie([len(df_serve_T_in_win), len(df_serve_T_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90) #Draw PIE
            else:
                subax1.pie([1, 1], colors = [c_green, c_orange], shadow=True, startangle=90)
            
            if is_serve_deuce_side:
                ax.text(-2.65, 0.55, f'{len(df_serve_W_in)} TOTAL ({int(round(100*len(df_serve_W_in)/all_in_serves, 0))} %)' , fontsize=13, ha='center', va='center') #How many serves in this direction        
                ax.text(-2.2, 0.9, selected_player_name, fontsize=13, ha='right', va='center')  #Print player name
                ax.text(-2.1, 1.1, str(int(round(100*len(df_serve_W_in_win)/np.nextafter(len(df_serve_W_in), 1), 0))) + '%', fontsize=13, ha='right', va='center') #print % of won points
                ax.text(-3.1, 0.9, 'OPPONENT', fontsize=13, ha='left', va='center') #Opponent name
                ax.text(-3.2, 1.1, str(int(round(100*len(df_serve_W_in_lose)/np.nextafter(len(df_serve_W_in), 1), 0))) + '%', fontsize=13, ha='left', va='center') #Print % win for opponent
                ax.text(-2.6, 1.6, 'In perc.: ' + str(int(round(100*len(df_serve_W_in)/np.nextafter(len(df_serve_W), 1), 0))) + ' %', fontsize=17, ha='center', va='center') #In % in this direction
            else:
                ax.text(-2.6, 0.55, f'{len(df_serve_T_in)} TOTAL ({int(round(100*len(df_serve_T_in)/all_in_serves, 0))} %)', fontsize=13, ha='center', va='center') #How many serves in this direction        
                ax.text(-2.2, 0.9, selected_player_name, fontsize=13, ha='right', va='center')  #Print player name
                ax.text(-2.1, 1.1, str(int(round(100*len(df_serve_T_in_win)/np.nextafter(len(df_serve_T_in), 1), 0))) + '%', fontsize=13, ha='right', va='center') #print % of won points
                ax.text(-3.1, 0.9, 'OPPONENT', fontsize=13, ha='left', va='center') #Opponent name
                ax.text(-3.2, 1.1, str(int(round(100*len(df_serve_T_in_lose)/np.nextafter(len(df_serve_T_in), 1), 0))) + '%', fontsize=13, ha='left', va='center') #Print % win for opponent
                ax.text(-2.6, 1.6, 'In perc.: ' + str(int(round(100*len(df_serve_T_in)/np.nextafter(len(df_serve_T), 1), 0))) + ' %', fontsize=17, ha='center', va='center') #In % in this direction
            
            subax2.set_title('B Serve Win %', fontsize=18, y=1.2)
            ax.text(0, 0.55, f'{len(df_serve_B_in)} TOTAL ({int(round(100*len(df_serve_B_in)/all_in_serves, 0))} %)', fontsize=13, ha='center', va='center')
            if len(df_serve_B_in_win) > 0  or len(df_serve_B_in_lose) > 0:
                subax2.pie([len(df_serve_B_in_win), len(df_serve_B_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90)
            else:
                subax2.pie([1, 1], colors = [c_green, c_orange], shadow=True, startangle=90)
            ax.text(0.45, 0.9, selected_player_name, fontsize=13, ha='right', va='center')
            ax.text(0.5, 1.1, str(int(round(100*len(df_serve_B_in_win)/np.nextafter(len(df_serve_B_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
            ax.text(-0.45, 0.9, 'OPPONENT', fontsize=13, ha='left', va='center')
            ax.text(-0.5, 1.1, str(int(round(100*len(df_serve_B_in_lose)/np.nextafter(len(df_serve_B_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
            ax.text(0, 1.6, 'In perc.: ' + str(int(round(100*len(df_serve_B_in)/np.nextafter(len(df_serve_B), 1), 0))) + ' %', fontsize=17, ha='center', va='center') #In % in this direction
            
            subax3.set_title('W Serve Win %', fontsize=18, y=1.2)
            if len(df_serve_W_in_win) > 0  or len(df_serve_W_in_lose) > 0:
                subax3.pie([len(df_serve_W_in_win), len(df_serve_W_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90)
            else:
                subax3.pie([1, 1], colors = [c_green, c_orange], shadow=True, startangle=90)
            if is_serve_deuce_side:
                ax.text(2.6, 0.55, f'{len(df_serve_T_in)} TOTAL ({int(round(100*len(df_serve_T_in)/all_in_serves, 0))} %)', fontsize=13, ha='center', va='center')    
                ax.text(3.05, 0.9, selected_player_name, fontsize=13, ha='right', va='center')
                ax.text(3.15, 1.1, str(int(round(100*len(df_serve_T_in_win)/np.nextafter(len(df_serve_T_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
                ax.text(2.15, 0.9, 'OPPONENT', fontsize=13, ha='left', va='center')
                ax.text(2.1, 1.1, str(int(round(100*len(df_serve_T_in_lose)/np.nextafter(len(df_serve_T_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
                ax.text(2.65, 1.6, 'In perc.: ' + str(int(round(100*len(df_serve_T_in)/np.nextafter(len(df_serve_T),1), 0))) + ' %', fontsize=17, ha='center', va='center') #In % in this direction
            else:
                ax.text(2.65, 0.55, f'{len(df_serve_W_in)} TOTAL ({int(round(100*len(df_serve_W_in)/all_in_serves, 0))} %)', fontsize=13, ha='center', va='center')    
                ax.text(3.05, 0.9, selected_player_name, fontsize=13, ha='right', va='center')
                ax.text(3.15, 1.1, str(int(round(100*len(df_serve_W_in_win)/np.nextafter(len(df_serve_W_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
                ax.text(2.15, 0.9, 'OPPONENT', fontsize=13, ha='left', va='center')
                ax.text(2.1, 1.1, str(int(round(100*len(df_serve_W_in_lose)/np.nextafter(len(df_serve_W_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
                ax.text(2.65, 1.6, 'In perc.: ' + str(int(round(100*len(df_serve_W_in)/np.nextafter(len(df_serve_W), 1), 0))) + ' %', fontsize=17, ha='center', va='center') #In % in this direction
            
            '''
            #Logo and legal
            im = image.imread('../../Razno/GSA Logo.png')
            ax.imshow(im, aspect='auto', extent=(5.35, 6.6, -0.75, 0), zorder=1)
            text_line_1 = 'Confidential and proprietary. Absent permission of GSA, please do not share,'
            text_line_2 = 'disclose, store, copy, distribute, resell, disclose, or use in derivative works.'
            ax.text(3.0, -0.75, text_line_1)
            ax.text(3.0, -0.85, text_line_2)
            '''
            
            #Draw ruler for distance from the sideline
            if is_serve_deuce_side:
                #wide
                ax.text(-3.52, 3.1, "Distance from the line", ha="center", va="center", size=14)
                ax.plot((-3.72,-3.72),(3.5, 6.4), c='black', linewidth=1)
                ax.text(-3.72, 3.3, "40 cm", ha="center", va="center", size=14)
                ax.plot((-3.32,-3.32),(3.5, 6.4), c='black', linewidth=1)
                ax.text(-3.32, 3.3, "80 cm", ha="center", va="center", size=14) 
                #deuce
                ax.text(-0.05, 3.1, "Distance from the line", ha="left", va="center", size=14)
                ax.plot((-0.4, -0.4),(3.5, 6.4), c='black', linewidth=1)
                ax.text(-0.4, 3.3, "40 cm", ha="center", va="center", size=14)
                ax.plot((-0.8, -0.8),(3.5, 6.4), c='black', linewidth=1)
                ax.text(-0.8, 3.3, "80 cm", ha="center", va="center", size=14)
            else:
                #wide
                ax.text(3.52, 3.1, "Distance from the line", ha="center", va="center", size=14)
                ax.plot((3.72,3.72),(3.5, 6.4), c='black', linewidth=1)
                ax.text(3.72, 3.3, "40 cm", ha="center", va="center", size=14)
                ax.plot((3.32,3.32),(3.5, 6.4), c='black', linewidth=1)
                ax.text(3.32, 3.3, "80 cm", ha="center", va="center", size=14)
                #deuce
                ax.text(0.05, 3.1, "Distance from the line", ha="right", va="center", size=14)
                ax.plot((0.4, 0.4),(3.5, 6.4), c='black', linewidth=1)
                ax.text(0.4, 3.3, "40 cm", ha="center", va="center", size=14)
                ax.plot((0.8, 0.8),(3.5, 6.4), c='black', linewidth=1)
                ax.text(0.8, 3.3, "80 cm", ha="center", va="center", size=14)
            
            #Draw boxes for bounces
            box_width = 1.377
            box_y_start = 5.4
            if is_serve_deuce_side:
                box_x_start= -4.12
            else:
                box_x_start= -0.01
            ax.add_patch(Rectangle((box_x_start, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False, zorder=-1))    
            ax.add_patch(Rectangle((box_x_start + box_width, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False))
            ax.add_patch(Rectangle((box_x_start + box_width*2, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False))
            box_y_start = 4.4
            ax.add_patch(Rectangle((box_x_start, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False))
            ax.add_patch(Rectangle((box_x_start + box_width, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False))
            ax.add_patch(Rectangle((box_x_start + box_width*2, box_y_start), box_width, 1, linewidth=1, edgecolor='black', fill=False))
            
            #Values for box
            #boxes are numbered like that (same deuce and ad)
            #b1 b2 b3
            #b4 b5 b6
            #b7 - all shorter serves
            #Slightly different number, to be consistent with W B T marks, because due to outer line edges the service box is larger
            box_width = 1.391
            box_y_start = 5.4
            if is_serve_deuce_side:
                x_start = -4.15
            else:
                x_start = -0.05 #some buffer
            df_serve_in_b1 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] < (x_start+box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start))]
            df_serve_in_b2 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] >= (x_start+box_width)) & (df_serve_in['REBOUND_Y_mirrored'] < (x_start+ 2*box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start))]
            df_serve_in_b3 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] >= (x_start+ 2*box_width)) & (df_serve_in['REBOUND_Y_mirrored'] < (x_start+ 3*box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start))]
            #2nd row
            df_serve_in_b4 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] < (x_start+box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_serve_in['REBOUND_X_abs'] < (box_y_start))]
            df_serve_in_b5 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] >= (x_start+box_width)) & (df_serve_in['REBOUND_Y_mirrored'] < (x_start+ 2*box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_serve_in['REBOUND_X_abs'] < (box_y_start))]
            df_serve_in_b6 = df_serve_in[(df_serve_in['REBOUND_Y_mirrored'] >= (x_start+ 2*box_width)) & (df_serve_in['REBOUND_Y_mirrored'] < (x_start+ 3*box_width)) & (df_serve_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_serve_in['REBOUND_X_abs'] < (box_y_start))]
            #3rd row
            df_serve_in_b7 = df_serve_in[df_serve_in['REBOUND_X_abs'] < (box_y_start-1)]
            
            #Print numbers for serves in for each box
            box_y_starts = [5.9, 4.9]
            box_x_starts = [box_x_start + box_width/2, box_x_start + (3*box_width/2), box_x_start + (5*box_width/2)] #box_x_start + box_width/2
            box_dfs = [df_serve_in_b1, df_serve_in_b2, df_serve_in_b3, df_serve_in_b4, df_serve_in_b5, df_serve_in_b6]
            for y_start in box_y_starts:
                for x_start in box_x_starts:
                    df_cur = box_dfs.pop(0) #removes element
                    ax.text(x_start,y_start, str(int(round(100*len(df_cur)/np.nextafter(len(df_serve_in), 1), 0))) + '%', fontsize=20, ha='center', va='center', color='black', zorder=100) #b1
            #3rd row - all shorter serves
            ax.text(box_x_starts[1], 3.9, str(int(round(100*len(df_serve_in_b7)/np.nextafter(len(df_serve_in), 1), 0))) + '%', fontsize=20, ha='center', va='center', color='black', zorder=100) #b7
            #ax.text(box_x_start + box_width/2,box_y_start + 0.5, str(int(round(100*len(df_serve_in_b1)/len(df_serve_in), 0))) + '%', fontsize=20, ha='center', va='center', color='black') #, bbox=dict(facecolor='white', pad=0.2, boxstyle='round'))
            
            #Arrow for distance from servis line
            if is_serve_deuce_side:
                ax.text(-6, 6.4, "0 m", ha="center", va="center", size=14, bbox=dict(boxstyle="larrow", fc="white", alpha=0.5, lw=1))
                ax.text(-6, 5.4, "1 m", ha="center", va="center", size=14, bbox=dict(boxstyle="larrow", fc="white", alpha=0.5, lw=1))
                ax.text(-6, 4.4, "2 m", ha="center", va="center", size=14, bbox=dict(boxstyle="larrow", fc="white", alpha=0.5, lw=1))
            else:
                ax.text(6, 6.4, "0 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))
                ax.text(6, 5.4, "1 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))
                ax.text(6, 4.4, "2 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))

            #plt.gca().invert_yaxis()
            #plt.gca().invert_xaxis()
            ax.set_ylim(ax.get_ylim()[::-1])
            ax.set_xlim(ax.get_xlim()[::-1])
            fig.set_tight_layout(True)
            return fig



        # In[48]:


        df = df1
        df_player_serves = df[((df['PLAYER_HIT'] == player1)  & (df['is_shot_serve'] == 1))]
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(19.5, 14.5))
        draw_serve_points(df_player_serves, ax, title1, is_1st_serve=True, is_serve_deuce_side=True, selected_player_name=player1).savefig(f'{basa_poc}/p41.png')
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(19.5, 14.5))
        draw_serve_points(df_player_serves, ax, title1, is_1st_serve=True, is_serve_deuce_side=False, selected_player_name=player1).savefig(f'{basa_poc}/p51.png')


        df = df2
        df_player_serves = df[((df['PLAYER_HIT'] == player2)  & (df['is_shot_serve'] == 1))]
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(19.5, 14.5))
        draw_serve_points(df_player_serves, ax, title2, is_1st_serve=True, is_serve_deuce_side=True, selected_player_name=player2).savefig(f'{basa_poc}/p42.png')
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(19.5, 14.5))
        draw_serve_points(df_player_serves, ax, title2, is_1st_serve=True, is_serve_deuce_side=False, selected_player_name=player2).savefig(f'{basa_poc}/p52.png')

        from docxtpl import DocxTemplate
        from docxtpl import InlineImage, RichText
        from docx.shared import Mm

        #new_slice_values = list(new_slice.values())
        doc = DocxTemplate("BASAVAREDDY TEMPLATE.docx")
        dirx = f'{basa_poc}/'

        context = { 
            'title1': title1,
            'title2': title2,
            'player': player1,
            
            
                }

        #'p11': dirx + 'p11.png'
        #   'p11': dirx + 'p12.png'

        doc.replace_pic("p11", dirx+'p11.png')
        doc.replace_pic("p12", dirx+'p12.png')

        doc.replace_pic("p_21", dirx+'p_21.png')
        doc.replace_pic("p_22", dirx+'p_22.png')

        doc.replace_pic("p21", dirx+'p21.png')
        doc.replace_pic("p22", dirx+'p22.png')
        doc.replace_pic("p61", dirx+'p61.png')
        doc.replace_pic("p62", dirx+'p62.png')
        doc.replace_pic("p31", dirx+'p31.png')
        doc.replace_pic("p32", dirx+'p32.png')
        doc.replace_pic("p41", dirx+'p41.png')
        doc.replace_pic("p42", dirx+'p42.png')

        doc.replace_pic("p51", dirx+'p51.png')
        doc.replace_pic("p52", dirx+'p52.png')

        doc.replace_pic("p71", dirx+'p71.png')
        doc.replace_pic("p72", dirx+'p72.png')

        doc.replace_pic("p81", dirx+'p81.png')
        doc.replace_pic("p82", dirx+'p82.png')

        doc.replace_pic("p91", dirx+'p91.png')
        doc.replace_pic("p92", dirx+'p92.png')

        doc.replace_pic("p121", dirx+'p121.png')
        doc.replace_pic("p122", dirx+'p122.png')

        doc.render(context)
        filename = f"{title1} V {title2}---{report_id}.docx"
        doc.save(filename)
        from glob import glob
        images = glob(basa_poc + '/*.png')
        for image in images:
            os.remove(image)
        #azure_upload_docx(container_client, filename)
        return True
    except:
        return False

        
