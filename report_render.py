import jinja2
from pathlib import Path

data_order = {
        'serve': [

            {'columns': ['first_serve_in_percentage',
                         'win_percent_first_serve',
                         'win_percent_second_serve',
            'first_serve_speed',
            'percent_of_first_serves_within_04m_of_sideline',
            'first_serve_speed_deuce_w',
            'first_serve_speed_deuce_t',
            'first_serve_speed_ad_t',
            'first_serve_speed_ad_w'
#             'win_percent_all',
#    'won_games_serve',
#    'aces_percenttal'
   ],

            'title': ''}
        ],
        'return': [

            {'columns': [
                'first_return_win_percentage',
                'first_return_in_percentage',
                'first_fh_return_in_percentage',
                'first_bh_return_in_percentage',
                'first_return_percent_deep',
            'first_return_defeat_under_five',
            #'first_return_extended_or_won', TODO check this
            'first_return_depth',
            ],
            'title': '1ST RETURN'},
            
            {'columns': [
                'second_return_win_percentage',
                'second_return_in_percentage',
                'second_fh_return_in_percentage',
                'second_bh_return_in_percentage',
                'second_return_aggressive',
            'second_return_percent_deep',
            'second_return_depth',
            ],
            'title': '2ND RETURN'}

        ],
        'return_speed': [
            {'columns': ['first_return_fh_speed',
            'first_return_bh_speed',
            
            'first_return_deuce_fh_speed',
            'first_return_deuce_bh_speed',
            'first_return_ad_fh_speed',
            'first_return_ad_bh_speed',
            ],
            'title': '1ST RETURNS'},
            {'columns': [
            'second_return_fh_speed',
            'second_return_bh_speed',
            'second_return_deuce_fh_speed',
            'second_return_deuce_bh_speed',
            'second_return_ad_fh_speed',
            'second_return_ad_bh_speed'],
            'title': '2ND RETURNS'}
        ],
        'consistency': [
            {'columns': ['fh_deuce_consistency',
            'fh_middle_consistency',
            'fh_ad_consistency',
            'bh_middle_consistency',
            'bh_ad_consistency',
            'bh_deuce_consistency'    ]}
        ],
        'initiative': [
            {'columns': ['initiative_first_over_nine',
            'initiative_over_nine',
            'initiative_second',
            'initiative_second_return']}
        ],
        'pressure': [
            {'columns': ['break_point_faced_win',
            'break_point_opportunity_win',
            'serve_speed_reduction_pressure',
            'return_speed_reduction_break']}
        ],
        'groundstroke_table': [
    {'columns': ['rally_winners_per_match',
    'rally_ue_per_match',
    'fh_amount',
    'bh_amount',
    'fh_cc_speed',
    
    
    
    'fh_cc_depth',
    
    
    
    'fh_cc_spin',
    'bh_cc_speed',
    'bh_cc_depth',
    'bh_cc_spin',
    'fh_dtl_speed',
    'fh_dtl_depth',
    'fh_dtl_spin',
    'bh_dtl_speed',
    'bh_dtl_depth',
    'bh_dtl_spin',
    
    ]}
            ],
            'winners_table': [
    {'columns': [
        'fh_cc_speed_winners',
    
    
    
    'fh_cc_depth_winners',
    
    
    
    'fh_cc_spin_winners',
        'bh_cc_speed_winners',
        'bh_cc_depth_winners',
        'bh_cc_spin_winners',
        'fh_dtl_speed_winners',
    'fh_dtl_depth_winners',
    'fh_dtl_spin_winners',
    'bh_dtl_speed_winners',
    'bh_dtl_depth_winners',
    'bh_dtl_spin_winners',
    
    
    ]}
            ],
        'approach_stats': [
           {'columns': [ 'approach_win_percentage',
    'approaches_to_FH',
    'approaches_to_BH',
    'approach_percentage',
    'approach_fh_win_perc',

    'approach_bh_win_perc',

    'approach_to_fh_win_perc',

    'approach_to_bh_win_perc']},
        ],
        'rally_play_type': [
            {'columns': ['rally_play_long_rallies_won',
    'rally_play_1st_serve_won_in_5_shots_or_less',
    'rally_play_1st_serve_finished_in_5_shots_or_less',
    'rally_play_2nd_return_won_in_5_or_less']}
        ],
        'dropshots': [           
    {'columns': ['dropshots_in_rallies',
    'dropshots_fh_win',
    'dropshots_bh_win']}
        ],
        'offensive': [
                {'columns': ['bh_dtl_all_rally_shots',
    'bh_dtl_well_placed',
    'bh_dtl_fast',
    'fh_all_rally_shots',
    'run_around_fh_percentage',
    'run_around_fh_winners_fe',
    'win_in_rallies_with_run_around_forehand',
    'fast_attacking_deuce_fh_cross_percentage',
    'fast_attacking_deuce_fh_cross_won',
    'fast_attacking_deuce_fh_line_percentage',
    'fast_attacking_deuce_fh_line_won',
    'opponent_moved_on_neutral_ball']}
        ],
        'defensive': [{'columns': ['on_the_run_fh_percent',
    'on_the_run_bh_percent',
    'on_the_run_fh_won',
    'on_the_run_bh_won',
    'on_the_run_bh_slice',
    'on_the_run_bh_slice_won',
    'on_the_run_bh_slice_won_on_fast']}],
    'rally_patterns': [{'columns': ['bh_cross_finish_win',
    'fh_cross_finish_win',
    'bh_cross_change_dtl_win',
    'fh_cross_change_dtl_win',
    'bh_cross_change_to_fh',
    'fh_cross_change_to_bh',
    'fast_ball_received_to_bh_percent',
    'fast_ball_outgoing_balls_to_opponent_bh']}]
        }

    
    
