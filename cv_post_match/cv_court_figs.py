"""Verbatim matplotlib visual builders from post_match_data.ipynb."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

# notebook cell-scope globals the plot functions rely on (hard court for all CV)
surface = 'hard'
surfaces = ['hard']
court_color_x = '#1F78B4'
out_of_court_color_x = '#78C0E8'
selected_player_name = None
selected_player_initials = ''
display = lambda *a, **k: None
class SurfaceCode:  # minimal stand-in; CV renders hard for all
    HARD = 2
    CLAY = 8
    GRASS = 4
surfacecode = SurfaceCode.HARD
Markdown = lambda *a, **k: None

def plot_contact_points_percentages(df_shots1, titlic, win_lose = False, show_winners = False, court_draw_width_start=-8, court_draw_width_end=8, title1 = '', title2='', main_title = ''):
    c_yellow = '#dfff4f'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
    set_half_court_contact(ax, court_draw_width_start=court_draw_width_start, court_draw_width_end=court_draw_width_end)
    
    #fig.suptitle(main_title)
    ax.set_title(titlic)
    
    #Set legend
    yellow_patch = mpatches.Patch(color=c_yellow, label='Contact point')
    
    #Set parameters for lines
    y_position_2m = 13.88
    y_position_0m = 11.88
    text_distance_x = -7
    text_move_y = 0
    text_move_for_perc_y = 0.85
    x_start = -7.5
    line_color = 'black'
    text_color = 'white'
    linewidth = 1
    text_size = 20
    text_size_perc = 44
    shots_all = df_shots1
    
    #ax.legend(handles=[yellow_patch], loc='best')

    #Plot lines
    ax.plot([x_start, -x_start], [y_position_2m, y_position_2m], linewidth=linewidth, linestyle="--", c=line_color)    
    ax.text(text_distance_x, y_position_2m + text_move_y, "-2 m", ha="center", va="center", size=text_size, c=text_color)
    ax.plot([x_start, -x_start], [y_position_0m, y_position_0m], linewidth=linewidth, linestyle="--", c=line_color)    
    ax.text(text_distance_x, y_position_0m + text_move_y, "", ha="center", va="center", size=text_size, c=text_color)

    #Plot percentages
    no_of_shots_2m_plus = len(shots_all[shots_all['CONTACT_X_abs'] >= y_position_2m])
    no_of_shots_0m_2m = len(shots_all[(shots_all['CONTACT_X_abs'] >= y_position_0m) & (shots_all['CONTACT_X_abs'] < y_position_2m)])
    no_of_shots_0m_minus = len(shots_all[shots_all['CONTACT_X_abs'] < y_position_0m])
    all_shots = no_of_shots_2m_plus + no_of_shots_0m_2m + no_of_shots_0m_minus
    if all_shots > 0:
        shots_2m_plus_perc = int(round(100*no_of_shots_2m_plus/all_shots, 0))
        shots_0m_2m_perc = int(round(100*no_of_shots_0m_2m/all_shots, 0))
        shots_0m_minus_perc = int(round(100*no_of_shots_0m_minus/all_shots, 0))
    else:
        shots_2m_plus_perc = 0
        shots_0m_2m_perc = 0
        shots_0m_minus_perc = 0

    ax.text(0, y_position_2m + text_move_for_perc_y, f'{shots_2m_plus_perc} %', ha="center", va="center", size=text_size_perc, c=line_color)
    ax.text(0, y_position_0m + text_move_for_perc_y, f'{shots_0m_2m_perc} %', ha="center", va="center", size=text_size_perc, c=line_color)
    ax.text(0, y_position_0m - 1.3, f'{shots_0m_minus_perc} %', ha="center", va="center", size=text_size_perc, c=line_color)
    
    c = sns.kdeplot(x=df_shots1['CONTACT_Y_mirrored'].to_list(), y=df_shots1['CONTACT_X_abs'].to_list(), levels=100, cmap="turbo", fill=True)
    #plt.show()
    return fig
    #Plot contact points
    #for _, row in shots_all.iterrows():
    #    ax.scatter(row['CONTACT_Y_mirrored'], row['CONTACT_X_abs'], color=c_yellow)

def visualize_return_direction(df, match_ids_selected, serve, side, directions, one_report_for_all_matches = False, folder_name=None, for_opponents = False):
    #Set where to set reports
    
    
    df = df[df['match_id'].isin(match_ids_selected)]
    
    #We are only interested in returns after a good serve
    if for_opponents:
        df_player_returns = df[((df['PLAYER_HIT'] != selected_player_name)&(df['shot_no'] == 2)&(df['is_shot_in'].shift(1) == 1)&(df['is_shot_serve'].shift(1) == 1))]
    else:
        df_player_returns = df[((df['PLAYER_HIT'] == selected_player_name)&(df['shot_no'] == 2)&(df['is_shot_in'].shift(1) == 1)&(df['is_shot_serve'].shift(1) == 1))]
    
    if one_report_for_all_matches:
        match_ids_selected = match_ids_selected[0:1] #to do the following loop only once
        
    for match_id in match_ids_selected:
        
        #df_player_returns = df[((df['PLAYER_HIT'] == selected_player_name) & (df['match_id'] == match_id) & (df['shot_no'] == 2))] 
        df_player_returns = df_player_returns[df_player_returns['match_id'] == match_id]
        match_name = get_match_name_from_match_id(match_id)
        
        
        
        figure_height = 15
        figure_width = 12
        if side == 'all_sides':
            directions_temp = directions[0:1]
        else:
            directions_temp = directions
        print(directions_temp, 'dirtemp')
        for direction in directions_temp:
            #pass
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figure_width, figure_height))  #constrained_layout=False
            draw_return_direction(df_player_returns, ax, match_name, serve_no = serve, side = side, direction = direction, for_opponents=for_opponents)
        return fig
        '''
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figure_width, figure_height))  #constrained_layout=False
        draw_return_points(df_player_returns, ax, match_name, is_1st_serve = True, is_serve_deuce_side = True, direction = 'T')        
        fig.savefig(folder_main + 'Return reports visuals/' + folder_selected + '/' + match_name + '-1st_serve_DEUCE.png', dpi=300, bbox_inches='tight', pad_inches=0)
        '''
    #plt.subplots_adjust(wspace=0.1, hspace=0)

def draw_return_direction(df_player_returns, ax, match_name, serve_no, side, direction, for_opponents=False):    
    c_green = '#A3FF74' #'#89E381'
    c_orange = '#FF7F00' #'#D27E24'
    c_red = '#E61A25' #'#C61A25' #'#BB2D3B'
    c_gray = '#7C8F9F'
    arrowstyle = '-|>'
    
    df_return = df_player_returns.copy()
    if serve_no != 'both_serves':
        if serve_no == '1st_serve':
            df_return = df_player_returns[df_player_returns['serve_number']==1]
        else:
            df_return = df_player_returns[df_player_returns['serve_number']==2]
        
    if side != 'all_sides':
        df_return = df_return[df_return['serve_deuce_or_ad'] == side]

    if direction != 'all_directions':
        df_return = df_return[df_return['serve_direction'] == direction]

    
    #Remove noise
    #Remove bounces on the same side
    df_return = df_return[~(df_return['CONTACT_X'] * df_return['REBOUND_X'] >0)]
    #Limit max speed
    #df_return = df_return[df_return['SPEED']<160]
    df_return['SPEED'] = np.where(df_return['SPEED']>150, 150, df_return['SPEED'])
    
    #Limit min speed
    df_return['SPEED'] = np.where(((df_return['SPEED']>1)&(df_return['SPEED']<=40)), 41, df_return['SPEED'])
    
    df_return_in = df_return[df_return['is_shot_in'] == 1]
    df_return_not_in = df_return[df_return['is_shot_in'] == 0]
    df_return_in_net = df_return[df_return['is_in_the_net'] == 1]
    df_return_in_win = df_return_in[df_return_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_in_lose = df_return_in[df_return_in['PLAYER_WIN_NAME'] != selected_player_name]

    #bounce left, middle, right
    left_third_y_border = -1.37
    right_third_y_border = 1.37
    
    df_return_leftside_in = df_return_in[df_return_in['REBOUND_Y_mirrored'] < left_third_y_border]
    df_return_middle_in = df_return_in[(df_return_in['REBOUND_Y_mirrored'] >= left_third_y_border) & (df_return_in['REBOUND_Y_mirrored'] <= right_third_y_border)]
    df_return_rightside_in = df_return_in[df_return_in['REBOUND_Y_mirrored'] > right_third_y_border]

    df_return_leftside_in_win = df_return_leftside_in[df_return_leftside_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_leftside_in_lose = df_return_leftside_in[df_return_leftside_in['PLAYER_WIN_NAME'] != selected_player_name]
    df_return_middle_in_win = df_return_middle_in[df_return_middle_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_middle_in_lose = df_return_middle_in[df_return_middle_in['PLAYER_WIN_NAME'] != selected_player_name]
    df_return_rightside_in_win = df_return_rightside_in[df_return_rightside_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_rightside_in_lose = df_return_rightside_in[df_return_rightside_in['PLAYER_WIN_NAME'] != selected_player_name]       

    #Draw court
    set_half_court(ax)

    #Title
    ax.add_patch(FancyBboxPatch((-5.9, -1.9), 11.8, 1.1, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))

    if for_opponents:
        title_text = 'OPPONENTS ' + serve_no.replace('_', ' ').upper() + ' RETURN PLACEMENT'  
    else:
        title_text = selected_player_name + ' ' + serve_no.replace('_', ' ').upper() + ' RETURN PLACEMENT'    
    
    ax.text(-5.7, -1.35, title_text, fontsize=22, weight='bold')
    ax.text(-5.7, -1.7, match_name, fontsize=16, weight='normal')
        
    if side == 'all_sides':
        side_text = 'BOTH SIDES'
    else:
        side_text = side.upper() 
    if direction == 'all_directions':
        side_text = side_text + ' ALL DIRECTIONS'
    else:
        side_text = side_text + ' ' + direction.upper()
    side_text = side_text + ' SERVE'
    
    ax.text(5.6, -1.2, side_text, fontsize=16, ha='right')
    ax.text(5.6, -1.7, str(len(df_return)) + ' RETURNS - ' + str(len(df_return_in)) + ' IN (' + str(int(round(100*len(df_return_in)/np.nextafter(len(df_return), 1),0))) + ' %)', fontsize=16, ha='right')
    
    #If no points finish here
    if len(df_return) == 0:
        ax.add_patch(FancyBboxPatch((-2.5, 1.9), 5, 1.1, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
        ax.text(-1, 2.3, 'NO SUCH SERVES', fontsize=22, weight='bold')
        return
    
    #Draw points
    #Set params
    #print(len(df_return))
    #min_speed = min(df_return[~np.isnan(df_return['REBOUND_X_abs'])]['SPEED'].values, default=0)
    #max_speed = max(df_return[~np.isnan(df_return['REBOUND_X_abs'])]['SPEED'].values, default=200)
    min_speed = min(df_return['SPEED'].values, default=0)
    max_speed = max(df_return['SPEED'].values, default=200)#print(min_speed)
    #print(max_speed)
    alpha = 0.7
    power = 1 #1.1 #1.15   
    lower_speed_border = int(min_speed/10)*10
    max_speed = max(df_return['SPEED'].values)
    upper_speed_border = int(max_speed/10)*10
    min_size_px = 5
    def add_arrows(ax, df, color):
        for i, row in df.iterrows():
            #ax.scatter(row['next_next_CONTACT_Y_mirrored'], row['next_next_CONTACT_X_abs'], color=c_green)
            #ax.scatter(row['CONTACT_Y_mirrored'], row['CONTACT_X_abs'], color=c_green)
            x = [-1*row['CONTACT_Y_mirrored'], row['REBOUND_Y_mirrored']]
            y = [-1*row['CONTACT_X_abs'], row['REBOUND_X_abs']]
            arrowstyle = '-|>'
            ax.annotate(s='', xytext = (x[0], y[0]), xy = (x[1], y[1]), arrowprops=dict(arrowstyle=arrowstyle, color=color, lw=1, ls='-'), alpha=0.5)
    
    def add_arrows(ax, df, color):
        def calculate_line_trajectory(x, y, c):
            x1, y1 = (x[0], y[0])
            x2, y2 = (x[1], y[1])
            m = (y1-y2)/(x1-x2)
            b = (x1*y2 - x2*y1)/(x1-x2)
            return m*c + b
        for i, row in df.iterrows():
            y_tr = calculate_line_trajectory([-1*row['CONTACT_X_abs'], row['REBOUND_X_abs']], [-1*row['CONTACT_Y_mirrored'], row['REBOUND_Y_mirrored']], 0)
            ax.plot([y_tr, row['REBOUND_Y_mirrored']], [0, row['REBOUND_X_abs']], c=color, lw=2)

    
    #Returns in win
    ax.scatter(df_return_in_win['REBOUND_Y_mirrored'].values, df_return_in_win['REBOUND_X_abs'].values, s = (df_return_in_win['SPEED'] - lower_speed_border + min_size_px)**power, label= selected_player_initials + ' won the point', c = c_green, alpha = alpha, edgecolors='black', zorder=11)        
    add_arrows(ax, df_return_in_win, c_green)
    #Returns in lose
    ax.scatter(df_return_in_lose['REBOUND_Y_mirrored'].values, df_return_in_lose['REBOUND_X_abs'].values, s = (df_return_in_lose['SPEED'] - lower_speed_border + min_size_px)**power, label= selected_player_initials + ' lost the point', c = c_orange, alpha = alpha, edgecolors='black', zorder=12)        
    add_arrows(ax, df_return_in_lose, c_orange)
    #Returns out
    ax.scatter(df_return_not_in['REBOUND_Y_mirrored'].values, df_return_not_in['REBOUND_X_abs'].values, s = (df_return_not_in['SPEED'] - lower_speed_border + min_size_px)**power, label= 'Return out', c = c_red, alpha = alpha, edgecolors='black', zorder=10)        
    add_arrows(ax, df_return_not_in, c_red)
    #Returns in net
    ax.scatter(df_return_in_net['NET_COORD_Y'].values, [0]*len(df_return_in_net), s = (df_return_in_net['SPEED'] - lower_speed_border + min_size_px)**power, label= 'Return into net', c = c_gray, alpha = 1, edgecolors='black')        
    
    #In the net
    text_for_returns_in_net = str(len(df_return_in_net)) + ' returns into net (' + str(int(round(100*len(df_return_in_net)/len(df_return), 0))) + '% of returns)'
    ax.text(0, 0.5, text_for_returns_in_net, fontsize=22, ha='center', va='center')
    
    
    #Legend
    #if is_serve_deuce_side:
    #    location = 'upper right'
    #else:
    #    location = 'upper left'
    lgnd = ax.legend(loc='upper right', fancybox=True, framealpha=0.7, fontsize=18, bbox_to_anchor=(0.265,0.46))
    lgnd.legend_handles[0]._sizes = [400]
    lgnd.legend_handles[1]._sizes = [400]
    lgnd.legend_handles[2]._sizes = [400]
    lgnd.legend_handles[3]._sizes = [400]    
    ax.add_artist(lgnd)
    
    #legend for speed
    #We need dummy points with speeds we want to show on the legend
    dummy_points_for_speed = []
    for i in range(lower_speed_border, upper_speed_border + 11, 20): #+10 so that we get also last value
        dummy_points_for_speed.append(ax.scatter(-100, -100, s = (i - lower_speed_border + min_size_px)**power, label= str(i) + ' km/h', facecolors='none', edgecolors='black', linewidth=2))

    ax.legend(handles=dummy_points_for_speed, loc='lower right', bbox_to_anchor=(0.995,0.30), fancybox=True, framealpha=0.7, fontsize=18, labelspacing=0.6)

    
    #Subaxeses
    box_y_start = -5.5
    box_width = 3.7
    box_height = 3.3
    #White Background squares
    ax.add_patch(FancyBboxPatch((-6.0, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    ax.add_patch(FancyBboxPatch((-1.95, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    ax.add_patch(FancyBboxPatch((2.00, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    
    #Create subaxes
    subax1, subax2, subax3 = set_embeded_graphs(ax, 0.03)
    
    #Draw subgraph pies    
    box_y_start = 1.2  
    total_y_start = -3.1
    player_name_y = -3.7
    player_perc_y = -4.2
    
    subax1.set_title('Deuce-side Return Win %', fontsize=18, y=box_y_start) #which serve it is
    ax.text(-4.0, total_y_start, str(len(df_return_leftside_in)) + ' TOTAL (' + str(int(round(100*len(df_return_leftside_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center') #How many serves in this direction
    subax1.pie([len(df_return_leftside_in_win), len(df_return_leftside_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90) #Draw PIE
    ax.text(-4.7, player_name_y, selected_player_name, fontsize=13, ha='right', va='center')  #Print player name
    ax.text(-4.9, player_perc_y, str(int(round(100*len(df_return_leftside_in_win)/np.nextafter(len(df_return_leftside_in), 1), 0))) + '%', fontsize=13, ha='right', va='center') #print % of won points
    ax.text(-3.4, player_name_y, 'OPPONENT', fontsize=13, ha='left', va='center') #Opponent name
    ax.text(-3.1, player_perc_y, str(int(round(100*len(df_return_leftside_in_lose)/np.nextafter(len(df_return_leftside_in), 1), 0))) + '%', fontsize=13, ha='left', va='center') #Print % win for opponent
    
    subax2.set_title('Middle Return Win %', fontsize=18, y=box_y_start)
    ax.text(0, total_y_start, str(len(df_return_middle_in)) + ' TOTAL (' + str(int(round(100*len(df_return_middle_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center')
    subax2.pie([len(df_return_middle_in_win), len(df_return_middle_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90)
    ax.text(-0.7, player_name_y, selected_player_name, fontsize=13, ha='right', va='center')
    ax.text(-1.0, player_perc_y, str(int(round(100*len(df_return_middle_in_win)/np.nextafter(len(df_return_middle_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
    ax.text(0.8, player_name_y, 'OPPONENT', fontsize=13, ha='left', va='center')
    ax.text(1.0, player_perc_y, str(int(round(100*len(df_return_middle_in_lose)/np.nextafter(len(df_return_middle_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
    
    subax3.set_title('Ad-side Return Win %', fontsize=18, y=box_y_start)
    ax.text(4.1, total_y_start, str(len(df_return_rightside_in)) + ' TOTAL (' + str(int(round(100*len(df_return_rightside_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center')
    subax3.pie([len(df_return_rightside_in_win), len(df_return_rightside_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90)
    ax.text(3.30, player_name_y, selected_player_name, fontsize=13, ha='right', va='center')
    ax.text(3.05, player_perc_y, str(int(round(100*len(df_return_rightside_in_win)/np.nextafter(len(df_return_rightside_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
    ax.text(4.75, player_name_y, 'OPPONENT', fontsize=13, ha='left', va='center')
    ax.text(4.95, player_perc_y, str(int(round(100*len(df_return_rightside_in_lose)/np.nextafter(len(df_return_rightside_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
    
    
    #Logo and legal
    '''
    im = image.imread('../../Razno/GSA Logo.png')
    ax.imshow(im, aspect='auto', extent=(5.35, 6.6, -0.75, 0), zorder=1)
    text_line_1 = 'Confidential and proprietary. Absent permission of GSA, please do not share,'
    text_line_2 = 'disclose, store, copy, distribute, resell, disclose, or use in derivative works.'
    ax.text(3.0, -0.75, text_line_1)
    ax.text(3.0, -0.85, text_line_2)
    '''
    '''
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
    df_return_in_b1 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] < (x_start+box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start))]
    df_return_in_b2 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] >= (x_start+box_width)) & (df_return_in['REBOUND_Y_mirrored'] < (x_start+ 2*box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start))]
    df_return_in_b3 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] >= (x_start+ 2*box_width)) & (df_return_in['REBOUND_Y_mirrored'] < (x_start+ 3*box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start))]
    #2nd row
    df_return_in_b4 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] < (x_start+box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_return_in['REBOUND_X_abs'] < (box_y_start))]
    df_return_in_b5 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] >= (x_start+box_width)) & (df_return_in['REBOUND_Y_mirrored'] < (x_start+ 2*box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_return_in['REBOUND_X_abs'] < (box_y_start))]
    df_return_in_b6 = df_return_in[(df_return_in['REBOUND_Y_mirrored'] >= (x_start+ 2*box_width)) & (df_return_in['REBOUND_Y_mirrored'] < (x_start+ 3*box_width)) & (df_return_in['REBOUND_X_abs'] >= (box_y_start - 1)) & (df_return_in['REBOUND_X_abs'] < (box_y_start))]
    #3rd row
    df_return_in_b7 = df_return_in[df_return_in['REBOUND_X_abs'] < (box_y_start-1)]
    
    #Print numbers for serves in for each box
    box_y_starts = [5.9, 4.9]
    box_x_starts = [box_x_start + box_width/2, box_x_start + (3*box_width/2), box_x_start + (5*box_width/2)] #box_x_start + box_width/2
    box_dfs = [df_return_in_b1, df_return_in_b2, df_return_in_b3, df_return_in_b4, df_return_in_b5, df_return_in_b6]
    for y_start in box_y_starts:
        for x_start in box_x_starts:
            df_cur = box_dfs.pop(0) #removes element
            ax.text(x_start,y_start, str(int(round(100*len(df_cur)/len(df_return_in), 0))) + '%', fontsize=20, ha='center', va='center', color='black', zorder=100) #b1
    #3rd row - all shorter serves
    ax.text(box_x_starts[1], 3.9, str(int(round(100*len(df_return_in_b7)/len(df_return_in), 0))) + '%', fontsize=20, ha='center', va='center', color='black', zorder=100) #b7
    #ax.text(box_x_start + box_width/2,box_y_start + 0.5, str(int(round(100*len(df_return_in_b1)/len(df_return_in), 0))) + '%', fontsize=20, ha='center', va='center', color='black') #, bbox=dict(facecolor='white', pad=0.2, boxstyle='round'))
    '''
    
    #Arrow for distance from servis line
    #ax.text(-6, 11.88, "0 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))
    #ax.text(-5, 10.88, "0-2 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))
    #ax.text(-5, 9.88, "2 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))    
    #ax.text(-5, 8.88, "2-4 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))    
    #ax.text(-5, 7.88, "4 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))  
    #ax.text(-5, 6.88, "4-6 m", ha="center", va="center", size=14, bbox=dict(boxstyle="rarrow", fc="white", alpha=0.5, lw=1))  
    
    court_width_doubles = 8.23 + 1.37 + 1.37
    court_width = 8.23
    linewidth = 1
    #ax.plot([-1*court_width/2, court_width/2], [9.88, 9.88], linewidth=linewidth, linestyle="-", c='black')    
    #ax.plot([-1*court_width/2, court_width/2], [7.88, 7.88], linewidth=linewidth, linestyle="-", c='black')
    #ax.plot([-1*court_width/2, court_width/2], [5.88, 5.88], linewidth=linewidth, linestyle="-", c='black')
    
    #ax.plot([-1*court_width/2, court_width/2], [9.18, 9.18], linewidth=linewidth, linestyle="-", c='black')
    
    #Vertical lines to separate court to 3 parts
    court_length = 11.88
    one_third_width = 2.74
    ax.plot([-1*court_width/2 + one_third_width, -1*court_width/2 + one_third_width], [0, court_length], linewidth=2, linestyle="-", c='black')
    ax.plot([-1*court_width/2 + one_third_width + one_third_width, -1*court_width/2 + one_third_width + one_third_width], [0, court_length], linewidth=2, linestyle="-", c='black')

def set_half_court(ax):
    court_draw_width_start = -7.5
    court_draw_width_end = 7.5
    court_draw_height_end = 15
    court_draw_height_start = -6
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
    #ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-1*court_length, 6.40], linewidth=linewidth, linestyle="-", c=line_color) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    #Net post
    #ax.add_artist(Circle((net_post_x_left, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_artist(Circle((net_post_x_right, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_patch(Rectangle((net_post_x_left - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    #ax.add_patch(Rectangle((net_post_x_right - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    
    #Court color
    if surfacecode == SurfaceCode.CLAY:
        ax.set_facecolor('#d45e3e')# -> clay court
    elif surfacecode == SurfaceCode.HARD:
        ax.set_facecolor('#1F78B4')# -> hard court
    elif surfacecode == SurfaceCode.GRASS:
        ax.set_facecolor('#83a462')# -> grass court
    #Out of court color
    
    light_grass = '#83a462'
    dark_grass = '#739655'
    # Number of stripes and their height
    
    if surfacecode == SurfaceCode.GRASS:
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
        #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#83a462')
        #ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#78C0E8')
        if surfacecode == SurfaceCode.CLAY:
            ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#d45e3e')
            ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#d45e3e')
            ax.axhspan(court_length, court_draw_height_end, alpha=1, color='#d45e3e') #behind baseline
        elif surfacecode == SurfaceCode.HARD:
            
            ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=1, color='#78C0E8')
            ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=1, color='#78C0E8')
            ax.axhspan(court_length, court_draw_height_end, alpha=1, color='#78C0E8') #behind baseline
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
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

def get_match_name_from_match_id(match_id):
    match_id_splited = match_id.split('_')
    tourney_name = match_id_splited[0]
    tourney_year = match_id_splited[1]
    opponent_name = match_id_splited[-1]
    #print(str(selected_player_name.split('.')[-1].upper()))
    if selected_player_name.split('.')[-1].upper() in opponent_name.upper():
        if len(match_id_splited[-2].upper()) == 2 and '.' in match_id_splited[-2].upper():
            opponent_name = match_id_splited[-3]
        else:
            opponent_name = match_id_splited[-2]
    match_name = tourney_name + '' + tourney_year + ' vs. ' + opponent_name.capitalize()
    #match_name = match_name.replace(' ', '_')
    match_name = match_name.replace('MS003', '2019')
    match_name = match_name.replace('MS015', '2019')
    return match_name

def set_half_court2(ax):
    
    img = plt.imread("alex_new_half_court.png")
    print(img.shape)
    #img = img[0:980, int(4*(921/17)):int(921-4*(921/17))]
    img = img[272:980, 217:704]
    #img = img[0:980,]
    court_draw_width_start = -4.5
    court_draw_width_end = 4.5
    court_draw_height_end = 12
    court_draw_height_start = -1

    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    

    ax.imshow(img, extent=[court_draw_width_start, court_draw_width_end, court_draw_height_start, court_draw_height_end])
    #plt.yticks(np.arange(court_draw_height_start, court_draw_height_end, 0.50))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.invert_xaxis()
    ax.invert_yaxis()
    
    
def set_full_court(ax):
    
    img = plt.imread("new_full_court.png")
    court_draw_width_start = -8.5
    court_draw_width_end = 8.5
    court_draw_height_end = 17
    court_draw_height_start = -17

    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    

    ax.imshow(img, extent=[court_draw_width_start, court_draw_width_end, court_draw_height_start, court_draw_height_end])
    #plt.yticks(np.arange(court_draw_height_start, court_draw_height_end, 0.50))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def plot_serve_placement(shots_all, fig_width=10, fig_height=10, main_title = 'Serve placement'):
    c_green = '#A3FF74'
    c_red = '#E61A25'
    #c_red = c_green
    arrowstyle = '-|>'
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(fig_width, fig_height))
    set_half_court(ax)
    
    
    #Set titles
    #fig.suptitle(main_title)
    
    #Set legend
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color=c_red, label='Point lost')
    green_patch = mpatches.Patch(color=c_green, label='Point won')
            
    shots_all_won = shots_all[shots_all.server_name == shots_all.PLAYER_WIN_NAME]
    shots_all_lost = shots_all[shots_all.server_name != shots_all.PLAYER_WIN_NAME]
    for i, row in shots_all_won.iterrows():
        ax.scatter(row['REBOUND_Y_mirrored'], row['REBOUND_X_abs'], color=c_green)
    for i, row in shots_all_lost.iterrows():
        ax.scatter(row['REBOUND_Y_mirrored'], row['REBOUND_X_abs'], color=c_red)
    
    red_patch = mpatches.Patch(color=c_red, label='Point lost')
    green_patch = mpatches.Patch(color=c_green, label='Point won')
    ax.legend(handles=[green_patch, red_patch], loc='upper center')
    return ax, fig

def visualize_return_depth(df, match_ids_selected, serve, side, directions, one_report_for_all_matches = False, folder_name=None, for_opponents = False):
    #Set where to set reports

            
    
    
    df = df[df['match_id'].isin(match_ids_selected)]
    
    #We are only interested in returns after a good serve    
    if for_opponents:
        df_player_returns = df[((df['PLAYER_HIT'] != selected_player_name)&(df['shot_no'] == 2)&(df['is_shot_in'].shift(1) == 1)&(df['is_shot_serve'].shift(1) == 1))]
    else:
        df_player_returns = df[((df['PLAYER_HIT'] == selected_player_name)&(df['shot_no'] == 2)&(df['is_shot_in'].shift(1) == 1)&(df['is_shot_serve'].shift(1) == 1))]
    
    print(df_player_returns.shape)
    if one_report_for_all_matches:
        match_ids_selected = match_ids_selected[0:1] #to do the following loop only once
        
    for match_id in match_ids_selected:
        
        df_player_returns = df_player_returns[df_player_returns['match_id'] == match_id]
        match_name = get_match_name_from_match_id(match_id)

        figure_height = 15
        figure_width = 12
        if side == 'all_sides':
            directions_temp = directions[0:1]
        else:
            directions_temp = directions
            
        for direction in directions_temp:
            #pass
            display(Markdown(f"## {serve.replace('_', ' ')} - {side.replace('_', ' ').title()} - {direction.replace('_', ' ').title()}"))
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figure_width, figure_height))  #constrained_layout=False
            draw_return_depth(df_player_returns, ax, match_name, serve_no = serve, side = side, direction = direction, for_opponents=for_opponents)       
            #file_name = folder_main + 'Return reports visuals depth/' + folder_name + '/' + match_name + ' ' + serve + ' ' + side + ' ' + direction + '.png'
            #print(file_name)
            #fig.savefig(file_name, dpi=300, bbox_inches='tight', pad_inches=0)
        
    return fig
        #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figure_width, figure_height))  #constrained_layout=False
        #draw_return_points(df_player_returns, ax, match_name, serve_no = '1st_serve', side = 'deuce', direction = 'all_directions')        
        #fig.savefig(folder_main + 'Return reports visuals/' + folder_selected + '/' + match_name + '-1st_serve_DEUCE.png', dpi=300, bbox_inches='tight', pad_inches=0)

    #plt.subplots_adjust(wspace=0.1, hspace=0)

def draw_return_depth(df_player_returns, ax, match_name, serve_no, side, direction, for_opponents=False):    
    c_green = '#A3FF74' #'#89E381'
    c_orange = '#FF7F00' #'#D27E24'
    c_red = '#E61A25' #'#C61A25' #'#BB2D3B'
    c_gray = '#7C8F9F'
    
    df_return = df_player_returns.copy()
    if serve_no != 'both_serves':
        if serve_no == '1st_serve':
            df_return = df_player_returns[df_player_returns['serve_number']==1]
        else:
            df_return = df_player_returns[df_player_returns['serve_number']==2]
        
    if side != 'all_sides':
        df_return = df_return[df_return['serve_deuce_or_ad'] == side]

    if direction != 'all_directions':
        df_return = df_return[df_return['serve_direction'] == direction]

    
    #Remove noise
    #Remove bounces on the same side
    df_return = df_return[~(df_return['CONTACT_X'] * df_return['REBOUND_X'] >0)]
    #Limit max speed
    #df_return = df_return[df_return['SPEED']<160]
    df_return['SPEED'] = np.where(df_return['SPEED']>150, 150, df_return['SPEED'])
    
    #Limit min speed
    df_return['SPEED'] = np.where(((df_return['SPEED']>1)&(df_return['SPEED']<=40)), 41, df_return['SPEED'])
    
    df_return_in = df_return[df_return['is_shot_in'] == 1]
    df_return_not_in = df_return[df_return['is_shot_in'] == 0]
    df_return_in_net = df_return[df_return['is_in_the_net'] == 1]
    df_return_in_win = df_return_in[df_return_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_in_lose = df_return_in[df_return_in['PLAYER_WIN_NAME'] != selected_player_name]
    
    #bounce left, middle, right
    deep_border = 9.18
    short_border = 6.40
    
    df_return_deep_in = df_return_in[df_return_in['REBOUND_X_abs'] >= deep_border]
    df_return_middle_in = df_return_in[(df_return_in['REBOUND_X_abs'] > short_border) & (df_return_in['REBOUND_X_abs'] < deep_border)]
    df_return_short_in = df_return_in[df_return_in['REBOUND_X_abs'] <= short_border]
    
    df_return_deep_in_win = df_return_deep_in[df_return_deep_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_deep_in_lose = df_return_deep_in[df_return_deep_in['PLAYER_WIN_NAME'] != selected_player_name]
    df_return_middle_in_win = df_return_middle_in[df_return_middle_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_middle_in_lose = df_return_middle_in[df_return_middle_in['PLAYER_WIN_NAME'] != selected_player_name]
    df_return_short_in_win = df_return_short_in[df_return_short_in['PLAYER_WIN_NAME'] == selected_player_name]
    df_return_short_in_lose = df_return_short_in[df_return_short_in['PLAYER_WIN_NAME'] != selected_player_name]       

    #Draw court
    set_half_court(ax)

    #Title
    ax.add_patch(FancyBboxPatch((-5.9, -1.9), 11.8, 1.1, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))

    if for_opponents:
        title_text = 'OPPONENTS ' + serve_no.replace('_', ' ').upper() + ' RETURN PLACEMENT'  
    else:
        title_text = selected_player_name + ' ' + serve_no.replace('_', ' ').upper() + ' RETURN PLACEMENT' 
        
    ax.text(-5.7, -1.35, title_text, fontsize=22, weight='bold')
    ax.text(-5.7, -1.7, match_name, fontsize=16, weight='normal')
        
    if side == 'all_sides':
        side_text = 'BOTH SIDES'
    else:
        side_text = side.upper() 
    if direction == 'all_directions':
        side_text = side_text + ' ALL DIRECTIONS'
    else:
        side_text = side_text + ' ' + direction.upper()
    side_text = side_text + ' SERVE'
    
    ax.text(5.6, -1.2, side_text, fontsize=16, ha='right')
    #ax.text(5.6, -1.7, str(len(df_return)) + ' RETURNS', fontsize=16, ha='right')
    if len(df_return) == 0:
        return_in_perc = 0
    else:
        return_in_perc = int(round(100*len(df_return_in)/len(df_return),0))
    ax.text(5.6, -1.7, str(len(df_return)) + ' RETURNS - ' + str(len(df_return_in)) + ' IN (' + str(return_in_perc) + ' %)', fontsize=16, ha='right')
    
    
    #If no points finish here
    if len(df_return) == 0:
        ax.add_patch(FancyBboxPatch((-2.5, 1.9), 5, 1.1, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
        ax.text(-1, 2.3, 'NO SUCH SERVES', fontsize=22, weight='bold')
        return
    
    #Draw points
    #Set params
    #print(len(df_return))
    #min_speed = min(df_return[~np.isnan(df_return['REBOUND_X_abs'])]['SPEED'].values, default=0)
    #max_speed = max(df_return[~np.isnan(df_return['REBOUND_X_abs'])]['SPEED'].values, default=200)
    min_speed = min(df_return['SPEED'].values, default=0)
    max_speed = max(df_return['SPEED'].values, default=200)
    #print(min_speed)
    #print(max_speed)
    
    power = 1 #1.05 #1.1   
    lower_speed_border = int(min_speed/10)*10
    max_speed = max(df_return['SPEED'].values)
    upper_speed_border = int(max_speed/10)*10
    min_size_px = 5
    alpha = 0.7
    #Returns in win
    ax.scatter(df_return_in_win['REBOUND_Y_mirrored'].values, df_return_in_win['REBOUND_X_abs'].values, s = (df_return_in_win['SPEED'] - lower_speed_border + min_size_px)**power, label= selected_player_initials + ' won the point', c = c_green, alpha = alpha, edgecolors='black', zorder=11)        
    #Returns in lose
    ax.scatter(df_return_in_lose['REBOUND_Y_mirrored'].values, df_return_in_lose['REBOUND_X_abs'].values, s = (df_return_in_lose['SPEED'] - lower_speed_border + min_size_px)**power, label= selected_player_initials + ' lost the point', c = c_orange, alpha = alpha, edgecolors='black', zorder=12)        
    #Returns out
    ax.scatter(df_return_not_in['REBOUND_Y_mirrored'].values, df_return_not_in['REBOUND_X_abs'].values, s = (df_return_not_in['SPEED'] - lower_speed_border + min_size_px)**power, label= 'Return out', c = c_red, alpha = alpha, edgecolors='black', zorder=10)        
    #Returns in net
    ax.scatter(df_return_in_net['NET_COORD_Y'].values, [0]*len(df_return_in_net), s = (df_return_in_net['SPEED'] - lower_speed_border + min_size_px)**power, label= 'Return into net', c = c_gray, alpha = 1, edgecolors='black')        
    
    #In the net
    text_for_returns_in_net = str(len(df_return_in_net)) + ' returns into net (' + str(int(round(100*len(df_return_in_net)/len(df_return), 0))) + '% of returns)'
    ax.text(0, 0.5, text_for_returns_in_net, fontsize=22, ha='center', va='center')
    
    
    #Legend
    #if is_serve_deuce_side:
    #    location = 'upper right'
    #else:
    #    location = 'upper left'
    lgnd = ax.legend(loc='upper right', fancybox=True, framealpha=0.7, fontsize=18, bbox_to_anchor=(0.265,0.46))
    lgnd.legend_handles[0]._sizes = [400]
    lgnd.legend_handles[1]._sizes = [400]
    lgnd.legend_handles[2]._sizes = [400]
    lgnd.legend_handles[3]._sizes = [400]    
    ax.add_artist(lgnd)
    
    #legend for speed
    #We need dummy points with speeds we want to show on the legend
    dummy_points_for_speed = []
    for i in range(lower_speed_border, upper_speed_border + 11, 20): #+10 so that we get also last value
        dummy_points_for_speed.append(ax.scatter(-100, -100, s = (i - lower_speed_border + min_size_px)**power, label= str(i) + ' km/h', facecolors='none', edgecolors='black', linewidth=2))

    ax.legend(handles=dummy_points_for_speed, loc='lower right', bbox_to_anchor=(0.995,0.30), fancybox=True, framealpha=0.7, fontsize=18, labelspacing=0.6)

    
    #Subaxeses
    box_y_start = -5.5
    box_width = 3.7
    box_height = 3.3
    #White Background squares
    ax.add_patch(FancyBboxPatch((-6.0, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    ax.add_patch(FancyBboxPatch((-1.95, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    ax.add_patch(FancyBboxPatch((2.00, box_y_start), box_width, box_height, boxstyle="round,pad=-0.0040,rounding_size=0.02", ec="none", fc='white', mutation_aspect=4))
    
    #Create subaxes
    subax1, subax2, subax3 = set_embeded_graphs(ax, 0.03)
    
    #Draw subgraph pies    
    box_y_start = 1.2  
    total_y_start = -3.1
    player_name_y = -3.7
    player_perc_y = -4.2
    
    subax1.set_title('Deep Return Win %', fontsize=18, y=box_y_start) #which serve it is
    ax.text(-4.0, total_y_start, str(len(df_return_deep_in)) + ' TOTAL (' + str(int(round(100*len(df_return_deep_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center') #How many serves in this direction
    subax1.pie([len(df_return_deep_in_win), len(df_return_deep_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90) #Draw PIE
    ax.text(-4.7, player_name_y, selected_player_name, fontsize=13, ha='right', va='center')  #Print player name
    ax.text(-4.9, player_perc_y, str(int(round(100*len(df_return_deep_in_win)/np.nextafter(len(df_return_deep_in), 1), 0))) + '%', fontsize=13, ha='right', va='center') #print % of won points
    ax.text(-3.4, player_name_y, 'OPPONENT', fontsize=13, ha='left', va='center') #Opponent name
    ax.text(-3.1, player_perc_y, str(int(round(100*len(df_return_deep_in_lose)/np.nextafter(len(df_return_deep_in), 1), 0))) + '%', fontsize=13, ha='left', va='center') #Print % win for opponent
    
    subax2.set_title('Middle Return Win %', fontsize=18, y=box_y_start)
    ax.text(0, total_y_start, str(len(df_return_middle_in)) + ' TOTAL (' + str(int(round(100*len(df_return_middle_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center')
    subax2.pie([len(df_return_middle_in_win), len(df_return_middle_in_lose)], colors = [c_green, c_orange], shadow=True, startangle=90)
    ax.text(-0.7, player_name_y, selected_player_name, fontsize=13, ha='right', va='center')
    ax.text(-1.0, player_perc_y, str(int(round(100*len(df_return_middle_in_win)/np.nextafter(len(df_return_middle_in), 1), 0))) + '%', fontsize=13, ha='right', va='center')
    ax.text(0.8, player_name_y, 'OPPONENT', fontsize=13, ha='left', va='center')
    ax.text(1.0, player_perc_y, str(int(round(100*len(df_return_middle_in_lose)/np.nextafter(len(df_return_middle_in), 1), 0))) + '%', fontsize=13, ha='left', va='center')
    
    subax3.set_title('Short Return Win %', fontsize=18, y=box_y_start)
    ax.text(4.1, total_y_start, str(len(df_return_short_in)) + ' TOTAL (' + str(int(round(100*len(df_return_short_in)/np.nextafter(len(df_return_in),1), 0))) + ' %)', fontsize=13, ha='center', va='center')


# --- additional verbatim helpers ---
def divide_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def set_half_court_contact(ax, court_draw_width_start = -6.5, court_draw_width_end = 6.5):
    #court_draw_width_start = -6.5
    #court_draw_width_end = 6.5
    court_draw_height_end = 17
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
    
    ax.plot([net_post_x_left, net_post_x_right], [0, 0], linewidth=linewidth, linestyle="--", c=line_color, zorder = -900) #net
    ax.plot([-court_width/2, -court_width/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #sideline
    ax.plot([court_width/2, court_width/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #sideline
    ax.plot([court_width_doubles/2, court_width_doubles/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #sideline doubles
    ax.plot([-court_width_doubles/2, -court_width_doubles/2], [-1, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #sideline doubles
    ax.plot([-court_width_doubles/2, court_width_doubles/2], [court_length, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #baseline
    #ax.plot([-court_width_doubles/2, court_width_doubles/2], [-court_length, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline
    ax.plot([-court_width/2, court_width/2], [6.40, 6.40], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #servisline
    #ax.plot([-court_width/2, court_width/2], [-6.40, -6.40], linewidth=linewidth, linestyle="-", c=line_color) #servisline
    ax.plot([0,0], [-1, 6.40], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #servis middle line
    ax.plot([0,0], [court_length-0.3, court_length], linewidth=linewidth, linestyle="-", c=line_color, zorder = -900) #baseline middle line
    #ax.plot([0,0], [-court_length+0.3, -court_length], linewidth=linewidth, linestyle="-", c=line_color) #baseline middle line
    
    #Net post
    #ax.add_artist(Circle((net_post_x_left, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_artist(Circle((net_post_x_right, 0), radius = 0.1, linewidth=1, color='white', transform=ax.transData))
    #ax.add_patch(Rectangle((net_post_x_left - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    #ax.add_patch(Rectangle((net_post_x_right - 0.1, -0.1), 0.2, 0.2, linewidth=1, edgecolor='white', facecolor='white', fill=True))
    
    #Court color
    court_color = '#62666d'
    around_court_color = '#bdc1c3'
    if len(surfaces) != 1:
        ax.set_facecolor(court_color)
        #Out of court color
        alpha = 1
        ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=around_court_color, zorder = -999)
        ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=around_court_color, zorder = -999)
        #Behind the baseline
        ax.axhspan(court_length, court_length + 10, alpha=alpha, color=around_court_color, zorder = -999)
        ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=around_court_color, zorder = -999)
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
            ax.set_facecolor(court_color)
            #Out of court color
            alpha = 1
            ax.axvspan(court_draw_width_start, -1 * court_width_doubles/2, alpha=alpha, color=around_court_color, zorder = -999)
            ax.axvspan(court_width_doubles/2, court_draw_width_end, alpha=alpha, color=around_court_color, zorder = -999)
            #Behind the baseline
            ax.axhspan(court_length, court_length + 10, alpha=alpha, color=around_court_color, zorder = -999)
            ax.axhspan(-court_length, -court_length - 10, alpha=alpha, color=around_court_color, zorder = -999)
    
    #Hide border
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Hide axes labels and ticks
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def set_embeded_graphs(ax, y_pos):
    #For all embeded plots
    height = 0.10
    width = 0.15
    #y_pos = 0.16
    y_pos = 0.06
    
    #1
    x_pos = 0.157
    rect = [x_pos,y_pos,width,height]
    subax1 = add_subplot_axes(ax,rect)
    
    #2
    x_pos = 0.425
    rect = [x_pos,y_pos,width,height]
    subax2 = add_subplot_axes(ax,rect)
    
    #3
    x_pos = 0.693
    rect = [x_pos,y_pos,width,height]
    subax3 = add_subplot_axes(ax,rect)
    
    all_axes = [subax1, subax2, subax3]
    
    for axis in all_axes:
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        
    return subax1, subax2, subax3

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

def get_match_name_from_match_id(match_id):
    match_id_splited = match_id.split('_')
    tourney_name = match_id_splited[0]
    tourney_year = match_id_splited[1]
    opponent_name = match_id_splited[-1]
    #print(str(selected_player_name.split('.')[-1].upper()))
    if selected_player_name.split('.')[-1].upper() in opponent_name.upper():
        if len(match_id_splited[-2].upper()) == 2 and '.' in match_id_splited[-2].upper():
            opponent_name = match_id_splited[-3]
        else:
            opponent_name = match_id_splited[-2]
    match_name = tourney_name + '' + tourney_year + ' vs. ' + opponent_name.capitalize()
    #match_name = match_name.replace(' ', '_')
    match_name = match_name.replace('MS003', '2019')
    match_name = match_name.replace('MS015', '2019')
    return match_name

def set_full_court(ax):
    
    img = plt.imread("new_full_court.png")
    court_draw_width_start = -8.5
    court_draw_width_end = 8.5
    court_draw_height_end = 17
    court_draw_height_start = -17

    ax.set_xlim((court_draw_width_start, court_draw_width_end))
    ax.set_ylim((court_draw_height_start, court_draw_height_end))
    

    ax.imshow(img, extent=[court_draw_width_start, court_draw_width_end, court_draw_height_start, court_draw_height_end])
    #plt.yticks(np.arange(court_draw_height_start, court_draw_height_end, 0.50))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
