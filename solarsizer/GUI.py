"""

Creates GUI with functionality to input latitude, longitude, and a csv file.
These user inputted values are run through the PySAM model.

Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
"""

import dash
from dash.dependencies import Input, Output, State
from dash import callback_context, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

import urllib.request
import os

from pysam import pysam_model
#from utils import parse_load_profile as plp
from utils import pull_irradiance
from utils import convert_load_profile

global_lat = None
global_lon = None
global_list_of_contents = None


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
                html.Div([
                    html.Label('Enter latitude and longitude below:'),
                    html.Br(),
                    
                    html.Label('Latitude (in degrees):'),
                    dcc.Input(id='lat', type='number'),
                    html.Br(),
                    
                    html.Label('Longitude (in degrees):'),
                    dcc.Input(id='lon', type='number'),
                ],
                style={'width': '49%', 'display': 'inline-block'}
                ),
            
                html.Div([
                    dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True),],
                style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
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
    
    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),

    html.Div(id='container-button-timestamp')
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
def load_profile_update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        global_list_of_contents = list_of_contents
        [convert_load_profile.create_load_txt(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        print('button clicked')
        msg = 'Button 1 was most recently clicked'
        
        model_output = pysam_model.pysam_model()
        print(model_output)
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
