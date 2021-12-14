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
    html.H1(
        children='Hello, welcome to solarGRID',
        style={
            'width': '50%',
            'textAlign': 'center',
            'float': 'left',
            'display': 'inline-block',
        }
    ),

     html.Img(
        src='/assets/SolarSizerLogo.png',
        style={
            'width': '49%',
            'height': '30vh', 
            'float': 'right',
            'display': 'inline-block',
            },
        ),

    html.H2(
        children='A web application for assisting with solar projects', 
        style={
        'textAlign': 'center',
        }
    ),

    html.Br(),

    # input div
    html.Div([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    html.Div([
                    html.Label('Enter latitude and longitude below:'),
                    html.Br(),
                    
                    html.Label('Latitude (in degrees):'),
                    dcc.Input(id='lat', type='number'),
                    html.Br(),
                    
                    html.Label('Longitude (in degrees):'),
                    dcc.Input(id='lon', type='number'),
                    html.Br(),
                    html.Div('Note: chosen point must be in the United States', style={'color': 'gray', 'fontSize': 14}),
                ],
                style={'width': '49%', 'display': 'inline-block'}
                ),
                ]),
                
                html.Br(),
                
                dbc.Row([
                    html.Div([
                    html.Label('Upload a load profile:'),
                    html.Br(),
                        
                    dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select File')
                    ]),
                    style={
                        'width': '90%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False),
                    html.Div('Note: load profile must be in csv format, see template in data directory', style={'color': 'gray', 'fontSize': 14}),
                    ],
                # style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
                ),], 
                justify='center',
                ),
            ])
        ],
        style={'display': 'inline-block',
            'width': '49%',
            'text-align': 'center',
            'color':'black',
            'background-color': 'thistle'},
        outline=True),
    ],
    
    style={
        'padding': '10px 5px'
    }
    ),

    html.Br(),

    html.Br(),

    html.Div(id="output"),
    
    
    html.Div(id='output-data-upload'),
    
    html.Button('Run Model', id='btn-nclicks-1', n_clicks=0),

    html.Div(id='model-status'),
    
])


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
        
        print('contents', contents)
        print(type(contents))
        
        # decode output from file upload
        _, content_string = contents.split(',')

        decoded_b64 = base64.b64decode(content_string)
        print('decoded_b64', decoded_b64)
        print(type(decoded_b64)) 
        
        # check that type csv
        if filename.endswith('.csv'):

            decoded_csv = io.StringIO(decoded_b64.decode('utf-8'))
            print('decoded_csv', decoded_csv)
            print(type(decoded_csv))

            # convert to txt
            convert_load_profile.create_load_txt(decoded_csv, filename)

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
        msg = 'Click button to run model once the lat and lon are inputted and a load profilee is uploaded as a .csv'
        return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
