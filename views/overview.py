import pandas as pd
import streamlit as st
import json
import time
import requests

from utils.utils import *


def overview():
    #Loop through all activities
    with open('configs/strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)

    page = 1
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']
    ## Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame(
        columns = [
                "id",
                "name",
                "start_date_local",
                "type",
                "distance",
                "moving_time",
                "elapsed_time",
                "total_elevation_gain",
                # "average_heartrate",
                # "max_heartrate",
                # "average_speed"

        ]
    )
    while True:
        
        # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        # if no results then exit loop
        if (not r):
            break
        
        # otherwise add new data to dataframe
        for x in range(len(r)):
            activities.loc[x + (page-1)*200,'id'] = r[x]['id']
            activities.loc[x + (page-1)*200,'name'] = r[x]['name']
            activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
            activities.loc[x + (page-1)*200,'type'] = r[x]['type']
            activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
            activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
            activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
            activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            # activities.loc[x + (page-1)*200,'average_heartrate'] = r[x]['average_heartrate']
            # activities.loc[x + (page-1)*200,'max_heartrate'] = r[x]['max_heartrate']
            # activities.loc[x + (page-1)*200,'average_speed'] = r[x]['average_speed']

        # increment page
        page += 1
    # activities.to_csv('strava_activities_2.csv')

    st.dataframe(activities, height=800)