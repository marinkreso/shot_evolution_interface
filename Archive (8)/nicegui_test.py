from nicegui import ui

class NumberOfElements:
    def __init__(self):
        self.number = 1
        self.sel_matches = []
        self.report_names = []

noe = NumberOfElements()
report_toggle = ui.toggle({1: '1', 2: '2', 3: '3'}, value=1, on_change=lambda e: button_view.refresh(e.value)).classes('mx-auto')#.bind_value(noe, 'number')


@ui.refreshable
def report_view(matches, report_names):
    print('INSIDE REPORT VIEW', matches)
    for m, r in zip(matches, report_names):
        ui.label(m + '-' + r).classes('mx-auto')

def dialog_action(this_dialog, i, buttonopener):
    print('INSIDE DIALOG ACTION BEW', i, this_dialog)
    noe.sel_matches[i] = 'Number ' + str(i)
    this_dialog.close()
    buttonopener.props("color=green") 

def set_report_name(value, i):
    noe.report_names[i] = value


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
    noe.report_names = ['']*x
    print('INSIDE BUTTON VIEW', x, noe.sel_matches)
    dialogs = []
    with ui.row().classes('mx-auto'):
        for i in range(x):
            with ui.column():
                ui.input(label=f'Enter Report Name', placeholder=f'Enter Report Name', on_change=lambda e, i=i: set_report_name(e.value, i))
                buttonopener = ui.button(f'REPORT {i}').classes('mx-auto')
            with ui.dialog() as dialog, ui.card():
                ui.label(f'Label {i}!')
                ui.button(f'Close me {i}', on_click=lambda i=i, buttonopener=buttonopener: dialog_action(dialogs[i], i, buttonopener))
            dialogs.append(dialog)
            buttonopener.on('click', dialog.open)
            
    print('DIALOGS: ', dialogs)


button_view(1)
ui.button(f'Generate report', on_click=lambda e: report_view.refresh(noe.sel_matches, noe.report_names)).classes('mx-auto')
report_view([], [])
ui.run()