"""
Module to test convert_load_profile
"""

import os
import sys

import numpy as np
import unittest
                
from solarsizer.utils import convert_load_profile


class Testconvertloadprofile(unittest.TestCase):

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        convert_load_profile.create_load_txt(contents, filename, date)
    def test_oneshot(self):
        """
        One shot test
        """
        convert_load_profile.create_load_txt(contents, filename, date)
        return
    def test_data_type(self):
        """
        Edge test to make sure the function throws an error
        when the data type in not floats or int
        """
        contents = # give it string
        filename = 'load_profile_template.txt'
        date = '2021-12-01'
        
        with self.assertRaises(TypeError):
            convert_load_profile.create_load_txt(contents, filename, date)
        return
    def test_wrong_len_txt_created(self):
        """
        Edge test to make sure the function throws an error
        when the txt created is the wrong length
        """
        contents = # need to make test data
        filename = 'load_profile_template.csv'
        date = '2021-12-01'
        
        with self.assertRaises(TypeError):
            convert_load_profile.create_load_txt(contents, filename, date)
        return
    def test_NaN_in_txt(self):
        """
        Edge test to make sure the function throws an error
        when the txt created is the wrong length
        """
        contents = # need to make test data
        filename = 'load_profile_template.csv'
        date = '2021-12-01'
        
        with self.assertRaises(TypeError):
            convert_load_profile.create_load_txt(contents, filename, date)
        return
    