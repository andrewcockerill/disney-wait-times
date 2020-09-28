import numpy as np
import pandas as pd
import holidays
import requests
import time
import json
import sqlite3
import os

###########################################
# TouringPlans wait times
###########################################

def fetch_one_wait_time_hist(url, attraction_name):
    """Retrieves and formats an attraction wait time dataset from public .csvs made available
    by TouringPlans (https://touringplans.com/walt-disney-world/crowd-calendar#DataSets). Output
    dataset is transformed to provide pertinent time data and wait times. Missing data is not handled
    at this point.
    
    Args:
        url : string
            The URL of the dataset
            
        ride_name : string
            Description of the ride
            
    Returns:
        wait_times : DataFrame
            The prepared data frame with columns for a single attraction
    """
    
    # Read in the csv file
    wait_times = pd.read_csv(
        url,
        usecols=['datetime','SACTMIN','SPOSTMIN'],
        dtype={'datetime':str,'SACTMIN':np.float64,'SPOSTMIN':np.float64}
    )
    
    # Transforms for date elements
    wait_times.loc[:,'datetime'] = pd.to_datetime(wait_times.datetime, format='%Y-%m-%d %H:%M:%S')
    wait_times['month_of_year'] = wait_times.datetime.dt.month
    wait_times['day_of_month'] = wait_times.datetime.dt.day
    wait_times['day_of_week'] = wait_times.datetime.dt.dayofweek
    wait_times['hour_of_day'] = wait_times.datetime.dt.hour
    wait_times['minute_of_day'] = wait_times.datetime.dt.minute
    wait_times['year_of_calendar'] = wait_times.datetime.dt.year
    wait_times['date_id'] = wait_times.datetime.dt.date
    
    # Wait time coalesce (use the actual time if available)
    wait_times['wait_time'] = wait_times.SACTMIN.combine_first(wait_times.SPOSTMIN)
    
    # Descriptor
    wait_times['attraction_name'] = attraction_name
    
    # Output data
    wait_times = wait_times[['attraction_name','date_id','month_of_year','day_of_month','day_of_week','hour_of_day','minute_of_day','year_of_calendar','wait_time']]
    return wait_times

def fetch_all_wait_time_hist():
    """Function to download all wait time datasets from public .csvs made available
    by TouringPlans (https://touringplans.com/walt-disney-world/crowd-calendar#DataSets).
    Output is saved as a single consolidated .csv file.
    
    Args:
        None
            
    Returns:
        wait_times : DataFrame
            The prepared data frame with columns for all attractions made available by
            TouringPlans
    """
    
    # Dictionary of attraction names and .csv urls
    url_lookup = {
        'Alien Swirling Saucers': 'https://cdn.touringplans.com/datasets/alien_saucers.csv',
        'Avatar Flight of Passage': 'https://cdn.touringplans.com/datasets/flight_of_passage.csv',
        'DINOSAUR': 'https://cdn.touringplans.com/datasets/dinosaur.csv',
        'Expedition Everest': 'https://cdn.touringplans.com/datasets/expedition_everest.csv',
        'Kilimanjaro Safaris': 'https://cdn.touringplans.com/datasets/kilimanjaro_safaris.csv',
        'Navi River Journey': 'https://cdn.touringplans.com/datasets/navi_river.csv',
        'Pirates of the Caribbean': 'https://cdn.touringplans.com/datasets/pirates_of_caribbean.csv',
        'Rock n Roller Coaster': 'https://cdn.touringplans.com/datasets/rock_n_rollercoaster.csv',
        'Seven Dwarfs Mine Train': 'https://cdn.touringplans.com/datasets/7_dwarfs_train.csv',
        'Slinky Dog Dash': 'https://cdn.touringplans.com/datasets/slinky_dog.csv',
        'Soarin': 'https://cdn.touringplans.com/datasets/soarin.csv',
        'Spaceship Earth': 'https://cdn.touringplans.com/datasets/spaceship_earth.csv',
        'Splash Mountain': 'https://cdn.touringplans.com/datasets/splash_mountain.csv',
        'Toy Story Mania': 'https://cdn.touringplans.com/datasets/toy_story_mania.csv'     
    }
    
    # Set up output dataframe
    wait_times = pd.DataFrame()
    
    # Iterate through dictionary
    for attraction_name, url in url_lookup.items():
        context_df = fetch_one_wait_time_hist(url=url, attraction_name=attraction_name)
        wait_times = pd.concat([wait_times,context_df]).reset_index(drop=True)
        
    # Return data
    return wait_times

###########################################
# Federal holidays
###########################################

def fetch_holidays():
    """Leverage the holidays package to create a dataframe of holiday names and related dates
    from 2015-2019.
    
    Args:
        None
    
    Retruns:
        date_df : DataFrame
            The data frame of holidays and dates
    """
    
    # Holiday object
    us_holidays = holidays.US(years=[i+2015 for i in range(5)])
    us_holidays = sorted(us_holidays.items())
    
    # Data frame
    date_df = pd.DataFrame(us_holidays)
    date_df.columns = ['date_id', 'holiday_name']
    return date_df

###########################################
# Temperature data
###########################################

