#%% 09.02.2021
# Code was generated by Christine Kaufhold as a part of a sea ice physics course
# Please do not use for research purposes unless you let me know
# This code was used to make histograms of the data

from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import PercentFormatter
import matplotlib.pylab as plt
from matplotlib import cm
import numpy.ma as ma
import pandas as pd
import numpy as np
import xarray
import csv
import os

from datetime import datetime
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
os.environ["PROJ_LIB"] = "C:\\Users\\owner\\anaconda3\\Library\\share"
from mpl_toolkits.basemap import Basemap

#%% Arctice Sea Ice Data

data_r = xarray.open_dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc")
data = Dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc", mode='r')
latitude = data.variables["latitude"][:]
longitude = data.variables["longitude"][:]


iifp = data.variables["IIFP"][:]
iifp_masked = (iifp < 0)
iifp = np.ma.array(iifp, mask=iifp_masked)    

oifp = data.variables["OIFP"][:]
oifp_masked = (oifp < 0)
oifp = np.ma.array(oifp, mask=oifp_masked) 

siz = data.variables["SIZ"][:]
slip = data.variables["SLIP"][:]

#%% Data manipulation

variable = oifp[-1] # Variable of interest
variable = variable.flatten()

fig = plt.figure(figsize=(11, 3))
ax = fig.add_subplot(111)

plt.grid()
histogram_var = variable[variable.mask == False]
weights = np.ones_like(histogram_var) / len(histogram_var)
plt.hist(histogram_var, bins=np.linspace(0, 365, 35), weights=weights)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
plt.title(r"OIFP Histogram, Year:2017", fontsize=13)
plt.xlabel("Period in days", fontsize=10)
plt.ylabel("Percentage of the area, %", fontsize=10)
plt.xlim(0, 365)
plt.show()