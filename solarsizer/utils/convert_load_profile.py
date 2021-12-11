"""
Module that contains function to convert GUI input file to a dataframe
Saves the dataframe to a txt file within the data directory

We assume the input file is csv format, though we include code for excel and txt inputs

TO DO: Remove date input, remove df returns

"""

import base64
import io

from decimal import Decimal
import pandas as pd
import numpy as np

def create_load_txt(contents, filename, date):
    """
    Load in GUI input file and returns a dataframe to be used in the PySAM model
    The dataframe is saved to a txt file named 'user_load_profile.txt'
    This txt file is saved within the data directory

    Parameters:
        contents (list):A list containing the file contents
        filename (str):Filename of the input data
        date (str):Date of data contained within file

    Returns:
        load_row_year (df):Dataframe containing the yearly load profile data

    """
    _, content_string = contents.split(',')

    lines = []
    nums = []
    decoded = base64.b64decode(content_string)

    if 'txt' in filename:
        data = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))

        lines = decoded.decode('utf-8').splitlines()
        lines.pop(0)
        for i in range(len(lines)):
            nums.append(Decimal(lines[i]))
      ##      print(nums[i])
      ##  print(len(lines))


    elif 'csv' in filename:
        # Assume that the user uploaded a CSV file
        data = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))

    # get load row
    load_row_day = data.iloc[-2]

    # get rid of nans and get values
    load_row_day = load_row_day.dropna()
    load_row_day = load_row_day.values

    # drop peak and total load
    load_row_day = load_row_day[1:-1]

    # assuming constant load for each day, create load profile for year
    load_row_year = np.array([load_row_day]*365)
    load_row_year = load_row_year.astype(dtype='float')
    load_row_year = np.reshape(load_row_year, (365*24))

    load_row_year_kw = load_row_year/1000 # converts from watts to kW

    ##print(load_row_year_kw.shape)

    np.savetxt('data/user_load_profile.txt', load_row_year_kw, delimiter=' ')

    return load_row_year
