#%% 09.02.2021
# Code was generated by Christine Kaufhold as a part of a sea ice physics course
# Please do not use for research purposes unless you let me know
# This code was used to perform linear regression on regions

from netCDF4 import Dataset, num2date
import numpy.ma as ma
import numpy as np
import xarray
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
#from mpl_toolkits.basemap import Basemap
from scipy.stats import linregress
from scipy import interpolate
from pandas import DataFrame
from scipy.signal import savgol_filter
from mpl_toolkits.basemap import Basemap

from datetime import datetime
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
os.environ["PROJ_LIB"] = "C:\\Users\\owner\\anaconda3\\Library\\share"
    
#%% Arctic Sea Ice Data

data_r = xarray.open_dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc")
data = Dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc", mode='r')
latitude = data.variables["latitude"][:]
longitude = data.variables["longitude"][:]

# Select coordinates to take data in between
latitude = ma.masked_outside(latitude, 42,  65)
#longitude = ma.masked_inside(longitude, 0, 161 )
#longitude= ma.masked_inside(longitude, 0, -149)
longitude = ma.masked_outside(longitude, 135, 165)

#%% Test

iifp = data.variables["IIFP"][:]
oifp = data.variables["OIFP"][:]
siz = data.variables["SIZ"][:]
slip = data.variables["SLIP"][:]

for i in range(0, 39):
    oifp[i] = ma.masked_array(oifp[i], latitude.mask)
    oifp[i] = ma.masked_array(oifp[i], longitude.mask)

    iifp[i] = ma.masked_array(iifp[i], latitude.mask)
    iifp[i] = ma.masked_array(iifp[i], longitude.mask)

data.close()

#%% Begin Regression

n = 1

df = DataFrame(range(1979, 2018, 1), columns=['Years'])
years = df['Years'].values[:,np.newaxis]

#%% Training/observational data

variable = iifp # Choose variable of interest

variable = variable.filled(fill_value=0)
variable = variable.reshape((variable.shape[0], -1)) #order='F')
regr = linear_model.LinearRegression()
regr.fit(years, variable)

slope = regr.coef_
intercept = regr.intercept_
    
slope = slope.reshape(448, 304)
slope = ma.masked_inside(slope, -1E-3, 1E-3)

#%% Prediction data

df = DataFrame(range(2018, 2050, 1), columns=['Years_Predict'])
years_predict = df['Years_Predict'].values[:,np.newaxis]

variable_predict = regr.predict(years_predict)
variable_predict = variable_predict.reshape((variable_predict.shape[0], 448, 304)) #order='F')
variable_predict_mask = (variable_predict < 1E-17)
variable_predict = np.ma.array(variable_predict, mask=variable_predict_mask) 
variable = ma.masked_inside(variable, -1E-3, 1E-3)

#%% Set-up Basemap

m = Basemap(width=18.e6,height=9.e6, projection='gnom',lat_0=90.,lon_0=20., resolution='l')
m.drawmapboundary(fill_color='#13003D')
m.drawcoastlines(linewidth=0.50)
m.fillcontinents(color='#8b8b8b',lake_color='#8b8b8b')
m.drawparallels(np.arange(10,90,5), labels=[True,False,False,False])
m.drawmeridians(np.arange(-180,180,25), labels=[False,False,False,True])
xi, yi = m(longitude, latitude)

#%% Plot

cs = m.pcolor(xi, yi, variable_predict[-1], vmin=0.0, vmax=365.0, cmap='gist_rainbow_r') #'jet') #cmap=newcmp)
plt.title(r"IIFP, Year: 2050", fontsize=13)
ticks = np.linspace(0.0, 365.0, 11, endpoint=True)

cs.set_clim(0,  365.0)
cbar = m.colorbar(cs, location='right', label="Period in days", ticks=ticks)
plt.gcf().set_size_inches(20, 5)
plt.show()

