from nicegui import ui
import pandas as pd
import datetime
import json

leaderboard = pd.read_parquet('leaderboard_haddad_new.parquet')
with open('all_data.json') as f:
    all_data = json.load(f)

class Model1:
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
    
class Model2:
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

class MatchData1(Model1):
    pass
class MatchData2(Model2):
    pass
class MatchData3(Model1):
    pass
class MatchData4(Model1):
    pass
db = {'MatchData1': sorted(all_data, key=lambda x: x['DATE'], reverse=True),
      'MatchData2': sorted(all_data, key=lambda x: x['DATE'], reverse=True),
      'MatchData3': sorted(all_data, key=lambda x: x['DATE'], reverse=True),
      'MatchData4': sorted(all_data, key=lambda x: x['DATE'], reverse=True)}

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
    MatchDatas = [MatchData1, MatchData2, MatchData3]
    class NumberOfReports:
            def __init__(self):
                self.number = 1
                self.surfaces = []
                self.tournaments = []
                self.years = []
                self.matches = [[]]*1
    nor = NumberOfReports()
    def add_new_column(e):
         nor.number = nor.number + 1
         nor.matches = [[]]*nor.number
         form_view.refresh(nor.number)
    @ui.refreshable
    async def form_view(x):
        creator_refreshables = [ui.refreshable(shot_evolution_creator)]*x
        players = []
        surfaces = []
        tournaments = []
        years = []
        filters = dict()
        async def on_company_change(i, dialoger, match_data):
            player = players[i].value
            surface = surfaces[i].value
            tournament = tournaments[i].value
            year = years[i].value
            #match = matches[i].value

            if player:
                filters['PLAYER'] = player
        
            if surface:
                filters['SURFACE'] = surface
                
            if year:
                filters['YEAR'] = year
            
            if tournament:
                filters['TOURNAMENT'] = tournament
            filtered_matches = await match_data.filter(db,**filters)
            selected_matches = sorted(list(set([row.match_id for row in filtered_matches])))
            nor.matches[i] = selected_matches
            rows = [
                            {
                                'SELECT': False,
                                'OPPONENT': m.OPPONENT,
                                'YEAR': m.YEAR,
                                'TOURNAMENT': m.TOURNAMENT,
                                'SURFACE': m.SURFACE,
                                'match_id': m.match_id
                            } for m in filtered_matches
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
            print(i, selected_matches)
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
                    ui.input('Column Name')
                    with ui.card():
                        with ui.column().classes('items-center'):
                            player_selection = ui.select(
                                label='Player',
                                with_input=True,
                                on_change=lambda i=i, dialog=dialog,match_data=MatchDatas[i]: on_company_change(i, dialog, match_data),
                                options=sorted(list(set([x['PLAYER'] for x in all_data]))),
                                ).classes('w-40') 
                            players.append(player_selection)
                            year_selection = ui.select(
                                label='Year(s)',
                                multiple=True,
                                options=sorted(list(set([x['YEAR'] for x in all_data]))),
                            ).classes('w-40').props('use-chips')
                            years.append(year_selection)
                            surface_selection = ui.select(
                                label='Surfaces',
                                multiple=True,
                                options=list(set([x['SURFACE'] for x in all_data])),
                            ).classes('w-40').props('use-chips')
                            surfaces.append(surface_selection)
                            tournament_selection = ui.select(
                                label='Tournaments',
                                multiple=True,
                                with_input=True,
                                options=sorted(list(set([x['TOURNAMENT'] for x in all_data]))),
                            ).classes('w-40').props('use-chips')
                            tournaments.append(tournament_selection)
                            ui.button('VIEW MATCHES', on_click=dialog.open)
                            #match_selection = ui.select(label='Available matches', options=[], multiple=True)#.props('use-chips')
                            #matches.append(match_selection)
        
        ui.button(f'Add New Column', icon='add', on_click=lambda e: add_new_column(e.sender)).classes('mx-auto')
    await form_view(nor.number)
    ui.button(f'Create Shot Evolution Report').classes('mx-auto')
ui.run()
    