pretty_dict = {
    'fh_amount': '% OF FH SHOTS',
    'bh_amount': '% OF BH SHOTS',
    'second_return_in_percentage': '2ND RETURN IN%',
    'second_fh_return_in_percentage': '2ND FH RETURN IN%',
    'second_bh_return_in_percentage': '2ND BH RETURN IN%',
    'first_return_in_percentage': '1ST RETURN IN%',
    'first_fh_return_in_percentage': '1ST FH RETURN IN %',
    'first_bh_return_in_percentage': '1ST BH RETURN IN %',
    'win_percent_first_serve': '1ST SERVE WIN%',
    'win_percent_second_serve': '2ND SERVE WIN%',
     'win_percent_all': 'SERVE WIN%',
   'won_games_serve': 'SERVE GAMES WON%',
   'aces_percenttal': 'ACES %',
    'second_return_percent_deep': f'% of deep 2nd returns',
    'second_return_depth': '2nd Return Depth (in m)',
    'second_return_win_percentage': 'Win% on 2nd returns',
    'first_return_win_percentage': 'Win% on 1st returns',
    'first_return_win_percentage': 'Win% on 1st returns',
    'first_return_depth': '1st Return Depth (in m)',
    'first_serve_in_percentage': '1st serve in%',
    'first_serve_speed': '1st serve average speed',
    'percent_of_first_serves_within_04m_of_sideline': f'% of well-placed serves ',
    'serve_quality_deuce_wide': 'SQ 1st Deuce Wide',
    'serve_quality_deuce_t': 'SQ 1st Deuce T',
    'serve_quality_ad_wide': 'SQ 1st Ad Wide',
    'serve_quality_ad_t': 'SQ 1st AD T',
    'first_return_extended_or_won': f'% of 1st serve returns that led to extended rallies (5+) or returner winning the point under 5 shots',
    'first_return_defeat_under_five': f'% of 1st serve returns that led to extended rallies (5+)',
    'second_return_extended_or_won': f'% of good 2nd returns that extended the point (5+) or player won the point',
    'second_return_aggressive': f'% of aggresive 2nd returns',
    'first_return_percent_deep': f'% of deep 1st returns',
    'initiative_first_over_nine': f'% OF TIME INSIDE the court\n on while server on 1st serve when\n rallies 9+ shots ',
    'initiative_over_nine': f'% OF TIME INSIDE the court\n on rallies +9 shots',
    'initiative_second': '% of time inside the court on 2nd serve',
    'initiative_second_return': f'% OF TIME INSIDE the court\n on 2nd return',
    'fh_consistency': 'FH unforced errors/amount of total shots hit',
    'bh_consistency': 'BH unforced errors/amount of total shots hit',
    'fh_consistency_winners': 'FH unforced errors percentage among winners/FE',
    'bh_consistency_winners': 'BH unforced errors percentage among winners/FE',
    'break_point_faced_win': f'Break points faced win%',
    'break_point_opportunity_win': f'Break point opportunity win%',
    'serve_speed_reduction_pressure': '1st serve speed reduction when under pressure versus no pressure (negative means speed reduction)',
    'return_speed_reduction_break': 'Return speed reduction on break point opportunities (negative means speed reduction)',
    'fh_deuce_consistency': 'Deuce FH Ball in play%',
    'fh_middle_consistency': 'Middle FH Ball in play%',
    'fh_ad_consistency': 'Ad FH Ball in play%',
    'bh_middle_consistency': 'Middle BH Ball in play%',
    'bh_ad_consistency': 'Ad BH Ball in play%',
    'bh_deuce_consistency': 'Deuce BH Ball in play%',
    'bh_dtl_all_rally_shots': f'% BH DTL IN ALL RALLIES',
    'bh_dtl_well_placed': f'% BH DTL WELL PLACED' ,
    'bh_dtl_fast': f'% FAST BH DTL',
    'fh_all_rally_shots': f'% FH HIT IN RALLIES',
    'run_around_fh_percentage': f'% USE RUN AROUND FH',
    'run_around_fh_winners_fe': f'% WINNERS WHEN RUN AROUND FH',
    'win_in_rallies_with_run_around_forehand': f'WIN % IN RALLIES USING RUN AROUND FH',
    'fast_attacking_deuce_fh_cross_percentage': f'% FAST ATTACKING DEUCE FH CROSS SHOTS',
    'fast_attacking_deuce_fh_cross_won': f'% FAST ATTACKING DEUCE FH CROSS WON',
    'fast_attacking_deuce_fh_line_percentage': f'% FAST ATTACKING DEUCE FH DTL SHOTS',
    'fast_attacking_deuce_fh_line_won': f'% FAST ATTACKING DEUCE FH DTL WON',
    'opponent_moved_on_neutral_ball': f'% MOVED THE OPPONENT AFTER RECEIVING A NEUTRAL BALL',
    'on_the_run_fh_percent': f'% OF TIMES PUT ON THE RUN TO THE FH IN RALLIES',
'on_the_run_bh_percent': f'% OF TIMES PUT ON THE RUN TO THE BH IN RALLIES',
'on_the_run_fh_won': f'% WON WHEN ON THE RUN TO FH',
'on_the_run_bh_won': f'% WON WHEN ON THE RUN TO BH',
'on_the_run_bh_slice': f'% USED SLICE WHEN ON THE RUN TO THE BH',
'on_the_run_bh_slice_won': f'% WON WHEN BH SLICE ON THE RUN',
'on_the_run_bh_slice_won_on_fast': f'% WON WHEN BH SLICE ON THE RUN ON FAST INCOMING BALL',
'bh_cross_finish_win': f'WIN % BH CROSS FINISH',
'fh_cross_finish_win':f'WIN % FH CROSS FINISH',
'bh_cross_change_dtl_win': f'WIN % BH CROSS CHANGE DTL',
'fh_cross_change_dtl_win': f'WIN % FH CROSS CHANGE DTL',
'bh_cross_change_to_fh': f'WIN % BH CROSS CHANGE TO FH',
'fh_cross_change_to_bh': f'WIN % FH CROSS CHANGE TO BH',
'fast_ball_received_to_bh_percent': f'% OF FAST BALLS RECEIVED TO THE BH',
'fast_ball_outgoing_balls_to_opponent_bh': f'% OF FAST OUTGOING BALLS HIT TO OPPONENT BH',
'approach_win_percentage': f'WIN% ON APPROACHES',
'approaches_to_FH': f'% APPROACHES TO FH',
'approaches_to_BH': f'% APPROACHES TO BH',
'approach_percentage': f'% APPROACHES IN RALLIES',
'approach_fh_win_perc': f'WIN % ON FH APPROACHES',
'first_serve_speed_deuce_w': '1ST DEUCE WIDE AVG SPEED',
        'first_serve_speed_deuce_t': '1ST DEUCE T AVG SPEED',
        'first_serve_speed_ad_t': '1ST AD T AVG SPEED',
        'first_serve_speed_ad_w': '1ST AD WIDE AVG SPEED',

'approach_bh_win_perc': f'WIN % ON BH APPROACHES',

'approach_to_fh_win_perc': f'WIN % APPROACH TO FH',

'approach_to_bh_win_perc': f'WIN % APPROACH TO BH',
'dropshots_in_rallies': f'% DROPSHOTS IN RALLIES',
'dropshots_fh_win': f'WIN% ON FH DROP SHOTS',
'dropshots_bh_win': f'WIN% ON BH DROP SHOTS',
'rally_play_long_rallies_won': f'% of long rallies won',
'rally_play_1st_serve_won_in_5_shots_or_less': '% of 1st serves won in 5 shots or less',
'rally_play_1st_serve_finished_in_5_shots_or_less': '% of 1st serves finished in 5 shots or less',
'rally_play_2nd_return_won_in_5_or_less': '% of 2nd returns won in 5 shots or less',
'rally_winners_per_match': 'rally winners per match',
'rally_ue_per_match': 'rally ue per match',
'topspin_slice': 'BH Topspin / slice ratio',
'fh_cc_dtl_ratio': 'fh cc / fh dtl ratio',
'bh_cc_dtl_ratio': 'bh cc / bh dtl ratio',
'bh_cc_speed': 'bh cc speed',
'bh_dtl_speed': 'bh dtl speed',
'fh_dtl_speed': 'fh dtl speed',
'fh_cc_speed': 'fh cc speed',
'bh_cc_depth': 'bh cc depth',
'bh_dtl_depth': 'bh dtl depth',
'fh_dtl_depth': 'fh dtl depth',
'fh_cc_depth': 'fh cc depth',
'bh_cc_spin': 'bh cc spin',
'bh_dtl_spin': 'bh dtl spin',
'fh_dtl_spin': 'fh dtl spin',
'fh_cc_spin': 'fh cc spin',
'bh_cc_speed_winners': 'bh cc speed winners',
'bh_dtl_speed_winners': 'bh dtl speed winners',
'fh_dtl_speed_winners': 'fh dtl speed winners',
'fh_cc_speed_winners': 'fh cc speed winners',
'bh_cc_depth_winners': 'bh cc depth winners',
'bh_dtl_depth_winners': 'bh dtl depth winners',
'fh_dtl_depth_winners': 'fh dtl depth winners',
'fh_cc_depth_winners': 'fh cc depth winners',
'bh_cc_spin_winners': 'bh cc spin winners',
'bh_dtl_spin_winners': 'bh dtl spin winners',
'fh_dtl_spin_winners': 'fh dtl spin winners',
'fh_cc_spin_winners': 'fh cc spin winners',


}
for k in ['bh_cc_speed',
'bh_dtl_speed',
'fh_dtl_speed',
'fh_cc_speed',
'bh_cc_depth',
'bh_dtl_depth',
'fh_dtl_depth',
'fh_cc_depth',
'bh_cc_spin',
'bh_dtl_spin',
'fh_dtl_spin',
'fh_cc_spin',
'bh_cc_speed_winners',
'bh_dtl_speed_winners',
'fh_dtl_speed_winners',
'fh_cc_speed_winners',
'bh_cc_depth_winners',
'bh_dtl_depth_winners',
'fh_dtl_depth_winners',
'fh_cc_depth_winners',
'bh_cc_spin_winners',
'bh_dtl_spin_winners',
'fh_dtl_spin_winners',
'fh_cc_spin_winners']:
    if 'winner' in k:
        xk = f'{k}/fe'.replace('_', ' ').upper()
    else:
        xk = f'{k} - average_in_play'.replace('_', ' ').upper()
    
    pretty_dict[k] = xk
