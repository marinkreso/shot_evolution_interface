from nicegui import ui

#ui.html(f'<h1 class="text-center">sometitle</h1>').classes('text-2xl').classes('mx-auto')
ui.separator().classes('w-2/3').classes('mx-auto')

with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
    ui.label('MEDVEDEV').classes('w-2/12').style('color: #28a745')
    ui.label('').classes('w-8/12')
    ui.label('DAVIDOVICH FOKINA').classes('w-2/12').style('color: #dc3545')
ui.separator().classes('w-2/3').classes('mx-auto')
with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
    ui.label('78')#.classes('mx-auto')#.classes('')
    ui.linear_progress(0.6, color='#28a745', show_value=False, size="20px").classes('w-5/12').props('reverse').props('rounded')
    with ui.row().classes('w-2/12'):#.classes('place-content-center'):
        ui.label('1st serve in% - pressure points').style('text-align: center;')#.classes('w-2/12')#.classes('')
    ui.linear_progress(0.4, color='#dc3545', show_value=False, size="20px").classes('w-5/12').props('rounded')
    ui.label('22')#.classes('mx-auto')#.classes('')
ui.separator().classes('w-2/3').classes('mx-auto')
with ui.row().classes('w-2/3 no-wrap').classes('mx-auto'):
    ui.label('60')#.classes('mx-auto')#.classes('')
    ui.linear_progress(0.6, color='#ADD8E6', show_value=False, size="20px").classes('w-5/12').props('reverse')#.props('rounded')
    with ui.row().classes('w-2/12'):#.classes('place-content-center'):
        ui.label('Player Average').classes('mx-auto').style('text-align: center;')#.classes('w-2/12')#.classes('')
    ui.linear_progress(0.4, color='#FFFF00', show_value=False, size="20px").classes('w-5/12').props('rounded')
    ui.label('55')#.classes('mx-auto')#.classes('')
ui.separator().classes('w-2/3').classes('mx-auto')

ui.run()