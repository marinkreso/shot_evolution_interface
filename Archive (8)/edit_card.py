import random
from time import sleep
from nicegui import ui

nodes: dict[str, list[dict]] = {}
default_columns = [
    {'name': 'value_name', 'label': 'Value name', 'field': 'value_name', 'align': 'left'},
    {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left'},
]


@ui.page('/node/{node_id}')
def node_page(node_id: str):
    ui.label('This is the more information page of node: ' + node_id)


@ui.refreshable
def node_grid() -> None:
    with ui.grid(columns=15, rows=1).classes('w-full h-full'):
        for node_id, node_items in nodes.items():
            with ui.card().classes('col-span-2 gap-0'):
                ui.link('Node ID: ' + node_id, target='/node/' + node_id, new_tab=True).classes('mx-auto text-bold').style('cursor: pointer; color:#000000').classes(
                    '!no-underline mx-auto')
                table = ui.table(columns=default_columns, rows=[], row_key='value_name').classes('w-full')
                for item in node_items:
                    for k, v in item.items():
                        table.add_rows({'value_name': k, 'value': v})


def add_node(node_id: str) -> None:
    nodes.update({node_id: [
        {'Node type': ''},
        {'Node UID': ''},
        {'Node last seen': ''},
    ]})
    node_grid.refresh()


def add_information_node(node_id: str) -> None:
    valuename_to_add = 'yet_another_item' + str(random.randint(0, 100))
    value_to_add = random.randint(0, 100)
    nodes[node_id].append({valuename_to_add: value_to_add})
    node_grid.refresh()


def update_information_node(node_id: str, node_valuename_to_update: str, node_value_to_update: str) -> None:
    for node_values in nodes[node_id]:
        node_values.update((k, str(node_value_to_update)) for k, v in node_values.items() if k == node_valuename_to_update)
    node_grid.refresh()


def remove_node(node_id: str) -> None:
    del nodes[node_id]
    node_grid.refresh()


@ui.page('/')
def gui():
    node_grid()
    with ui.grid(columns=4, rows=3).classes('w-full'):
        node_id = ui.input('node id', value='x')
        node_valuename_to_update = ui.select(['Node type', 'Node UID', 'Node last seen'], value='Node type', label='Value to update').classes('w-40')
        node_value_to_update = ui.input('value', value='123')

        ui.button('add node', on_click=lambda: add_node(node_id.value))
        ui.button('add information to node', on_click=lambda: add_information_node(node_id.value))
        ui.button('update information of node', on_click=lambda: update_information_node(node_id.value, node_valuename_to_update.value, node_value_to_update.value))
        ui.button('remove node', on_click=lambda: remove_node(node_id.value))


for i in range(20):
    add_node(str(i))
    sleep(0.1)

ui.run(reload=False)