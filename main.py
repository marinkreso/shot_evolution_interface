import json
import os
import uuid
from pathlib import Path

from nicegui import app, run, ui

from report_core import compute_columns, load_leaderboard
from report_render import create_shot_evolution

APP_DIR = Path(__file__).parent
REPORTS_DIR = APP_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)

with open(APP_DIR / 'all_data2.json') as f:
    ALL_MATCHES = sorted(json.load(f), key=lambda x: x['match_id'])

with open(APP_DIR / 'lefties.json') as f:
    LEFTIE_PLAYERS = set(json.load(f))

ALL_PLAYERS = sorted({m['PLAYER'] for m in ALL_MATCHES})

app.add_static_files('/images', str(APP_DIR / 'images'))
app.add_static_files('/reports', str(REPORTS_DIR))

FAVICON = str(APP_DIR / 'images' / 'fav.png')


class ColumnState:
    def __init__(self, players=None):
        self.name = ''
        self.players = players or []
        self.years = []
        self.surfaces = []
        self.tournaments = []
        self.handedness = 'RIGHT'
        self.selected_matches = None  # None -> all matches that pass the filters


def filter_matches(col, skip=None):
    """Return the match rows that pass a column's filters (optionally ignoring one filter)."""
    results = []
    for m in ALL_MATCHES:
        if skip != 'players' and col.players and m['PLAYER'] not in col.players:
            continue
        if skip != 'years' and col.years and m['YEAR'] not in col.years:
            continue
        if skip != 'surfaces' and col.surfaces and m['SURFACE'] not in col.surfaces:
            continue
        if skip != 'tournaments' and col.tournaments and m['TOURNAMENT'] not in col.tournaments:
            continue
        if col.handedness == 'RIGHT' and m['OPPONENT'] in LEFTIE_PLAYERS:
            continue
        if col.handedness == 'LEFT' and m['OPPONENT'] not in LEFTIE_PLAYERS:
            continue
        results.append(m)
    return results


def display_name(col):
    if col.name.strip():
        return col.name.strip().upper()
    parts = [' + '.join(col.players)]
    if col.years:
        parts.append(' & '.join(sorted(col.years)))
    if col.surfaces:
        parts.append('/'.join(col.surfaces))
    if col.tournaments and len(col.tournaments) < 4:
        parts.append('/'.join(col.tournaments))
    return ' '.join(parts).upper()


