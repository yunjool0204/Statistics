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

 results_df = getFilmPermitData()

 category_ct = pd.DataFrame(results_df["category"].value_counts(normalize = True))
 category_ct = category_ct.reset_index()
 category_ct.columns = ['category', 'counts']
 print(category_ct)
 n = category_ct.shape[0]
 #
 colors = sns.color_palette('pastel')[0:(n-1)]
 plt.pie(data = category_ct, x = 'counts', labels = 'category', colors=colors, autopct='%.0f%%')
 plt.show()
 # #print(category_ct.iloc[:,0])
 # #print(category_ct.iloc[:,0].to_numpy())