def fetch_tmax_hist(api_key):
    """Pull 2015-2019 observed hi temperatures measured from MCO. In practice, only forecasted
    temperatures would be available.
    
    Args:
        api_key : string
            API key provided by NOAA National Climatic Data Center for data requests
            
    Returns:
        tmax_df : DataFrame
            The dataframe consisting of daily high temperatures measured on the Fahrenheit scale
    """
    
    # Set up output dataframe
    tmax_df = pd.DataFrame()
    
    # API token header
    headers = {'token':api_key}
    
    # Establish years to pull from
    years = [2015, 2016, 2017, 2018, 2019]
    
    # Parameters
    param_strings = ['datasetid=GHCND&stationid=GHCND:USW00012815&startdate={0}-01-01&enddate={0}-12-31&datatypeid=TMAX&units=standard&limit=1000' \
                     .format(str(i)) for i in years]
    
    # Run API requests and append
    print('Preparing to run {0} NCDC API request(s)'.format(str(len(years))))
    
    for idx, params in enumerate(param_strings):
        print('Running request number {0}'.format(idx+1))
        time.sleep(5) # Set delay between requests as a precaution (limit is 5 requests per second)
        
        api_req = requests.get(url='https://www.ncdc.noaa.gov/cdo-web/api/v2/data',
                               params=params,
                               headers=headers)
        
        req_results = api_req.json()['results']
        
        context_df = pd.DataFrame.from_dict(req_results)
        tmax_df = tmax_df.append(context_df, ignore_index=True)
    
    # Dataframe pivot
    tmax_df = tmax_df.pivot(index='date', columns='datatype',values='value')
    tmax_df['date_id'] = tmax_df.index
    tmax_df = tmax_df.reset_index(drop=True)[['date_id','TMAX']]
    
    # Date handling
    tmax_df.loc[:, 'date_id'] = pd.to_datetime(tmax_df.date_id.str[0:10], format='%Y-%m-%d').dt.date
    tmax_df.columns = ['date_id','tmax']
    
    return tmax_df


###########################################
# BLS data
###########################################

def make_bls_df(req, idx, metric):
    """Helper function to create a dataframe from a BLS API request JSON string.
    
    Args:
        req : Response object
            The response object from a requests.post call
        
        idx : int
            The index of the JSON series to pull the data from
            
        metric : str
            The name of the metric being tracked
    """
    
    # Context json
    context_json = req.json()['Results']['series'][idx]['data']
    
    # Dataframe
    context_df = pd.DataFrame.from_dict(context_json)
    context_df['month_of_year'] = context_df.period.str[1:3].astype(int)
    context_df['year_of_calendar'] = context_df.year.astype(int)
    context_df[metric] = context_df.value.astype(np.float64)
    context_df = context_df[['month_of_year', 'year_of_calendar', metric]]
    
    return context_df
    

def fetch_bls_hist(api_key):
    """Retrieve three datasets of economic indicator data from the BLS API. This includes (not seasonally adjusted)
    (1) Unemployment data for the Orlando-Kissimmee-Sanford area
    (2) National unemployment data
    (3) National CPI data
    
    Args:
        api_key : string
            The key provided by BLS needed to use Version 2 of the public API
            
    Returns:
        out_df : DataFrame
            Dataset containing unemployment and cpi metrics by month and year
    """
    
    # Header
    headers = {'Content-type': 'application/json'}
    
    # Payload
    # LAUMT123674000000003 : local unemployment for Orlando
    # LNU04000000: national unemployment
    # CUUR0000SA0 : national CPI
    
    series_list = ['LAUMT123674000000003','LNU04000000','CUUR0000SA0']
    
    payload = json.dumps({
        "seriesid": series_list,
        "startyear": "2014",
        "endyear": "2019",
        "registrationkey": api_key
        })
    
    # Request
    print('Sending request, may take a few minutes...')
    req = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=payload, headers=headers)
    
    # Dataframes
    local_unemp = make_bls_df(req=req, idx=0, metric='unemp_local')
    natl_unemp = make_bls_df(req=req, idx=1, metric='unemp_natl')
    natl_cpi = make_bls_df(req=req, idx=2, metric='cpi_natl')
    
    # Consolidated dataframe
    out_df = pd.merge(local_unemp, natl_unemp, how='outer', on=['month_of_year','year_of_calendar'])
    out_df = pd.merge(out_df, natl_cpi, how='outer', on=['month_of_year','year_of_calendar'])
    
    return out_df

###########################################
# Build SQL Database
###########################################

def build_sqlite_db(ncdc_api_key, bls_api_key):
    """Builds a database using sqlite3 to store all relevant datasets as tables to use
    for exploratory analysis and modeling. Data will be stored to ../data/project_data.db. Any
    tables that already exist will be overwritten.
    
    Args:
        ncdc_api_key : str
            API key provided by NOAA National Climatic Data Center for data requests
            
        bls_api_key : str
            The key provided by BLS needed to use Version 2 of the public API
            
    Returns:
        None
    """
    
    # Build datasets
    print('Step 1 - Fetching wait time data...')
    wait_time_data = fetch_all_wait_time_hist()
    
    print('Step 2 - Fetching holiday data...')
    holiday_data = fetch_holidays()
    
    print('Step 3 - Fetching daily hi temperature data...')
    tmax_data = fetch_tmax_hist(api_key=ncdc_api_key)
    
    print('Step 4 - Fetching BLS stats...')
    bls_data = fetch_bls_hist(api_key=bls_api_key)
    
    print('Building DB...')
    
    # Connection - will create if does not already exist
    conn = sqlite3.connect('../data/project_data.db')
    wait_time_data.to_sql('T_WAIT_TIMES', con=conn, if_exists='replace', index=False)
    holiday_data.to_sql('T_HOLIDAYS', con=conn, if_exists='replace', index=False)
    tmax_data.to_sql('T_HI_TEMPERATURES', con=conn, if_exists='replace', index=False)
    bls_data.to_sql('T_BLS_STATS', con=conn, if_exists='replace', index=False)
        
    print('Finished!')
        
        
        
