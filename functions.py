import requests
import json
import os
import pandas as pd
from sodapy import Socrata
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# Enter API_KEY for openweather.org, and return the current data for a zipcode.
def getWeatherByZipCode(zipCode):
    # API_KEY shouldn't be open to public. make api key as an environment variable e.g. API_KEY = os.getenv("API_KEY") and import os
    API_KEY = os.environ.get('API_openweather')

    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipCode}&appid={API_KEY}&units=imperial"
    # call the API
    response = requests.get(url)
    # error handing code would be needed - figure out what went wrong

    # convert response to a python object
    jsonWeatherData = json.loads(response.content)

    result = {
        "current Temperature": jsonWeatherData["main"]["temp"],
        "feels like temp": jsonWeatherData["main"]["feels_like"],
        "humidity": jsonWeatherData["main"]["humidity"],
        "verbal desc": " ".join([weather["description"] for weather in jsonWeatherData["weather"]]),
        "location name": jsonWeatherData["name"]
    }

    return result

def getFilmPermitData():
    MyAPPToken = os.environ.get('Soc_App_token')
    nyc_username = os.environ.get('nyc_username')
    nyc_password = os.environ.get('nyc_password')

    client = Socrata("data.cityofnewyork.us",
                     MyAPPToken,
                     username=nyc_username,
                     password=nyc_password)

    # Returned as JSON from API / converted to Python list of dictionaries by sodapy.
    results = client.get("tg4x-b46p")
    #results = client.get("tg4x-b46p", limit=20)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    # Identify the year and month of the permit start date.
    results_df["StartYear"] = results_df["startdatetime"].str[:4]
    results_df["StartMonth"] = results_df["startdatetime"].str[6:7]

    # Split multiple zipcodes into multiple columns
    results_df["zipcode_s"] = results_df["zipcode_s"].astype(str)
    results_df["ZipCodeLength"] = results_df["zipcode_s"].str.len()

    # Identify the longest zipcode list among the permits
    series = results_df["ZipCodeLength"]
    max = series.max()
    id = series.idxmax()

    # Identify the maximum number of zipcode in one array and determine the number of columns related to zipcodes.
    # e.x) If  one event happened in zipcodes [10019, 10020, 10022, 10036, 10112, 11201],
    # the length of the array is 40 = 7*5+5 (7 includes 5 zipcode letters, comma, and space)
    # The number of the zipcodes becomes 6 = (40-5)/7 + 1.
    zip_idx = (max - 5) / 7 + 1
    zip_idx = int(zip_idx)
    for i in range(zip_idx):
        new_col = f"zipcode_{i}"
        results_df[new_col] = results_df["zipcode_s"].str.split(pat=',', expand=True).iloc[:, i]

    return results_df

#In progress
def getCategoryChart(df): 
    category_ct = pd.DataFrame(df["category"].value_counts())
    category_ct = category_ct.reset_index()
    category_ct.columns = ['category', 'counts']
    n = category_ct.shape[0]

    colors = sns.color_palette('pastel')[0:(n - 1)]
    # labels = pd.unique(results_df["category"])

    # create pie chart
    plt.pie(data=category_ct["counts"], labels=category_ct["category"], colors=colors, autopct='%.0f%%')
    plt.show()

#In progress
def getBoroughChart(df):
    sns.histplot(data=df, x="borough", shrink=.8, alpha=.8, legend=False)
    plt.show()

#In progress
def my_plot(x, y, style='o--', label='Data'):
    f, ax = plt.subplots()
    ax.plot(x, y, style, label=label)
    return ax
