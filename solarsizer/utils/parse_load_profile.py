import base64
import datetime
import io

from dash import dcc
from dash import html
from decimal import *
import pandas as pd
from dash import dash_table

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    lines = []
    nums = []
    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

            lines = decoded.decode('utf-8').splitlines()
            lines.pop(0)
            for i in range(len(lines)):
                nums.append(Decimal(lines[i]))
                print(nums[i])
            print(len(lines))
        elif 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(str(type(contents))),
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.H6("Shape: {}".format(df.shape)),
        html.H6("List size: {}".format(len(lines))),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
