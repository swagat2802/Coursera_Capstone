#!/usr/bin/env python
# coding: utf-8

# ## Introduction

# Project Title: Helping Customers with their first home

# When buying a new house, most people are concerned about the locality, facilities and restaurants available nearby. 
# The problem in most cities is that people are not able to find the best location to buy a new house.
# My idea is to use the Foursquare location data to find areas with ample facilities nearby and provide this information to people that can help them to buy a new house.
# I am working with a leading bank in Ireland. So my plan is to provide this data science drive insights to our customers to buy a new house in Dublin and surrounding areas, and with that provide our mortgage (home loan) product.

# My idea is to consider two different locations in Dublin, and then analyze these areas based on below 5 categories in nearby locations:
# 1. Restaurants
# 2. Park
# 3. Church
# 4. Gym
# 5. University

# Table of Contents:
#     1. Analyzing Dublin 4 based on above categories
#     2. Analyzing Dublin 8 based on above categories
#     3. Get Trending venues
#     4. Comparing the results
#     5. Summary

# ### Import necessary libraries

# In[1]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# ### Define Foursquare Credentials and Version

# In[39]:


CLIENT_ID = 'A3IMVQQHNHKJ4IG21TD5DTKPLLFKIZTSKNHYCL1B5PQFGBHI' # your Foursquare ID
CLIENT_SECRET = '1AQJ3KKDJ3JPMP3KWSAYJEL0LY5M2C4GQ0NUXIRQQYNFBB12' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# ## Analyze Dublin 4 location

# In[25]:


address1 = 'Dublin 4, Ireland'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address1)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# ##### Now, let's analyze this location based on the 5 categories in nearby areas

# In[26]:


# 1: Restaurants
search_query1 = 'restaurant'

# 2: Parks
search_query2 = 'park'

# 3: Church
search_query3 = 'church'

# 4: Gym
search_query4 = 'gym'

# 5: College/University
search_query5 = 'college university'

radius = 500


# ##### Define the corresponding urls

# In[27]:


# 1: Restaurants
url1 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query1, radius, LIMIT)

# 2: Park
url2 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query2, radius, LIMIT)

# 3: Church
url3 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query3, radius, LIMIT)

# 4: Gym
url4 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query4, radius, LIMIT)

# 5: College/University
url5 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query5, radius, LIMIT)


# ##### Send the GET Request and examine the results

# In[28]:


results1 = requests.get(url1).json()
results2 = requests.get(url2).json()
results3 = requests.get(url3).json()
results4 = requests.get(url4).json()
results5 = requests.get(url5).json()


# ##### Get relevant part of JSON and transform it into a pandas dataframe

# In[29]:


# assign relevant part of JSON to venues
venues1 = results1['response']['venues']
venues2 = results2['response']['venues']
venues3 = results3['response']['venues']
venues4 = results4['response']['venues']
venues5 = results5['response']['venues']

# tranform venues into a dataframe
dataframe1 = json_normalize(venues1)
dataframe2 = json_normalize(venues2)
dataframe3 = json_normalize(venues3)
dataframe4 = json_normalize(venues4)
dataframe5 = json_normalize(venues5)


# ##### Define information of interest and filter dataframe

# In[30]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns1 = ['name', 'categories'] + [col for col in dataframe1.columns if col.startswith('location.')] + ['id']
dataframe_filtered1 = dataframe1.loc[:, filtered_columns1]

filtered_columns2 = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
dataframe_filtered2 = dataframe2.loc[:, filtered_columns2]

filtered_columns3 = ['name', 'categories'] + [col for col in dataframe3.columns if col.startswith('location.')] + ['id']
dataframe_filtered3 = dataframe3.loc[:, filtered_columns3]

filtered_columns4 = ['name', 'categories'] + [col for col in dataframe4.columns if col.startswith('location.')] + ['id']
dataframe_filtered4 = dataframe4.loc[:, filtered_columns4]

filtered_columns5 = ['name', 'categories'] + [col for col in dataframe5.columns if col.startswith('location.')] + ['id']
dataframe_filtered5 = dataframe5.loc[:, filtered_columns5]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered1['categories'] = dataframe_filtered1.apply(get_category_type, axis=1)
dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
dataframe_filtered3['categories'] = dataframe_filtered3.apply(get_category_type, axis=1)
dataframe_filtered4['categories'] = dataframe_filtered4.apply(get_category_type, axis=1)
dataframe_filtered5['categories'] = dataframe_filtered5.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered1.columns = [column.split('.')[-1] for column in dataframe_filtered1.columns]
dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
dataframe_filtered3.columns = [column.split('.')[-1] for column in dataframe_filtered3.columns]
dataframe_filtered4.columns = [column.split('.')[-1] for column in dataframe_filtered4.columns]
dataframe_filtered5.columns = [column.split('.')[-1] for column in dataframe_filtered5.columns]


