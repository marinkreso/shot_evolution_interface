from nicegui import ui

select = ui.select([1, 2, 3], multiple=True, value=[1, 2]).props('use-chips')
with ui.row():
    ui.button('4, 5, 6',  on_click=lambda: select.set_options([4, 5, 6], value=[4, 5])).props('use-chips')

    ui.button('1, 2, 3', on_click=lambda: select.set_options([1, 2, 3], value=list([4, 5]))). props('use-chips')


ui.run()