"""
Module to test the pv model
"""

import numpy as np
import unittest

from pysam.pysam_utils import pvmodel


class TestPVModel(unittest.TestCase):

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        pvmodel.execute_pvmodel(5, 6, n_inverters=10)
        return
