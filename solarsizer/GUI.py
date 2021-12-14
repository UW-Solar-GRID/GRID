"""

Creates GUI with functionality to input latitude, longitude, and a csv file.
These user inputted values are run through the PySAM model.

Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
"""

import dash
from dash.dependencies import Input, Output, State
from dash import callback_context, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

import urllib.request
import os
import base64
import io

from decimal import Decimal
from pysam import pysam_model
#from utils import parse_load_profile as plp
from utils import pull_irradiance
from utils import convert_load_profile

global_lat = None
global_lon = None
global_contents = None

app = dash.Dash(__name__)

app.layout = html.Div( children=[
    
    #  Logo and Header
    dbc.Row([
        dbc.Col(
            [html.Img(
            src='/assets/SolarSizerLogo.png',
            style={
                'width': '25%',
                'height': '13vh', 
                'float': 'left',
                'display': 'inline-block',
                },
            ),],
            ),
        dbc.Col([
            dbc.Row(
                [html.Div(
                children='Solar Sizer',
                style={
                    'textAlign': 'left',
                    'fontSize': 55,
                }
            ),],
            ),
            dbc.Row(
                [html.Div(
                children='A web application for planning off-grid solar projects', 
                style={
                    'textAlign': 'left',
                    'fontSize': 24,
                }
                ),],
                ),
            ],
            style={
                'height': '25vh',
                'width': '70%',
                'float': 'right',
                }),
        ],
            style={
                'height': '16vh',
            }
        ),
    
    # Separate bar
    dbc.Row(
        style={
            'height': '5vh',
            'background-color': 'cornflowerblue'
        }
    ),
    
    # Main block
    dbc.Row([
        html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label('Try'),
        
        # Row for input and output
        dbc.Row([
            # Scrolling output, floating to the right
            dbc.Col(
                children=[
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Label('Try'),
                    dbc.Row([html.Div(id='model-status')]),
                    ],
                style={
                    'width': '64%',
                    'height': '68vh',
                    'float': 'right',
                    'background-color': 'lightgreen',
                    'overflow': 'scroll',
                    'borderRadius': '3px',
                    'padding-top': '20px',
                    },
            ),
            
            # Input card, floating to the left
            dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Div([
                        html.Div('Enter latitude and longitude below:', style={'fontSize': 24,}),
                        html.Div('Note: chosen point must be in the United States', style={'color': 'gray', 'fontSize': 14, 'padding-bottom': '3px',}),
                        
                        html.Label('Latitude (in degrees):'),
                        dcc.Input(id='lat', type='number'),
                        html.Br(),
                        
                        html.Label('Longitude (in degrees):'),
                        dcc.Input(id='lon', type='number'),
                        html.Br(), 
                    ],
                    style={'width': '78%', 'display': 'inline-block'}
                    ),
                    ]),
                    
                    html.Br(),
                    html.Br(),
                    
                    dbc.Row([
                        html.Div('Upload a load profile:', style={'fontSize': 24,}),
                        dbc.Row(
                            [
                                html.Center([
                                    dbc.Row([html.Div('Note: load profile must be in csv format, see template in data directory', style={'color': 'gray', 'fontSize': 14}),]),
                                    dcc.Upload(
                                        id='upload-data',
                                        children=[
                                            html.Div(
                                                ['Drag and Drop or Select File',], 
                                                style={
                                                    'vertical-align': 'top'
                                                    },
                                                )
                                            ],
                                        style={
                                            'width': '80%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '2px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'margin': '10px',
                                            'vertical-align': 'top'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=False,
                                    ),
                                ])
                            ]
                        ),
                        
                        ], 
                    style={
                        'vertical-align': 'top'
                        },
                    justify='center',
                    ),
                    
                    html.Br(),
                    html.Br(),
                    
                    dbc.Row([
                        html.Button('Run', id='btn-nclicks-1', n_clicks=0, 
                                    style={
                                        'width': '80%',
                                        'height': '60px',
                                        'borderWidth': '2px',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'color': 'grey',
                                    },
                                    ),
                    ],
                    )
                ],
                style={
                    'padding-top': '20px',
                    'padding-right': '3px',
                    'padding-bottom': '5px',
                    'padding-left': '8px',
                }
                )
            ],
            style={
                'display': 'inline-block',
                'height': '54vh',
                'width': '35%',
                'float': 'left',
                'text-align': 'center',
                'color':'black',
                'background-color': 'thistle',
                'borderRadius': '3px',
                },
            ),
        ],
        
        style={
            'padding': '5px 5px',
        }
        ),
        ],
                
        style={
            'width': '100%',
            'height': '70vh',
            'overflow': 'scroll',
            'background-color': 'yellow',
        }
        ),
    ],
    style={
            'width': '100%',
            'height': '70vh',
            'overflow': 'scroll',
            'background-color': 'gray',
        }        
    
    ),

    html.Br(),

    html.Br(),

    html.Div(id="output"),
    
    html.Div(id='output-data-upload'),
],
style={
    'padding-top': '30px',
    'padding-right': '150px',
    'padding-bottom': '10px',
    'padding-left': '150px',
}
)


@app.callback(Output('output', 'children'),
              Input('lat', 'value'),
              Input('lon', 'value'))

def update_output(lat, lon):
    """
    Updates output with input values run through FakeSAM model.
    """

    if lat is not None and lon is not None:
        global_lat = lat
        global_lon = lon
        print('global_lat', global_lat)
        print('global_lon', global_lon)
        
        pull_irradiance.create_irradiance_file(lat,lon,2000) # may want to turn this off when testing because will max out request from API rate. Also might want to see about using average irradiance from NREL instead of from a set year.

    else:
        pass


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def load_profile_update_output(contents, filename, last_modified):
    if contents is not None:
        global_contents = contents
        
        # decode output from file upload
        _, content_string = contents.split(',')

        decoded_b64 = base64.b64decode(content_string)
        
        # check that type csv
        if filename.endswith('.csv'):

            decoded_csv = io.StringIO(decoded_b64.decode('utf-8'))
            
            # convert to pandas dataframe
            data = pd.read_csv(decoded_csv)

            # convert to txt
            convert_load_profile.create_load_txt(data)

        else:
            raise TypeError('Load profile must be a csv file')
        
    else:
        pass


# output is n*4cols data frame
@app.callback(
    Output('model-status', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    test_df = pd.DataFrame()
    if 'btn-nclicks-1' in changed_id:
        print('button clicked')
        
        model_output = pysam_model.pysam_model()
        test_df = model_output
        print(model_output)
        print('test_df++++++++', test_df)
        
        msg = 'Model running'
        return html.Div(msg)
    
    elif not test_df.empty:
        msg = 'Model finished running, result below:'
        return [html.Div(msg), 
            
            html.Div([
                dash_table.DataTable(
                    data=test_df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in test_df.columns]
                ),
                html.Hr(),])
                ]
    else:
        msg = "placeholder"
        # msg = 'Click button to run model once the lat and lon are inputted and a .csv load profile is uploaded'
        return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
