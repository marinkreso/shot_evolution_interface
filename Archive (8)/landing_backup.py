from nicegui import ui, app
from fastapi import FastAPI


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

def init(fastapi_app: FastAPI) -> None:
    

    ui.run_with(
        fastapi_app,
        mount_path='/landing',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )

    @ui.page('/landing/post_match_list')
    async def show():
        ui.label('Hello, Landing Page!')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')