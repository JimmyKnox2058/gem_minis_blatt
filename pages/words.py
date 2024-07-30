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
    html.H1(children='Pick some words:'),
    dcc.Checklist(options=['Interesting words'], id='interest'),
    dcc.Dropdown(options=rel_freq_year.columns, value=total_df.index[0],
                 id='dropdown-selection',multi=True),
    html.H1(children='Aggregated data', style={'textAlign':'center'}),
    dash_table.DataTable(id='total_table'),
    html.H1(children='Correlations', style={'textAlign':'center'}),
    dash_table.DataTable(id='cor_table'), 
    html.H1(children='Relative Frequencies', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content',
              figure=px.line(rel_freq_year[rel_freq_year.columns[0]],
                             x=rel_freq_year.index,
                             y=rel_freq_year.columns[0]))
])

@callback(
    Output('graph-content', 'figure'),
    Output('total_table', 'data'),
    Output('cor_table', 'data'),
    Input('dropdown-selection', 'value')
)
def update_data(value:list[str]) -> ('go.figure', dict, dict):
    """Updates the graph and the tables when dropdown selection is changed.

    Args:
        value (list[str]): Selected list of words.

    Returns:
        (go.figure, dict, dict): graph of frequencies of words and dictionaries
            for both the stats for those words and their correlations
    """
    dff = rel_freq_year[value] 
    cor = pd.DataFrame(rel_freq_year[value]).corr().reset_index(names="")
    return (px.line(dff, x=rel_freq_year.index, y=value),
            total_df.loc[value].reset_index().to_dict('records'),
            cor.to_dict('records')
            )


@callback(
    Output('dropdown-selection', 'options'),
    Input('interest', 'value')
)
def update_word_list(value: list) -> pd.Index:
    """Updates the dropdown selection, restricting either to interesting words
    or expanding to all words.

    Args:
        value (list): Either list containing the single string 'Interesting words' or None.

    Returns:
        pd.Index: Index with either all words or a restricted amount of interesting words.
    """
    if not value==None and 'Interesting words' in value:
        return interesting_rel_df.columns
    return rel_freq_year.columns
    