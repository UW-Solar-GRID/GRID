# Welcome to SolarSizer

<img src="doc/SolarSizerLogo.png" width="250" height="100" />

Created by: Cassidy Quigley, Clayton Sasaki, Lindsey Taylor, Ning Wang

## Objective

The main objective of SolarSizer is to assist in the planning of small off-grid solar projects by creating a user friendly dashboard that takes in a location and load profile and returns an equipment list and cost estimate of a solar array capable of meeting the load profile.

## Structure

![Example diagram](doc/SolarSizerFlowChart.png)

## How to install and run SolarSizer

After cloning the repo to your local machine and navigating to the base SolarSizer directory, you will need to set up the environment for running the code. This may be done using the following line of code:
`conda env create -f environment.yml`
You will then need to activate the environment with `conda activate grid_ss`

The interface will be created when you run the GUI file. To do so, enter `python GUI.py` into the command line. Copy the link provided in the output to navigate to the user interface.

## Acknowledgements

This python package has been created for CSE 583 under the guidence of Professor David Beck and Anant Mittal from the University of Washington. This package also uses modeling code developed by [GRID](https://github.com/UW-GRID/PV_sizing), a registered student orgainization at the University of Washington.
