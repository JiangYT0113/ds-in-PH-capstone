# ds-in-PH-capstone
The goal is to create a simple covid dashboard in streamlit. Your app should desplay the daily deaths, recoveries and cases in some fashion in a sigle page. There has to be some user controls to change the view or graph properties (up to you!). You need to display at least one country.
Example of reading in the data
 
import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import statsmodels.api as sm
dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
## Get Italy, drop everyrthing except dates, convert to long (unstack converts to tuple)
y=dat[dat['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).unstack()
## convert from tuple to array
y = np.asarray(y)  
## get case counts instead of cumulative counts
y = y[1 : y.size] - y[0 : (y.size - 1)]
## get the first non zero entry
y =  y[np.min(np.where(y !=  0)) : y.size]
plt.plot(y)
 
 
Please include a short gif screencast in your repository of your app running. I use chromecapture for this.
Please only submit one repository per group.
Please include all of the names of the people in your group.
