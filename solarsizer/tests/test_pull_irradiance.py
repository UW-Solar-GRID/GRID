"""
Module to test pull_irradiance
"""

import sys

import numpy as np
import unittest
                
from solarsizer.utils import pull_irradiance

class Testpullirradiance(unittest.TestCase):

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        pull_irradiance.create_irradiance_file(30, -76, 2012)
    def test_oneshot(self):
        """
        One shot test
        """
        pull_irradiance.create_irradiance_file(45, -122, 2000)
        return
    def test_invalid_lat_lon_year(self):
        """
        Edge test to make sure the function throws an error
        Should says invalue inputs: lat, lon or year
        We can probably just let these errors be caught by one error unless we know the bounds of the data and want to catch them before calling the API
        """
        with self.assertRaises(AssertionError):
            pull_irradiance.create_irradiance_file(122, -222, 2000)
        return
