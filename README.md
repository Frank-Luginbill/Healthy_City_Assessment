# Healthy_City_Assessment

This is the readme file for the Healthy City Assessment project that is being hosted by MSU. This project aims to enhance the analysis of health data in the tri-county area, particularily for vulnerable elderly populations. This project is hosted by the Center of Community and Economic Development at MSU, and they have partnered with a group of students from MSU's cmse495 class. CMSE495 is the capstone class for the Computational Data Science program, and it revolves around a single collabrative group project between community partner and student group. This repository is run by the student group responsible for the Healthy City Assessment project, who are Frank Luginbill, Noah Mueller, Jun Han, and Amman Thasin.

Folder organization:
Data found in Teams Folder -> "Use These Datasets When Running Map" Folder


Ground rules for maintaining this repository:
1. If you add, remove, or edit any folders, make sure to document it above so that we can keep track of it.
2. For handling weekly work, make a branch to work locally, and then when we meet in class we can discuss the changes made and merge it together

## Code Files
1. app.py - Runs the streamlit map.
2. getting_bus_stops.ipynb - Code used to pull bus stops without API key.
3. census_data_cleaning.ipynb - Code used to clean census data files that were pulled from the 2023 census data.

## Map Usage & Installation Instructions
[The map is currently available at this link](https://msu-healthy-city-map.streamlit.app/)

### Running Locally
1. Clone or unzip the project repository into a folder on your computer. Use command: git clone https://github.com/Frank-Luginbill/Healthy_City_Assessment
2. Download and install the [condaforge](https://conda-forge.org/) software for your OS. Follow default install instructions.
3. When you are installing on Mac make sure you say yes to having conda be installed on your current shell.
4. Open an conda command prompt on windows, or terminal on mac, and navigate to the project folder. (This can be done using the command: cd <PATH>)
5. Create a project specific conda environment by running the following command from the unzipped folder conda env create --prefix ./envs --file environment.yml
6. Activate the conda environment using the following command: conda activate ./envs
7. Download the required data, data found in Teams Folder -> "Use These Datasets When Running Map" Folder. Put all extracted data into the data folder and not in the github main folder so that the code correctly locates the data files.
8. Make sure ALL the files from that folder are individually within the **data** folder, NOT just moving the "Use These Datasets.." folder into the project folder or dumping the data into the project folder.
9. Now, run the file using the command streamlit run app.py
