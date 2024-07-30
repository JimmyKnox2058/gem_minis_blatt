#import time 
import pickle
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash


pickle_path ="./data/pickle_jar/"

with open(pickle_path+"absoluteYearly.pickle","rb") as file:
    yearly_total = pickle.load(file).sum(axis=1)
    
dash.register_page(__name__)



layout = html.Div([
    html.H1(children='Total words', style={'textAlign':'center'}),
    dcc.Graph(id='totalGraph', figure=px.line(yearly_total, x=yearly_total.index, y=yearly_total.values))
])


