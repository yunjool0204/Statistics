# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from sodapy import Socrata
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests
import json
import os


from dotenv import load_dotenv
load_dotenv()

from functions import getWeatherByZipCode
from functions import getFilmPermitData
#from functions import getFilmPermitData_byYr



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Convert to pandas DataFrame
 results_df = getFilmPermitData()
 # for col in results_df.columns:
 #    print(col)
 #print(getWeatherByZipCode(10128))

 #print(results_df[results_df["borough"] == "Manhattan"].shape)

 # # plot
 # fig, ax = plt.subplots()
 #
 # ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
 #
 # #ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
 # #      ylim=(0, 8), yticks=np.arange(1, 8))
 #
 # plt.show()

 #getBoroughChart(results_df)
 #sns.histplot(data=results_df, x="StartMonth", shrink=.8, alpha=.8, legend=False)
 #plt.show()
 #define Seaborn color palette to use


 # Restructure the category by summing bottom 5 categories
 category_ct = pd.DataFrame(results_df["category"].value_counts(normalize = True))
 category_ct = category_ct.reset_index()
 category_ct.columns = ['category', 'counts']
 print(category_ct)
 print(np.sum(category_ct.iloc[:,1]))
 others = np.sum(category_ct.loc[4:8]['counts'])
 print(category_ct.loc[4:8]['counts'])
 category_ct = category_ct.drop(labels = range(4,9), axis = 0)
 print(category_ct)
 others_df = pd.DataFrame({'category': ['Others'], 'counts': [others]})
 print(others_df)
 category_ct = pd.concat([category_ct, others_df], ignore_index = True)
 n = category_ct.shape[0]
 #
 colors = sns.color_palette("Set3")
 plt.pie(data = category_ct, x = 'counts', labels = 'category', colors=colors, autopct='%.0f%%')
 plt.show()
 # #print(category_ct.iloc[:,0])
 # #print(category_ct.iloc[:,0].to_numpy())

#print(results_df["startdatetime"])
 # url = "https://data.cityofnewyork.us/resource/tg4x-b46p.json?startdatetime=2021-01-04T00:01:00.000"
 # response = requests.get(url)
 # opennycData = json.loads(response.content)
 # opennycData_df = pd.DataFrame.from_records(opennycData)
 # print(opennycData_df)
 # startdate = "'2022-01-01T00:00:00'"
 # enddate = "2022-12-31T00:00:00"
 # #opennycData_df = getFilmPermitData_byYr(startdate, enddate)
 #
 # url = f"https://data.cityofnewyork.us/resource/tg4x-b46p.json?$where=startdatetime between {startdate} and {enddate}"
 # response = requests.get(url)
 # opennycData = json.loads(response.content)
 # opennycData_df = pd.DataFrame.from_records(opennycData)
 # print(opennycData_df)







