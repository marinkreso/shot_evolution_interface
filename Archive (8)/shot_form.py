from nicegui import ui, run
import pandas as pd
import datetime
import json

import psycopg2
from psycopg2 import pool
from psycopg2.extras import Json
from datetime import datetime

user='marin'
password='RV4vjA9xUxTjMc'
host='gsa-pg-data-production.postgres.database.azure.com'
port='5432'
database='hawkeye'
# Initialize a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,      # Minimum number of connections in the pool
    maxconn=10,     # Maximum number of connections in the pool
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)

def insert_data_to_db(key, value, reportname):
    conn = None
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        
        # Check if the connection is valid
        if conn.closed:
            print("Connection is closed. Reconnecting...")
            conn = connection_pool.getconn()

        # Create a cursor object
        cur = conn.cursor()

        # SQL query to insert data
        insert_sql = """
        INSERT INTO hawkeye_app.shot_evolution_table (key, value, created_at, reportname)
        VALUES (%s, %s, %s, %s)
        """
        print(insert_sql)
        # Insert data into the table
        cur.execute(insert_sql, (key, Json(value), datetime.now(), reportname))

        # Commit the transaction
        conn.commit()

        print(f"Data inserted successfully for key: {key}")

        # Close the cursor
        cur.close()

    except Exception as e:
        # If there's an error, rollback the transaction
        if conn:
            conn.rollback()
        print(f"Error while inserting data: {e}")

    finally:
        # Always return the connection back to the pool
        if conn:
            connection_pool.putconn(conn)

# Close the connection pool when shutting down the API
def close_pool():
    connection_pool.closeall()

async def insert_data_and_generate_link(nor):
    if all(player for player in nor.players):
        import uuid
        link_id = str(uuid.uuid4())
        data = []
        for i in range(nor.number):
            if nor.matches[i]:
                data.append({
                    'player': nor.players[i],
                    'matches': nor.matches[i],
                    'name': nor.columns[i]
                })
            else:
                data.append({
                    'player': nor.players[i],
                    'matches': nor.filter_only_matches[i],
                    'name': nor.columns[i]
                })

        await run.io_bound(insert_data_to_db, f'{link_id}', data, nor.report_name)
        ui.navigate.to(f'http://127.0.0.1:8000/gui/report/{link_id}')
    else:
        ui.notify(f"PLEASE ENSURE THAT YOU'VE SELECTED PLAYER FOR EVERY COLUMN".upper(), position='center', type='negative')
    #ui.navigate.to('https://gsapostmatch.azurewebsites.net/gui/report/OSAKA_COMPARISON')
    



with open('all_data.json') as f:
    all_data = json.load(f)

class ModelShot:
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
                if k == 'PLAYER':
                   
                    if not item[k] == v:
                        match = False

                else:
                    if not item[k] in v:
                        match = False
            
            if match:
                results.append(cls(**item))
        
        return results
    


class MatchDataShot(ModelShot):
    pass

db = {'MatchDataShot': sorted(all_data, key=lambda x: x['DATE'], reverse=True)}

def shot_evolution_creator( 
    noe,
    i,
    data,
    columns,
    dialog,
    table_classes=''
) -> None:

    
    def handle_save():
        any_chosen = False
        for d in data:
            if d['SELECT']:
                any_chosen = True
                break
        if any_chosen:        
             noe.matches[i] = [d['match_id'] for d in data if d['SELECT']]
            #tab_report.refresh(movement_data, [d['match_id'] for d in data if d['SELECT']], image_dir, selected_player=selected_player)
        else:
            noe.matches[i] = [d['match_id'] for d in data]
            #tab_report.refresh(movement_data, [d['match_id'] for d in data], image_dir, selected_player=selected_player)
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

                        # if on_change:
                        #     cls_parms["on_change"] = lambda event, r=row_index, c=col_name: on_change(
                        #         r=r, c=c, value=event.value
                        #     )

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

