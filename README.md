# Welcome to SolarSizer

<img src="doc/SolarSizerLogo.png" width="250" height="100" />

Created by: Cassidy Quigley, Clayton Sasaki, Lindsey Taylor, Ning Wang

## Objective

The main objective of SolarSizer is to assist in the planning of small off-grid solar projects by creating a user friendly dashboard that takes in a location and load profile and returns an equipment list and cost estimate of a solar array capable of meeting the load profile.

## Structure

![Example diagram](doc/SolarSizerFlowChart.png)

## How to install and run SolarSizer

SolarSizer is set up using a conda environment to make sure the correct dependencies are installed. If you do not use conda you will need to make sure you have the packages listed in the environment.yml installed.

1. Clone the repository to your local machine: https://github.com/UW-Solar-GRID/SolarSizer.git
2. Naviate to the base SolarSizer directory: `cd SolarSizer`
3. Set up the conda environment: `conda env create -f environment.yml`
4. Activate the conda environment with: `conda activate grid_ss`
5. Run the dashboard interface with: `python GUI.py` 
6. Copy the locally hosted URL from the command line to navigate to the dashboard interface.

## Acknowledgements

This python package has been created for CSE 583 under the guidence of Professor David Beck and Anant Mittal from the University of Washington. This package also uses modeling code developed by [GRID](https://github.com/UW-GRID/PV_sizing), a registered student orgainization at the University of Washington.
