from nicegui import ui

def create_text_header():
    with ui.header().classes('bg-gray-800 text-white p-4 shadow-md'):
        with ui.row().classes('items-center justify-between w-full'):
            # Title of the application
            

            # Navigation Options
            with ui.row().classes('gap-6'):
                ui.button('Shot evolution interface').props(f'color=bh-gray-800')#.classes('text-lg')
                ui.button('Post match report').props(f'color=bh-gray-800')#.classes('text-lg')
                ui.button('Movement report').props(f'color=bh-gray-800')#.classes('text-lg')
                ui.button('Tracking interface', on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug')).props(f'color=bh-gray-800')#.classes('text-lg')
            with ui.row():
                ui.image('https://operationslakedb.blob.core.windows.net/gsa-post-match/fav.png').classes('w-10')
                ui.label('Dashboard').classes('text-xl font-semibold')
create_text_header()
ui.html(''''
        <h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>
        <h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>
        <h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>
        <h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>
        ''')
ui.run()