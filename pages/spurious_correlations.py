import pickle
from dash import html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash

pickle_path ="./data/pickle_jar/"

with open(pickle_path + "statsTotal.pickle","rb") as file:
    total_df = pickle.load(file)
    
with open(pickle_path + "relativeYearly.pickle","rb") as file:
    rel_freq_year = pickle.load(file)
    
with open(pickle_path + "interesting_words.pickle","rb") as file:
    interesting_words = pickle.load(file)
    
rel_freq_year = rel_freq_year.reindex(sorted(rel_freq_year.columns), axis=1)
interesting_words=interesting_words.sort_values()
total_df = total_df.sort_index()
interesting_total_df = total_df.loc[interesting_words]
interesting_rel_df = rel_freq_year[interesting_words]

dash.register_page(__name__)


layout = html.Div([
    html.H1(children='Spurious correlations', style={'textAlign':'center'}),
    html.H2(children='Finanzierung der Bundeswehr', style={'textAlign':'center'}),
    dcc.Graph(figure=px.line(rel_freq_year[['metzgerei','bundeswehrkasse']],
                             x=rel_freq_year.index,
                             y=['metzgerei','bundeswehrkasse'])),
    html.H2(children='Neue Verbrechen', style={'textAlign':'center'}),
    dcc.Graph(figure=px.line(rel_freq_year[['arithmetisch','polizeiangelegenheit']],
                             x=rel_freq_year.index,
                             y=['arithmetisch','polizeiangelegenheit'])),
    html.H2(children='Studentenfutter', style={'textAlign':'center'}),
    dcc.Graph(figure=px.line(rel_freq_year[['speiseeis','selbststudium']],
                             x=rel_freq_year.index,
                             y=['speiseeis','selbststudium'])),
    html.H2(children='Helmuts sind schlechte Enkel', style={'textAlign':'center'}),
    dcc.Graph(figure=px.line(rel_freq_year[['grosselter','verpfändung']],
                             x=rel_freq_year.index,
                             y=['grosselter','verpfändung']))
])
