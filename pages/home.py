# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:54:25 2024

@author: Thomas
"""

import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
])