return_speed_columns = [
        'second_return_fh_speed',
        'second_return_bh_speed',
        'second_return_deuce_fh_speed',
        'second_return_deuce_bh_speed',
        'second_return_ad_fh_speed',
        'second_return_ad_bh_speed'] + ['first_return_fh_speed',
        'first_return_bh_speed',
        
        'first_return_deuce_fh_speed',
        'first_return_deuce_bh_speed',
        'first_return_ad_fh_speed',
        'first_return_ad_bh_speed',
        ]
for k in return_speed_columns:
    pretty_key = ''
    if 'fh' in k:
        pretty_key = pretty_key + 'FH'
    else:
        pretty_key = pretty_key + 'BH'
    if 'deuce' in k:
        pretty_key = pretty_key + ' DEUCE'
    elif '_ad_' in k:
        pretty_key = pretty_key + ' AD'
    pretty_dict[k] = pretty_key + ' SPEED (IN KMH)'


APP_DIR = Path(__file__).parent
TEMPLATE_FILE = "reportnew.html"


def create_shot_evolution(report_id, player, data):
    """Render the shot evolution report and write it to reports/. Returns the file name."""
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=str(APP_DIR)))
    template = template_env.get_template(TEMPLATE_FILE)
    context = {
        'player': player,
        'order': data_order,
        'pretty': pretty_dict,
        'data': data,
    }
    output_text = template.render(data=context)

    from convert_gsa_report import convert_gsa_report
    html_output = convert_gsa_report(output_text, title="Shot Quality Evolution Report", subtitle="")

    file_name = f"{player}_{report_id}.html".replace(' ', '_').replace('/', '-')
    reports_dir = APP_DIR / 'reports'
    reports_dir.mkdir(exist_ok=True)
    with open(reports_dir / file_name, 'w') as f:
        f.write(html_output)
    return file_name