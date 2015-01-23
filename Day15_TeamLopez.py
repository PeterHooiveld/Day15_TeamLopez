### Team Lopez members: Bart Driessen & Peter Hooiveld  
### January 23, 2015

### Step 1: Import modules.
import os, urllib2, zipfile, requests,tarfile
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32

### Step 2: Download data.
    # Browse ; "https://www.dropbox.com/s/zb7nrla6fqi1mq4/LC81980242014260-SC20150123044700.tar.gz?dl=0"
    # Save and unpack in "/Data"
    
### Step 3: Open raster file
Data ={}
Data['4'] = gdal.Open("/home/user/Desktop/Day_15/Data/LC81980242014260LGN00_sr_band4.tif")
Data['5'] = gdal.Open("/home/user/Desktop/Day_15/Data/LC81980242014260LGN00_sr_band5.tif")


### Step 4: Extract bands in for loop and calculating NDWI.
LandSat = {}
for i in Data:
    band = Data[i]
    bandArr = band.ReadAsArray(0,0,Data[i].RasterXSize, Data[i].RasterYSize)
    bandArr = bandArr.astype(np.float32)
    LandSat["band"+str(i)] = bandArr
mask = np.greater((LandSat["band4"] +LandSat["band5"]),0 )
NDWI = np.choose(mask,(-99,(LandSat["band4"] - LandSat["band5"])/(LandSat["band4"] +LandSat["band5"])))

### Step 5: Cloudcover removal
Fmask = gdal.Open("/home/user/Desktop/Day_15/Data/LC81980242014260LGN00_cfmask.tif")
mask = np.greater(Fmask,1 )
NDWI_cloudless = np.choose(mask,(-99,NDWI))
 
 
### Step 6: Create output file.
driver = gdal.GetDriverByName('GTiff')
outDataSet=driver.Create('Data/NDWI.tif', Data['5'].RasterXSize, Data['5'].RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(NDWI_cloudless,0,0)
outBand.SetNoDataValue(-99)
outBand.FlushCache()
outDataSet.FlushCache()

### Step 7: Close GDAL files
Data['4'] = None
Data['5'] = None
Fmask = None

### Step 7: Plot map
    # We think this should work, but computer says memory problems.
import matplotlib.pyplot as plt
plt.imshow(NDWI_cloudless,cmap = plt.cm.jet)
plt.show()


