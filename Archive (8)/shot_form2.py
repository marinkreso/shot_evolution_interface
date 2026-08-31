from nicegui import ui

@ui.page('/', response_timeout=15, dark=True,favicon='https://operationslakedb.blob.core.windows.net/gsa-post-match/fav.png')
async def report_creation():
    ui.markdown('# PLAYER EVOLUTION/COMPARISON').classes('mx-auto')
    with ui.dialog() as dialog, ui.card():
                        
        with ui.row().classes('w-full'):
            selected_p = ui.select(label='Players', options=list(set(['SINNER', 'FRITZ', 'OSAKA'])), with_input=True, multiple=True).classes('w-40').props('use-chips').props('rounded outlined')
            selected_surfaces = ui.select(label='Surfaces', options=['CLAY', 'HARD', 'GRASS'], multiple=True).classes('w-40').props('use-chips').props('rounded outlined')
            selected_years = ui.select(label='Seasons', options=['2022', '2023', '2024'], multiple=True).classes('w-40').props('use-chips').props('rounded outlined')
            selected_opponents = ui.select(label='Opponents', options=list(set(['SINNER', 'FRITZ', 'OSAKA']))).classes('w-40').props('use-chips').props('rounded outlined')
            
    @ui.refreshable
    class NumberOfReports:
            def __init__(self):
                self.number = 1
                self.selected_matches = []
                self.report_names = []
    nor = NumberOfReports()
    def add_new_column(e):
         nor.number = nor.number + 1
         form_view.refresh(nor.number)
    @ui.refreshable
    async def form_view(x):
        with ui.column().classes('mx-auto').style('justify-content: flex-start;'):
            for i in range(x):
                with ui.row():
                    with ui.card():
                        ui.input('Column Name').classes('w-40')
                        ui.button('SELECT MATCHES', on_click=dialog.open).props('rounded outlined')
        ui.button(f'Add New Column', icon='add', on_click=lambda e: add_new_column(e.sender)).classes('mx-auto')
    await form_view(nor.number)
    ui.button(f'Create Shot Evolution Report').classes('mx-auto')
ui.run()