@ui.page('/', dark=True, response_timeout=60, favicon=FAVICON)
async def index():
    ui.add_body_html('''
<header class="bg-[url(/images/footer.jpg)] w-full relative">
    <div class="absolute left-0 top-0 bg-[linear-gradient(240deg,_rgba(0,_0,_0,_0.00)_24.28%,_#000_63.81%)] h-full w-2/4"></div>
    <div class="container relative mx-auto flex items-center content-center align-middle h-full min-h-[200px] mt-10">
        <div class="mt-10 w-full">
            <h1 class="text-white font-light leading-none tracking-[3.05px] text-[50px] mb-12 text-center">
                <span class="text-[#D5AA2A]">SHOT EVOLUTION INTERFACE</span>
            </h1>
        </div>
    </div>
</header>
''')
    columns = [ColumnState(), ColumnState()]

    def open_matches_dialog(col):
        matches = filter_matches(col)
        rows = [
            {
                'key': f"{m['PLAYER']}|{m['match_id']}",
                'PLAYER': m['PLAYER'],
                'OPPONENT': m['OPPONENT'],
                'TOURNAMENT': m['TOURNAMENT'],
                'YEAR': m['YEAR'],
                'SURFACE': m['SURFACE'],
                'match_id': m['match_id'],
            }
            for m in matches
        ]
        table_columns = [
            {'name': c, 'label': c, 'field': c, 'align': 'left', 'sortable': True}
            for c in ['PLAYER', 'OPPONENT', 'TOURNAMENT', 'YEAR', 'SURFACE']
        ]
        with ui.dialog() as dialog, ui.card().classes('w-full').style('max-width: 900px'):
            ui.label(f'{len(rows)} MATCHES AVAILABLE').classes('text-lg mx-auto')
            search = ui.input('Search').props('outlined dense clearable').classes('w-full')
            table = ui.table(
                columns=table_columns,
                rows=rows,
                row_key='key',
                selection='multiple',
                pagination=10,
            ).classes('w-full')
            search.bind_value_to(table, 'filter')
            if col.selected_matches is None:
                table.selected = rows
            else:
                table.selected = [r for r in rows if r['match_id'] in col.selected_matches]

            def apply():
                if table.selected and len(table.selected) < len(rows):
                    col.selected_matches = sorted({r['match_id'] for r in table.selected})
                else:
                    col.selected_matches = None
                dialog.close()

            with ui.row().classes('mx-auto'):
                ui.button('APPLY', on_click=apply)
                ui.button('SELECT ALL', on_click=lambda: setattr(table, 'selected', rows)).props('outline')
                ui.button('UNSELECT ALL', on_click=lambda: setattr(table, 'selected', [])).props('outline')
                ui.button('CANCEL', on_click=dialog.close).props('flat')
        dialog.open()

    @ui.refreshable
    def columns_view():
        with ui.row().classes('mx-auto items-start justify-center'):
            for i, col in enumerate(columns):
                render_column(i, col)
        ui.button('ADD NEW COLUMN', icon='add', on_click=add_column).classes('mx-auto mt-4')

    def add_column():
        columns.append(ColumnState())
        columns_view.refresh()

    def remove_column(i):
        if len(columns) > 1:
            columns.pop(i)
            columns_view.refresh()

    def render_column(i, col):
        with ui.card().classes('no-shadow').props('flat bordered'):
            with ui.column().classes('items-center'):
                name_input = ui.input(label='Column Name', value=col.name).props('outlined').classes('w-60')
                name_input.bind_value_to(col, 'name')
                ui.separator().classes('w-full')

                selects = {}

                def options_for(dimension):
                    field = {'years': 'YEAR', 'surfaces': 'SURFACE', 'tournaments': 'TOURNAMENT'}[dimension]
                    return sorted({m[field] for m in filter_matches(col, skip=dimension)})

                def on_filter_change():
                    col.selected_matches = None
                    for dim, select in selects.items():
                        opts = options_for(dim)
                        value = [v for v in getattr(col, dim) if v in opts]
                        setattr(col, dim, value)
                        select.set_options(opts, value=value)
                    count_label.set_text(f'{len(filter_matches(col))} matches in this column')

                def on_players_change(e):
                    col.players = e.value or []
                    on_filter_change()

                ui.select(
                    label='Player(s) — several = averaged as one',
                    options=ALL_PLAYERS,
                    value=col.players,
                    multiple=True,
                    with_input=True,
                    on_change=on_players_change,
                ).classes('w-60').props('use-chips outlined')

                for dim, label in [('years', 'Year(s)'), ('surfaces', 'Surfaces'), ('tournaments', 'Tournaments')]:
                    def on_change(e, dim=dim):
                        setattr(col, dim, e.value or [])
                        on_filter_change()

                    selects[dim] = ui.select(
                        label=label,
                        options=options_for(dim),
                        value=getattr(col, dim),
                        multiple=True,
                        with_input=True,
                        on_change=on_change,
                    ).classes('w-60').props('use-chips outlined')

                def on_handedness_change(e):
                    col.handedness = e.value
                    on_filter_change()

                ui.select(
                    label='Opponent handedness',
                    options=['BOTH', 'RIGHT', 'LEFT'],
                    value=col.handedness,
                    on_change=on_handedness_change,
                ).classes('w-60').props('outlined')

                count_label = ui.label(f'{len(filter_matches(col))} matches in this column').classes('text-xs text-gray-400')
                ui.button('VIEW MATCHES', on_click=lambda col=col: open_matches_dialog(col))
                ui.button(icon='close', on_click=lambda i=i: remove_column(i)).props('round color=red size=10px')

    columns_view()

    spinner_row = ui.row().classes('w-full justify-center mt-2')
    spinner_row.visible = False
    with spinner_row:
        ui.spinner('dots', size='xl')

    async def create_report():
        if not all(col.players for col in columns):
            ui.notify('PLEASE SELECT AT LEAST ONE PLAYER FOR EVERY COLUMN', position='center', type='negative')
            return
        payload = []
        for col in columns:
            available = sorted({m['match_id'] for m in filter_matches(col)})
            if col.selected_matches is not None:
                available = [m for m in available if m in col.selected_matches]
            if not available:
                ui.notify(f'NO MATCHES LEFT IN COLUMN "{display_name(col)}"', position='center', type='negative')
                return
            payload.append({'players': col.players, 'matches': available, 'name': display_name(col)})

        spinner_row.visible = True
        create_button.disable()
        try:
            title = ' / '.join(dict.fromkeys(p for col in columns for p in col.players))[:60]
            # io_bound (thread) instead of cpu_bound: forking a second Python
            # process doubles memory and OOMs small Render instances.
            datas = await run.io_bound(compute_columns, payload)
            file_name = await run.io_bound(create_shot_evolution, uuid.uuid4().hex[:12], title, datas)
            ui.navigate.to(f'/reports/{file_name}', new_tab=True)
        finally:
            spinner_row.visible = False
            create_button.enable()

    create_button = ui.button('CREATE SHOT EVOLUTION REPORT', on_click=create_report).classes('mx-auto mt-6')
    ui.space()


if __name__ in {'__main__', '__mp_main__'}:
    load_leaderboard()  # warm the cache before serving so the first report is fast
    ui.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080)),
        title='GSA Shot Evolution',
        favicon=FAVICON,
        dark=True,
        reload=False,
        show=False,
    )
