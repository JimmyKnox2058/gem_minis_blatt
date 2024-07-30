"""
Dash page to show pre-made word clouds from a pickle file.
"""
import pickle
from dash import html, dcc, callback, Output, Input
import dash


pickle_path ="./data/pickle_jar/"

with open(pickle_path+"topic_clouds.pickle","rb") as file:
    clouds = pickle.load(file)
    
dash.register_page(__name__)


layout = html.Div([
    html.H1(children='Topic Clouds', style={'textAlign':'center',
                                           'object-fit' : 'scale-down'}),
    html.Img(src=clouds[0],
             id='topic_cloud',
             style={'object-fit' : 'contain',
                    'width': '60%',
                    'height': '60%',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto'}),
    dcc.Dropdown(list(range(len(clouds))), value=0,
                 id='dropdown-selection_topic')
])

@callback(
    Output('topic_cloud', 'src'),
    Input('dropdown-selection_topic', 'value')
)
def update_image(value:int)-> 'PIL.Image.Image':
    """Returns the image for the selected value.

    Args:
        value (int): Entry of the dropdown field.

    Returns:
        'PIL.Image.Image': Image for the selected value.
    """
    return clouds[value]