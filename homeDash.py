# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:49:06 2024

@author: Thomas
"""

import dash
from dash import Dash, html, dcc
import os
from pathlib import Path
BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)