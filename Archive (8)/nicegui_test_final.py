from nicegui import ui

class NumberOfElements:
    def __init__(self):
        self.number = 1
        self.sel_matches = []

noe = NumberOfElements()
report_toggle = ui.toggle({1: '1', 2: '2', 3: '3'}, value=1, on_change=lambda e: button_view.refresh(e.value)).classes('mx-auto')#.bind_value(noe, 'number')


@ui.refreshable
def report_view(matches):
    print('INSIDE REPORT VIEW', matches)
    for m in matches:
        ui.label(m).classes('mx-auto')

def dialog_action(this_dialog, i):
    print('INSIDE DIALOG ACTION BEW', i, this_dialog)
    noe.sel_matches[i] = 'Number ' + str(i)
    this_dialog.close()

class EditableButton:

    def __init__(self) -> None:
        super().__init__()
        

    def add_button(self, dialog, i) -> None:
        with self:  # Make sure to use the context of the card
            ui.button(f'REPORT {i}!', on_click=dialog.open)

@ui.refreshable
def button_view(x):
    EditableButton
    noe.number = x
    noe.sel_matches = [0]*x
    print('INSIDE BUTTON VIEW', x, noe.sel_matches)
    dialogs = []
    with ui.row().classes('mx-auto'):
        for i in range(x):
            with ui.dialog() as dialog, ui.card():
                ui.label(f'Label {i}!')
                ui.button(f'Close me {i}', on_click=lambda i=i: dialog_action(dialogs[i], i))
            dialogs.append(dialog)
            ui.button(f'REPORT {i}!', on_click=dialog.open)
    print('DIALOGS: ', dialogs)


button_view(1)
ui.button(f'Generate report', on_click=lambda e: report_view.refresh(noe.sel_matches)).classes('mx-auto')
report_view([])
ui.run()