"""
Module to test the pv model
"""

import numpy as np
import unittest
import sys
sys.path.insert(0,"/Users/cassidyquigley/desktop/solarsizer/solarsizer/pysam")
                
from pysam.pysam_utils import pvmodel

print(sys.path)
class TestPVModel(unittest.TestCase):

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        pvmodel.execute_pvmodel(5, 6, n_inverters=10)
        return
      
# One shot: In this case, you call the code under test with arguments for which you know the expected result
#   1. We could do this with the above smoke test or create another set up where we know the output

# Edge test: The code under test is invoked with arguments that should cause an exception, and you evaluate if the expected exception occurrs
#   1. input a load profile that is way too high, still need to handle this case in psyam_model.py
#   2. Lat,Lon over ocean? 

# Pattern test: Based on your knowledge of the *calculation* (not implementation) of the code under test, you construct a suite of test cases for which the results are known or there are known patterns in these results that are used to evaluate the results returned
#   1. run the code twice, one load profile is larger than the other, compare outputs 
#   2. same thing but with locations, choose one location that has much more irradiance 
