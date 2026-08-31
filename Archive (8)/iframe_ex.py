from nicegui import ui

#ui.label('VIDEO PAGE')
ui.html('''<iframe src="https://app.goldensetanalytics.com/shotsview" width="100%" height="1000px" style="clip-path: inset(10% 0 0 0); border:none;"></iframe>''').classes('w-full')
#<iframe src="YOUR_APP_URL" style="clip-path: inset(10% 0 0 0); height: 100vh; width: 100%; border: none;"></iframe>

ui.run()