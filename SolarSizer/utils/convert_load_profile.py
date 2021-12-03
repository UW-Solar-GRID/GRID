import base64
import datetime
import io

from decimal import *
import pandas as pd
import numpy as np

def create_load_txt(contents, filename, date):
    content_type, content_string = contents.split(',')

    lines = []
    nums = []
    decoded = base64.b64decode(content_string)

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
        
    # get load row
    load_row_day = df.iloc[-2]
    
    # get rid of nans and get values
    load_row_day = load_row_day.dropna()
    load_row_day = np.asarray(load_row_day.values)
    
    # drop peak and total load
    load_row_day = load_row_day[1:-1]
    
    # assuming constant load for each day, create load profile for year
    load_row_year = [load_row_day]*365
    
    np.savetxt('data/load_profile_example.txt', load_row_year)

    return load_row_year