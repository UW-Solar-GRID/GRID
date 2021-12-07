#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import numpy as np
import pandas as pd
import PySAM.Pvsamv1 as pv
import matplotlib.pyplot as plt
import urllib.request


# ## Load Profile
# 
# Getting our load profile



# ## PV Model - "PVBatteryResidential"
# 
# `PVBatteryResidential` is one of the buit-in models in PySAM. We will use it for our analysis as it meets all of our basic requirements.
# 
# - Instantiate the model with default values
# - Specify the solar resource file for the location
# - Assign the load profile (defined above) to the the model. This will inform the model what kind of load our system will support
# - Pick module and inverter models - can design our own with specifications as needed but here we will pick from the available database
# - Identify the minimum and the maximum number of modules that can be in a string (*connected in series*). This is to make sure we are in the operating range for the inverter. The number of modules we select to be connected in a string must fall between these min and max values
# - Design the system :
#     - Set inverter count - *how many inverters do we want?*
#     - For a single subarray:
#         - Assign the number of modules in a string (*modules in series*)
#         - Assign the number of strings (*rows (in parallel)*)
#         - Fixed axis system or tracking (*tracking means it will track the sun throughout the day*)
#     - Repeat for desired number of subarrays
# - Specify Battery system specs: charge, discharge
# - Identify power dispatch from battery
#     - Manually control - specify when to charge and discharge the battery (*this makes more sense if you look at the UI in SAM*)
# - Execute the model!

# Refer [this link](https://sam.nrel.gov/images/webinar_files/sam-webinars-2020-modeling-pv-systems.pdf) for detailed explanation on MMPT, subarray, strings, etc

# In[15]:


def execute_pvmodel(number_of_modules_per_string, number_of_strings, n_inverters=4):
    
    data_path = os.path.abspath("../SolarSizer/data")
    
    # initialize model with defaults
    pvmodel = pv.default('PVBatteryResidential')
    
    # sepcify solar resource file for the location
    pvmodel.SolarResource.solar_resource_file = os.path.join(data_path, "irradiance.csv")
    
    print('found irradiance.csv')
    print(os.path.join(data_path, "irradiance.csv"))
    
    # try user load profile, if it does not work use default load profile 
    try:
        our_load_profile = np.loadtxt(os.path.join(data_path, "user_load_profile.txt"), skiprows=0)
        
        print('user load profile loaded')
        print(os.path.join(data_path, "user_load_profile.txt"))
    
    except:
        # add exception
        pass
       # our_load_profile = np.loadtxt(os.path.join(data_path, "Max_load_profile_for_year.txt"), skiprows=1)
        
       # print('user load profile did not work. Using default load profile')
       # print(os.path.join(data_path, "Max_load_profile_for_year.txt"))
    

    
    pvmodel.Load.load = tuple(our_load_profile)
    
    print('loaded load profile')
    
    # select module and inverter from database
    pvmodel.Module.module_model = 1 # set it to CEC model
    
    pvmodel.Inverter.inverter_model = 0. # set it to CEC
    pvmodel.Inverter.inv_num_mppt = 1 # use single mmpts
    
    
    ## Max number of modules in a string
    max_modules_in_string = pvmodel.Inverter.mppt_hi_inverter/pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_oc_ref
    
    ## Min number of modules in a string
    min_modules_in_string = pvmodel.Inverter.mppt_low_inverter/pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_oc_ref
    
    print('set some parameters and got min and max modules')
    
    # modules per string specified must be within (min, max) modules required
    assert number_of_modules_per_string > min_modules_in_string
    assert number_of_modules_per_string < max_modules_in_string
    
    print('min and max modules check passsed')
    
    # System Design
    pvmodel.SystemDesign.inverter_count = n_inverters

    pvmodel.SystemDesign.subarray1_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray1_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray1_mppt_input = 1
    pvmodel.SystemDesign.subarray1_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray2_enable = 1
    pvmodel.SystemDesign.subarray2_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray2_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray2_mppt_input = 1
    pvmodel.SystemDesign.subarray2_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray3_enable = 1
    pvmodel.SystemDesign.subarray3_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray3_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray3_mppt_input = 1
    pvmodel.SystemDesign.subarray3_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray4_enable = 1
    pvmodel.SystemDesign.subarray4_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray4_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray4_mppt_input = 1
    pvmodel.SystemDesign.subarray4_track_mode = 0 # fixed tracking
    
    print('something System Design')
    
    # Total Capacity of the system
    mod_power_rating = pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_mp_ref * pvmodel.CECPerformanceModelWithModuleDatabase.cec_i_mp_ref
    pvmodel.SystemDesign.system_capacity = mod_power_rating * 4 * number_of_modules_per_string * number_of_strings
    
    print('something Total Capacity of the system')
    
    # Battery system design - charge/discharge
    pvmodel.BatterySystem.batt_current_charge_max = 24
    pvmodel.BatterySystem.batt_current_discharge_max = 24

    pvmodel.BatterySystem.batt_power_charge_max_kwac = 12
    pvmodel.BatterySystem.batt_power_discharge_max_kwac= 11

    pvmodel.BatterySystem.batt_power_charge_max_kwdc = 12
    pvmodel.BatterySystem.batt_power_discharge_max_kwdc= 12
    
    print('something Battery system design')

    # MUST ENABLE Battery storage!!
    pvmodel.BatterySystem.en_batt = 1
    
#     pvmodel.BatterySystem.batt_computed_bank_capacity = batt_bank_capacity # kWh
#     pvmodel.BatterySystem.batt_computed_series = 139
#     pvmodel.BatterySystem.batt_computed_strings = 48
#     pvmodel.BatterySystem.batt_power_charge_max_kwac = 10.417
#     pvmodel.BatterySystem.batt_power_discharge_max_kwac = 9.6
#     pvmodel.BatterySystem.batt_power_charge_max_kwdc = 9.982
#     pvmodel.BatterySystem.batt_power_discharge_max_kwdc = 9.982

    # Battery Dispatch
    pvmodel.BatteryDispatch.batt_dispatch_choice = 4.0 # manual discharge
    pvmodel.BatteryDispatch.dispatch_manual_charge = (1, 1, 1, 1, 0, 0)
    pvmodel.BatteryDispatch.dispatch_manual_discharge = (1, 1, 1, 1, 0, 0)
    pvmodel.BatteryDispatch.dispatch_manual_percent_discharge = (25, 25, 25, 75)
    
    print('about to execute model')
    
    # Finally, run the model!
    pvmodel.execute()
    
    print('done executing the model')
    
    return pvmodel, our_load_profile
