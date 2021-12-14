"""
Module to test convert_load_profile
"""

import os
import sys
import unittest

import numpy as np
import pandas as pd
                
from solarsizer.utils import convert_load_profile


class Testconvertloadprofile(unittest.TestCase):

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        data = pd.read_csv(r'test_data/load_profile_smoke.csv')
        
        convert_load_profile.create_load_txt(data)
    def test_oneshot(self):
        """
        One shot test
        """
        data = pd.read_csv(r'test_data/load_profile_one_shot.csv')
        
        convert_load_profile.create_load_txt(data)
        
        # ADD CODE to compare txts created to correct txt
    def test_wrong_len_load_row_day(self):
        """
        Edge test to make sure the function throws an error
        when load_row_day does not have a length of 24
        """
        data = pd.read_csv(r'test_data/load_profile_too_many_hours.csv')

        with self.assertRaises(ValueError):
            convert_load_profile.create_load_txt(data)
    def test_not_values_load_row_day(self):
        """
        Edge test to make sure the function throws an error
        when load_row_day is not floats or ints
        """
        data = pd.read_csv(r'test_data/load_profile_some_loads_are_strings.csv')

        with self.assertRaises(TypeError):
            convert_load_profile.create_load_txt(data)
        return
    def test_NaN_in_load(self):
        """
        Edge test to make sure the function throws an error
        when Nans are in the load profile
        """
        data = # need to make test data
        
        with self.assertRaises(ValueError):
            convert_load_profile.create_load_txt(data)
        return
    