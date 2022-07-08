import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

'''
# Taxi fare calculation for NY city
'''
st.markdown('Made by Patricia R Soares de Souza')

# get date
d = st.date_input(
    "Select travel date:",
    datetime.datetime(2019, 7, 6))
# get time
t = st.time_input('Select travel time:', datetime.time(6, 8, 45))

# combine date & time
formatted_pickup_datetime = f"{d} {t}"

# get pickup & dropoff
def get_lonlat(address):
    '''This function uses the nominatim API to convert address into longitude & latitude
    input: address string
    '''
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q':address, \
            'format':'json'}
    response = requests.get(url,
                        params=params).json()[0]

    return  float(response['lat']), float(response['lon'])

# get pickup lat/long
pickup = st.text_input('Pickup location (street name, number, and city):', '20 W 34th St., New York, NY 10001, United States')
lat1, lon1 = get_lonlat(pickup)

# get dropoff lat/long
dropoff = st.text_input('Dropoff location (street name, number, and city):', '334 Furman St, Brooklyn, NY 11201, United States')
lat2, lon2 = get_lonlat(dropoff)

#get map
pickup_point = {"lat":[lat1, lat2], "lon":[lon1, lon2]}
pickup_df= pd.DataFrame(data=pickup_point)
st.map(pickup_df)




# https://api.mapbox.com/directions/v5/mapbox/driving-traffic


# get number of passengers
passengers = st.slider('Select number of passengers', 1, 20, 3)


# create parameter dictionary for our taxi fare API
parameters = {
    # FAKE KEY FOR SUBMIT TO KAGGLE
    "key": "2013-07-06 17:18:00.000000119",
    "pickup_datetime": formatted_pickup_datetime,
    "pickup_longitude": lon1,
    "pickup_latitude": lat1,
    "dropoff_longitude": lon2,
    "dropoff_latitude": lat2,
    "passenger_count": passengers
    }




url = 'https://taxifare.lewagon.ai/predict'

#if url == 'https://taxifare.lewagon.ai/predict':

#    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


response = requests.get(url,
                        params=parameters).json()

#Display fare
fare= round(response['fare'], 2)
st.metric("Fare", f"{'$'}{fare}")