# ## Analyze Dublin 2 location

# In[47]:


## Analyze Dublin 2 location

address1 = 'Dublin 2, Ireland'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address1)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# ##### Now, let's analyze this location based on the 5 categories in nearby areas

# In[48]:


# 1: Restaurants
search_query1 = 'restaurant'

# 2: Parks
search_query2 = 'park'

# 3: Church
search_query3 = 'church'

# 4: Gym
search_query4 = 'gym'

# 5: College/University
search_query5 = 'college university'

radius = 500


# ##### Define the corresponding urls

# In[49]:


# 1: Restaurants
url1 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query1, radius, LIMIT)

# 2: Park
url2 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query2, radius, LIMIT)

# 3: Church
url3 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query3, radius, LIMIT)

# 4: Gym
url4 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query4, radius, LIMIT)

# 5: College/University
url5 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query5, radius, LIMIT)


# ##### Send the GET Request and examine the results

# In[50]:


results1 = requests.get(url1).json()
results2 = requests.get(url2).json()
results3 = requests.get(url3).json()
results4 = requests.get(url4).json()
results5 = requests.get(url5).json()


# ##### Get relevant part of JSON and transform it into a pandas dataframe

# In[51]:


# assign relevant part of JSON to venues
venues1 = results1['response']['venues']
venues2 = results2['response']['venues']
venues3 = results3['response']['venues']
venues4 = results4['response']['venues']
venues5 = results5['response']['venues']

# tranform venues into a dataframe
dataframe1 = json_normalize(venues1)
dataframe2 = json_normalize(venues2)
dataframe3 = json_normalize(venues3)
dataframe4 = json_normalize(venues4)
dataframe5 = json_normalize(venues5)


# ##### Define information of interest and filter dataframe

# In[52]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns1 = ['name', 'categories'] + [col for col in dataframe1.columns if col.startswith('location.')] + ['id']
dataframe_filtered1 = dataframe1.loc[:, filtered_columns1]

filtered_columns2 = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
dataframe_filtered2 = dataframe2.loc[:, filtered_columns2]

filtered_columns3 = ['name', 'categories'] + [col for col in dataframe3.columns if col.startswith('location.')] + ['id']
dataframe_filtered3 = dataframe3.loc[:, filtered_columns3]

filtered_columns4 = ['name', 'categories'] + [col for col in dataframe4.columns if col.startswith('location.')] + ['id']
dataframe_filtered4 = dataframe4.loc[:, filtered_columns4]

filtered_columns5 = ['name', 'categories'] + [col for col in dataframe5.columns if col.startswith('location.')] + ['id']
dataframe_filtered5 = dataframe5.loc[:, filtered_columns5]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered1['categories'] = dataframe_filtered1.apply(get_category_type, axis=1)
dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
dataframe_filtered3['categories'] = dataframe_filtered3.apply(get_category_type, axis=1)
dataframe_filtered4['categories'] = dataframe_filtered4.apply(get_category_type, axis=1)
dataframe_filtered5['categories'] = dataframe_filtered5.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered1.columns = [column.split('.')[-1] for column in dataframe_filtered1.columns]
dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
dataframe_filtered3.columns = [column.split('.')[-1] for column in dataframe_filtered3.columns]
dataframe_filtered4.columns = [column.split('.')[-1] for column in dataframe_filtered4.columns]
dataframe_filtered5.columns = [column.split('.')[-1] for column in dataframe_filtered5.columns]


# ## Let's summarize each of the categories in both locations of Dublin 2 and DUblin 4 (IRELAND)
# 

# In[55]:


categ1 = dataframe_filtered1['name'].count()
categ2 = dataframe_filtered2['name'].count()
categ3 = dataframe_filtered3['name'].count()
categ4 = dataframe_filtered4['name'].count()
categ5 = dataframe_filtered5['name'].count()

print("Location: Dublin 4, Ireland - ")
print("Restaurants:",categ1)
print("Parks:",categ2)
print("Church:",categ3)
print("Gym",categ4)
print("College/University",categ5)

categ6 = dataframe_filtered1['name'].count()
categ7 = dataframe_filtered2['name'].count()
categ8 = dataframe_filtered3['name'].count()
categ9 = dataframe_filtered4['name'].count()
categ10 = dataframe_filtered5['name'].count()

print("Location: Dublin 2, Ireland - ")
print("Restaurants:",categ6)
print("Parks:",categ7)
print("Church:",categ8)
print("Gym",categ9)
print("College/University",categ10)


# ### Final Result: Based on above output values between Dublin 2 and Dublin 4 can help the customers to pick the best location to buy their new home.

# In[ ]:




