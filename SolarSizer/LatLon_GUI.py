"""

Creates GUI with functionality to input latitude and longitude.

These user inputted values are run through a FakeSAM model that just
multiplies them by two and then returns them as outputs in the GUI.

"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#import datetime

import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
#import plotly.express as px
import pandas as pd

import urllib.request
import os

import fake_SAM
from SolarArrayModel.pull_irradiance.pull_irradiance import create_irradiance_file

app = dash.Dash(__name__)

colors = {
    'background': '#777777',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello, welcome to solarGRID',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='A web application for assisting with solar projects', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Br(),

    html.Label('Enter latitude and longitude below:', style={'color': colors['text']

    }),

    html.Br(),

    html.Br(),

    html.Label('Latitude (in degrees):', style={'color': colors['text']

    }),

    dcc.Input(id='lat', type='number'),

    html.Br(),

    html.Label('Longitude (in degrees):', style={'color': colors['text']

    }),

    dcc.Input(id='lon', type='number'),

    html.Br(),

    html.Br(),

    html.Div(id="output"),

#    html.Label('Upload a load profile below:', style={'color': colors['text']
#
#    }),
#
#
#    dcc.Upload(
#        id='upload-csv',
#        children=html.Div([
#            'Drag and Drop or ',
#            html.A('Select csv Files')
#        ]),
#        style={
#            'width': '100%',
#            'height': '60px',
#            'lineHeight': '60px',
#            'borderWidth': '1px',
#            'borderStyle': 'dashed',
#            'borderRadius': '5px',
#            'textAlign': 'center',
#            'margin': '10px'
#        },
#        # Allow multiple files to be uploaded
#        multiple=True
#    ),
#    html.Div(id='output-csv-upload'),
])

#def parse_contents(contents, filename, date):
#    return html.Div([
#        html.H5(filename),
#        html.H6(datetime.datetime.fromtimestamp(date)),
#        html.Hr(),
#        html.Div('Raw Content'),
#        html.Pre(contents[0:200] + '...', style={
#            'whiteSpace': 'pre-wrap',
#            'wordBreak': 'break-all'
#        })
#    ])
#
#@app.callback(Output('output-csv-upload', 'children'),
#              Input('upload-csv', 'contents'),
#              State('upload-csv', 'filename'),
#              State('upload-csv', 'last_modified'))
#def update_output(list_of_contents, list_of_names, list_of_dates):
#    if list_of_contents is not None:
#        children = [
#            parse_contents(c, n, d) for c, n, d in
#            zip(list_of_contents, list_of_names, list_of_dates)]
#        return children


@app.callback(Output('output', 'children'),
              Input('lat', 'value'),
              Input('lon', 'value'))

def update_output(lat, lon):
    """
    Updates output with input values run through FakeSAM model.
    """

    if lat is not None and lon is not None:
        create_irradiance_file(lat,lon,2000)
        nlat, nlon = fake_SAM.twice_lat_lon(lat, lon)
        return u'Lat: {}, Lon: {}'.format(nlat, nlon)
    else:
        pass
                
if __name__ == '__main__':
    app.run_server(debug=True)
