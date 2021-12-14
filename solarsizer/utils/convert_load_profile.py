"""
Module that contains function to convert GUI input file to a dataframe
Saves the dataframe to a txt file within the data directory

We assume the input file is csv format, though we include code for excel and txt inputs

TO DO: Remove date input, remove df returns

"""

import numpy as np
import pandas as pd

def create_load_txt(decoded_csv):
    """
    Loads in decoded load profile from GUI and converts to dataframe. Then gets the row with the hourly load
    and saves as a txt file to be used in the PySAM model. The txt file contains the daily load profile repeated
    for a year and is named 'user_load_profile.txt'. This txt file is saved within the data directory.

    Parameters:
        decoded_csv (io.StringIO object):An object containing the file contents

    """

    # convert to pandas dataframe
    data = pd.read_csv(decoded_csv)
    print('data', data)
    print(type(data))

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


    np.savetxt('data/user_load_profile.txt', load_row_year_kw, delimiter=' ')

