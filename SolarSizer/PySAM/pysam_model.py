#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import pandas as pd
import PySAM.Pvsamv1 as pv
import matplotlib.pyplot as plt
import urllib.request
from pysam_utils import pvmodel

def pysam_model():

    ## Running multiple scenarios

    # Now, we will evaluate multiple scenarios - we will look at a range of modules numbers and a range of strings to find minimum system requirements that satisfy maximum uptime

    pvmodels_param_dict = []
    pvmodels = []

    for m in range(2,8): # m is no of modules    
        for n in range(4,15): # n is no of strings        
           # if m*n >=30:\n#             
            l.append([m,n])           
            pvmodels_param_dict.append({"modules_per_string" : m, "number_of_strings" : n})            
            z = pvmodel.execute_pvmodel(m,n, n_inverters=5)           
            pvmodels.append(z)

    len(pvmodels)

    pvmodels[0]

    uptime_percent = []

    for i in range(len(pvmodels)):
        uptime_hours = np.count_nonzero(
            (np.array(pvmodels[i].Outputs.system_to_load) + 
             np.array(pvmodels[i].Outputs.batt_to_load) - 
             np.tile(our_load_profile, 25)  # repeat load profile for 25 years
            ) == 0 
        )

        uptime_percent.append(uptime_hours/(365 * 24 * 25))

    print("UPTIME", uptime_percent)
    print("PARAMS", pvmodels_param_dict)

    (np.array(pvmodels[0].Outputs.system_to_load) + np.array(pvmodels[0].Outputs.batt_to_load) - np.tile(our_load_profile, 25))[-24:]
    
    return 'place holder text'
