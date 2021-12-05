#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import pandas as pd
import PySAM.Pvsamv1 as pv
import matplotlib.pyplot as plt
import urllib.request
from pysam.pysam_utils import pvmodel

def pysam_model():

    ## Running single scenario to get an estimate of the array size 
    pv_guess = pvmodel.execute_pvmodel(2, 1, n_inverters=1)
    uptime_hours = np.count_nonzero(
        (np.array(pvmodel.Outputs.system_to_load) + 
         np.array(pvmodel.Outputs.batt_to_load) - 
         np.tile(our_load_profile, 25)  # repeat load profile for 25 years
        ) == 0 
    )
    panel_number_estimate = (1/(uptime_hours/(365 * 24 * 25)))/1.5 #, uptime_hours  # percent uptime for 25 years


    # Now, we will evaluate multiple scenarios - we will look at a range of modules numbers and a range of strings to find minimum system requirements that satisfy maximum uptime

    pvmodels_param_dict = []
    pvmodels = []

    for m in range(2,8): # m is no of modules
        for n in range(1,25): # n is no of strings        
            if m*n >=panel_number_estimate:           
                z = execute_pvmodel(m,n,m)
                pvmodels_param.append([m, n, n])
                pvmodels.append(z) 
                
    if len(pvmodels) == 0:
    #error for system cant match load profile 
    
    uptime_percent = []

    for i in range(len(pvmodels)):
        uptime_hours = np.count_nonzero(
        (np.array(pvmodels[i].Outputs.system_to_load) + 
         np.array(pvmodels[i].Outputs.batt_to_load) - 
         np.tile(our_load_profile, 25)  # repeat load profile for 25 years
        ) == 0 
        )
    
    uptime_percent.append(uptime_hours/(365 * 24 * 25))
    pvmodel_analysis = pvmodels_param[i]
    pvmodel_analysis.append(uptime_percent[i])
    system_analysis.append(pvmodel_analysis)

    df_system_array = pd.DataFrame(system_analysis,columns = ['Panels in Strings','Strings','Inverters','Uptime_Percent'])
    df_uptime_met = df_system_array[df_system_array.Uptime_Percent>0.95] 
    return 'df_uptime_met?'
