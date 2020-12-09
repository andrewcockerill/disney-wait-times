## Predictive Modeling of Walt Disney World Attraction Wait Times

### Overview
This repository contains pertinent Python scripts and notebooks used to procure
datasets involving the wait times for a selection of rides/attractions at various
theme parks within the Walt Disney World Resort. This data is then combined with
other covariates with the goal of building predictive models to forecast wait times.

### Methods
For this project, we will leverage multiple data sources to build out a set of potential predictors
of wait times at a given time of day, measured as a continuous feature in hours (ex. 7:45 PM is represented by
19.75). To consolidate all of the raw data, an initial script is called to query this from the web either by
direct download or by using free API calls. All data will be transformed and ingested into a sqlite database. This
can allow us to expore the data though multiple means (SQL queries, pandas DataFrames).

Overall, we will look to incorporate data from the following resources:

- **TouringPlans**: Historical wait times for multiple rides
- **NOAA National Climate Datacenter**: Historical temperature data
- **U.S. Bureau of Labor Statistics**: Historical data of economic and employment indicators
- **Python holidays package**: Provides Federal and State level data on holidays, calendar metadata

For this analysis, we will consider the hypothetical use case in which we seek to use the prior three years of data
for a single attraction to build a regression model that predicts wait times for the upcoming year. Given this method,
we employ a "sliding" train-validation-test split in which models will be trained on 3 years of data, which are then validated/tuned
on the following year's data. After a model is selected, the window then "slides" so that it includes 2 years from the original training set
along with the validation set. This final model is then applied to a holdout test set that is one year ahead of the validation set. This will
be used as our unbiased estimate of error for the model. This is similar to the time series cross-validation methods described by Hyndman (https://robjhyndman.com/hyndsight/tscv/).

### How to Use
The following scripts/notebooks describe how one might employ the methods detailed above. As of 12/2020, this project attempts the proposed methodology
to predict wait times for the *Soarin'* ride, a popular attraction at Epcot.

- <tt>src/data_acquisition.py</tt>: Data acquisition script, requires API keys from NOAA and U.S. BLS
- <tt>notebooks/soarin_eda.ipynb</tt>: Exploratory data analysis of wait times for the attraction
- <tt>notebooks/soarin_modeling.ipynb</tt>: Construction of regression models to predict future wait times, estimation of model error

### Citations
The wait time datasets used in this project have been made available by TouringPlans.com
for data science use cases. Citations for the involved datasets are provided below:


"alien_saucers.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"flight_of_passage.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"dinosaur.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"expedition_everest.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"kilimanjaro_safaris.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"navi_river.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"pirates_of_caribbean.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"rock_n_rollercoaster.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"7_dwarfs_train.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"slinky_dog.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"soarin.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"spaceship_earth.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"splash_mountain.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.
    

"toy_story_mania.csv", Disney World Ride Wait Time Datasets, TouringPlans.com, June 2018, 
https://www.touringplans.com/walt-disney-world/crowd-calendar/#DataSets. 
First Accessed 13 September 2020.

This project also uses leverages the following APIs:

National Centers for Environmental Information API
https://www.ncdc.noaa.gov/cdo-web/webservices/v2
First Accessed 13 September 2020.


U.S. Bureau of Labor Statistics API, February 2016
https://www.bls.gov/developers/
First Accessed 13 September 2020.
