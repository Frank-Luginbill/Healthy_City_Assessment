# Healthy_City_Assessment

This is the readme file for the Healthy City Assessment project that is being hosted by MSU. This project aims to enhance the analysis of health data in the tri-county area, particularily for vulnerable elderly populations. This project is hosted by the Center of Community and Economic Development at MSU, and they have partnered with a group of students from MSU's cmse495 class. CMSE495 is the capstone class for the Computational Data Science program, and it revolves around a single collabrative group project between community partner and student group. This repository is run by the student group responsible for the Healthy City Assessment project, who are Frank Luginbill, Noah Mueller, Jun Han, and Amman Thasin.

Folder organization:
(update as we add code)


Ground rules for maintaining this repository:
1. If you add, remove, or edit any folders, make sure to document it above so that we can keep track of it.
2. For handling weekly work, make a branch to work locally, and then when we meet in class we can discuss the changes made and merge it together

## Map Usage & Installation Instructions
[The map is currently available at this link](https://msu-healthy-city-map.streamlit.app/)

### Running Locally
1. Clone or unzip the project repository into a folder on your computer. Use command: git clone https://github.com/Frank-Luginbill/Healthy_City_Assessment
2. Download and install the [condaforge](https://conda-forge.org/) software for your OS. Follow default install instructions.
3. Open an conda command prompt and navigate to the project folder. (This can be done using the command: cd <PATH>)
4. Create a project specific conda environment by running the following command from the unzipped folder conda env create --prefix ./envs --file environment.yml
5. Activate the conda environment using the following command: conda activate ./envs
6. Before you are able to run the map through the conda command prompt you must create a google maps API key. Instructions can be found [here](https://developers.google.com/maps/documentation/javascript/get-api-key)
7. *Once you have your key, create a config.yaml file and add this text, but fill in your personal key: api_key: "YOUR_SECRET_KEY"
8. Ensure that your API key has access to these features: Places API,
Maps Static API,
Maps SDK for iOS,
Maps Embed API,
Maps Elevation API,
Geolocation API,
Geocoding API
9. Now back in the conda command prompt, run the file using the command streamlit run app.py

*Note: After 30 days google will require you to upgrade to a paid plan, but you will not be charged unless there's over 10,000 calls which we do not anticipate.
