#%% 09.02.2021
# Code was generated by Christine Kaufhold as a part of a sea ice physics course
# Please do not use for research purposes unless you let me know
# This code was used to visualize different regions

from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as plt
from matplotlib import cm
import numpy.ma as ma
import pandas as pd
from matplotlib.patches import Polygon
import numpy as np
import xarray
import csv
import os

from datetime import datetime
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
os.environ["PROJ_LIB"] = "C:\\"

#%% Arctic Sea Ice Data

data_r = xarray.open_dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc")
data = Dataset("arctic_seaice_climate_indicators_nh_v01r01_1979-2017.nc", mode='r')
latitude = data.variables["latitude"][:]
longitude = data.variables["longitude"][:]
data.close()

#%% Set-up Basemap
  
m = Basemap(width=18.e6,height=9.e6, projection='gnom',lat_0=90.,lon_0=20., resolution='l')
m.drawmapboundary(fill_color='#13003D')
m.drawcoastlines(linewidth=0.50)
m.fillcontinents(color='#8b8b8b',lake_color='#8b8b8b')
m.drawparallels(np.arange(10,90,5), labels=[True,False,False,False])
m.drawmeridians(np.arange(-180,180,25), labels=[False,False,False,True])

xi, yi = m(longitude, latitude)
xi = xi.filled()
yi = yi.filled()

#%% Crop Regions

def draw_poly(lats, lons):
    x, y = m( lons, lats )
    xy = zip(x,y)
    return xy
    
#%% Regions

# Format:
#longitude = [lonmin,lonmax,lonmax,lonmin,lonmin]
#latitude = [latmin,latmin,latmax,latmax,latmin]

# Canadian Arctic: -130.0,56.0,-70.0,83.0
longitude_cad = [-70, -130, -130, -70, -70]
latitude_cad = [49, 49, 82, 82, 49]
canadian_arctic = draw_poly(latitude_cad, longitude_cad)

# Kuroshiro: 115.0,24.0,165.0,64.0
longitude_kuroshio = [135, 165, 165, 135, 135]
latitude_kuroshio = [42, 42, 65, 65, 42]
kuroshio_current = draw_poly(latitude_kuroshio, longitude_kuroshio)

# Gulf Stream: -86.0,19.0,-48.0,51.0
longitude_gulf = [-48, -75, -75, -48, -48]
latitude_gulf = [40, 40, 65, 65, 40]
gulf_stream = draw_poly(latitude_gulf, longitude_gulf)

# North Pacific: 115,35.0,-120.0,60.0
longitude_pacific = [-150, 162, 162, -150, -150]
latitude_pacific = [50, 50, 69, 69, 50]
pacific = draw_poly(latitude_pacific, longitude_pacific)

# Arctic 1:
longitude_arctic1 = [-128, 150, 150, -128, -128]
latitude_arctic1 = [64, 64, 82, 82, 64]
arctic1 = draw_poly(latitude_arctic1, longitude_arctic1)

# Arctic 2:
longitude_arctic2 = [65, 150, 150, 65, 65]
latitude_arctic2 = [66, 66, 82, 82, 66]
arctic2 = draw_poly(latitude_arctic2, longitude_arctic2)

# Barents Sea:
longitude_wv = [20, 55, 55, 20, 20]
latitude_wv = [70, 70, 83, 83, 70]
wv = draw_poly(latitude_wv, longitude_wv)

# Greenland Sea:
longitude_ds =  [-40, 20, 20, -40, -40]
latitude_ds = [68, 68, 83, 83, 68]
ds = draw_poly(latitude_ds, longitude_ds)

# Denmark Strait:
longitude_strait =  [-50, -20, -20, -50, -50]
latitude_strait = [55, 55, 70, 70, 55]
strait = draw_poly(latitude_strait, longitude_strait)

#%% Plot

poly1 = Polygon(list(canadian_arctic), alpha=0.4, label="Canadian Arctic", facecolor='red')
poly2 = Polygon(list(kuroshio_current), alpha=0.4, label="Japan/Okhotsk Seas", facecolor='cyan')
poly3 = Polygon(list(gulf_stream), alpha=0.4, label="Labrador Sea", facecolor='green')
poly4 = Polygon(list(pacific), alpha=0.4, label="Chukchi/Bering Seas", facecolor='yellow')
poly5 = Polygon(list(arctic1), alpha=0.4, label="Siberian/Beaufort Seas", facecolor='lime')
poly6 = Polygon(list(arctic2), alpha=0.4, label="Kara/Laptev Seas", facecolor='fuchsia')
poly7 = Polygon(list(wv), alpha=0.4, label="Barents Sea", facecolor='orange')
poly8 = Polygon(list(ds), alpha=0.4, label="Greenland Sea", facecolor='darkviolet')
poly9 = Polygon(list(strait), alpha=0.4, label="Denmark Strait", facecolor='blue')

plt.gca().add_patch(poly1)
plt.gca().add_patch(poly2)
plt.gca().add_patch(poly3)
plt.gca().add_patch(poly4)
plt.gca().add_patch(poly5)
plt.gca().add_patch(poly6)
plt.gca().add_patch(poly7)
plt.gca().add_patch(poly8)
plt.gca().add_patch(poly9)

plt.title(r"Regions", fontsize=13)
plt.gcf().set_size_inches(12, 5.5)
plt.legend(loc='lower right', fontsize=10)
plt.show()