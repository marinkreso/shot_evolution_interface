from nicegui import ui
ui.dark_mode(True)
with ui.dialog() as dialog, ui.card():
    with ui.card_section():
        ui.label('Terms of Agreement').classes('text-h6')
    ui.separator()
    with ui.card_section().classes('max-h-[50vh] scroll'):
        for i in range(15):ui.html('Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.',tag='p').classes('mb-4')
    ui.separator()
    with ui.card_actions().props('align="right"').classes('w-full'):
        ui.button('Decline',on_click=dialog.close).props('flat')
        ui.button('Accept',on_click=dialog.close).props('flat')
ui.button('Fixed size',on_click=dialog.open)

ui.run()