@ui.page('/', response_timeout=15, dark=True,favicon='https://operationslakedb.blob.core.windows.net/gsa-post-match/fav.png')
async def report_creation():
    ui.markdown('# PLAYER EVOLUTION/COMPARISON').classes('mx-auto')
    
    class NumberOfReports:
            def __init__(self):
                self.number = 2
                self.surfaces = [[]]*2
                self.players = [[]]*2
                self.tournaments = [[]]*2
                self.years = [[]]*2
                self.matches = [[]]*2
                self.filter_only_matches = [[]]*2
                self.report_name = ''
                self.columns = [f'Column {i+1}' for i in range(2)]
    nor = NumberOfReports()
    def add_new_column(e):
         nor.number = nor.number + 1
         nor.matches.append([])
         nor.filter_only_matches.append([])
         nor.years.append([])
         nor.tournaments.append([])
         nor.surfaces.append([])
         nor.players.append([])
         nor.columns.append(f'Column {nor.number+1}')
         form_view.refresh(nor.number)
    def set_column_name(value, i):
        nor.columns[i] = value
    @ui.refreshable
    async def form_view(x):
        creator_refreshables = [ui.refreshable(shot_evolution_creator) for _ in range(x)]
        players = []
        surfaces = []
        tournaments = []
        years = []
        
        async def on_company_change(i, dialoger):
            filters = dict()
            player = players[i].value
            surface = surfaces[i].value
            tournament = tournaments[i].value
            year = years[i].value
            #match = matches[i].value
            print(f"{player}-{str(year)}-{str(tournament)}-{str(surface)}")
            if player:
                filters['PLAYER'] = player
                nor.players[i] = player
                
        
            if surface:
                filters['SURFACE'] = surface
                nor.surfaces[i] = surface
                
            if year:
                filters['YEAR'] = year
                nor.years[i] = year
            
            if tournament:
                filters['TOURNAMENT'] = tournament
                nor.tournaments[i] = tournament
            filtered_matches = await MatchDataShot.filter(db,**filters)
            print([m.match_id for m in filtered_matches])
            selected_matches = sorted(list(set([row.match_id for row in filtered_matches])))
            nor.filter_only_matches[i] = selected_matches
            rows = [
                            {
                                'SELECT': True if m.match_id in nor.matches[i] else False,
                                'OPPONENT': m.OPPONENT,
                                'YEAR': m.YEAR,
                                'TOURNAMENT': m.TOURNAMENT,
                                'SURFACE': m.SURFACE,
                                'match_id': m.match_id
                            } for m in filtered_matches
                        ]
            #nor.matches[i] = selected_matches
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
            
            years[i].set_options(sorted(list(set([m.YEAR for m in await MatchDataShot.filter(db,**{x: filters[x] for x in filters if x != 'YEAR'})]))))
            surfaces[i].set_options(sorted(list(set([m.SURFACE for m in await MatchDataShot.filter(db,**{x: filters[x] for x in filters if x != 'SURFACE'})]))))
            tournaments[i].set_options(sorted(list(set([m.TOURNAMENT for m in await MatchDataShot.filter(db,**{x: filters[x] for x in filters if x != 'TOURNAMENT'})]))))
            
            creator_refreshables[i].refresh( 
                nor,
                i,
                rows,
                columns,
                dialoger,
                table_classes='text-center mx-auto w-full'
            )
            
            
        with ui.row().classes('mx-auto'):
            for i in range(x):
                with ui.dialog() as dialog, ui.card():
                    rows = [
                            {
                                'SELECT': False,
                                'OPPONENT': m.OPPONENT,
                                'YEAR': m.YEAR,
                                'TOURNAMENT': m.TOURNAMENT,
                                'SURFACE': m.SURFACE,
                                'match_id': m.match_id
                            } for m in []
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
                    creator_refreshables[i]( 
                        nor,
                        i,
                        rows,
                        columns,
                        dialog,
                        table_classes='text-center mx-auto w-full'
                    )
                with ui.column().classes('mx-auto'):
                    #ui.input('Column Name')
                    ui.input(label=f'Enter Column Name', placeholder=f'Enter Column Name', on_change=lambda e, i=i: set_column_name(e.value, i)).classes('mx-auto')
                    with ui.card():
                        with ui.column().classes('items-center'):
                            player_selection = ui.select(
                                label='Player',
                                with_input=True,
                                on_change=lambda i=i, dialog=dialog: on_company_change(i, dialog),
                                options=sorted(list(set([x['PLAYER'] for x in all_data]))),
                                ).classes('w-40') 
                            if nor.players[i]:
                                player_selection.set_value(nor.players[i])
                            players.append(player_selection)
                            year_selection = ui.select(
                                label='Year(s)',
                                multiple=True,
                                on_change=lambda i=i, dialog=dialog: on_company_change(i, dialog),
                                options=sorted(list(set([x['YEAR'] for x in all_data]))),
                            ).classes('w-40').props('use-chips')
                            if nor.years[i]:
                                year_selection.set_value(nor.years[i])
                            years.append(year_selection)
                            surface_selection = ui.select(
                                label='Surfaces',
                                multiple=True,
                                on_change=lambda i=i, dialog=dialog: on_company_change(i, dialog),
                                options=list(set([x['SURFACE'] for x in all_data])),
                            ).classes('w-40').props('use-chips')
                            if nor.surfaces[i]:
                                surface_selection.set_value(nor.surfaces[i])
                            surfaces.append(surface_selection)
                            tournament_selection = ui.select(
                                label='Tournaments',
                                multiple=True,
                                on_change=lambda i=i, dialog=dialog: on_company_change(i, dialog),
                                with_input=True,
                                options=sorted(list(set([x['TOURNAMENT'] for x in all_data]))),
                            ).classes('w-40').props('use-chips')
                            if nor.tournaments[i]:
                                tournament_selection.set_value(nor.tournaments[i])
                            tournaments.append(tournament_selection)
                            ui.button('VIEW MATCHES', on_click=dialog.open)
                            #match_selection = ui.select(label='Available matches', options=[], multiple=True)#.props('use-chips')
                            #matches.append(match_selection)
        
        ui.button(f'Add New Column', icon='add', on_click=lambda e: add_new_column(e.sender)).classes('mx-auto')
    async def set_report_name(value):
        nor.report_name = value
    ui.input(label=f'Enter Report Name', placeholder=f'Enter Report Name', on_change=lambda e: set_report_name(e.value)).classes('mx-auto')
    await form_view(nor.number)

    ui.button(f'Create Shot Evolution Report', on_click=lambda e: insert_data_and_generate_link(nor)).classes('mx-auto')
ui.run()
