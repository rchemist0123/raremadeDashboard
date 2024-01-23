from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import layout
import callbacks
import pandas as pd


external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts = external_script)
server = app.server
app.layout = layout.create_layout()
app.scripts.config.serve_locally = True
    
if __name__ == '__main__':
    app.run(debug = True)
