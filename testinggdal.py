#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tdahlberg
#
# Created:     02/12/2013
# Copyright:   (c) tdahlberg 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *

gdal.AllRegister()
dataset = gdal.Open("D:\Landsat Downloader\Downloads\LE70290302002347EDC00.tar\LE70290302002347EDC00\LE70290302002347EDC00_B1.TIF",
GA_ReadOnly)
if dataset is None:
   print "Couldn't open file"
   sys.exit(1)
band = dataset.GetRasterBand(1)

print type(dataset)
print type(band)
bandtype = gdal.GetDataTypeName(band.DataType)
print bandtype

dataset = None