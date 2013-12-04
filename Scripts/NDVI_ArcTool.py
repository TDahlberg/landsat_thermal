#-------------------------------------------------------------------------------
# Name:        Landsat Thermal Conversion Script
# Purpose:
#
# Authors:     Tyler Dahlberg, Ryan Williams, Mike Cecil
#
# Created:     29/11/2013
# Copyright:
# Licence:     <your licence>
#-------------------------------------------------------------------------------



def main():
    pass




if __name__ == '__main__':
    main()



import arcpy                # Imports the ArcGIS Python bindings
from arcpy.sa import *      # Imports modules from ArcGIS Spatial Analyst
arcpy.CheckOutExtension("Spatial")

from arcpy import env

import os
import glob                 # Imports Module that looks through directories
arcpy.env.overwriteOutput = True

# Set the working directory below, using one of two options (comment out the other)
# inputrasterdirectory = 'C:\Users\mcecil\Desktop\Landsat' # Option (1), set working directory directly
inputrasterdirectory = arcpy.GetParameterAsText (0) # Option (2), set working directory using an input tool in ArcGIS

env.workspace = inputrasterdirectory # sets the working directory


# This function parses through a Landsat 5 file folder, identfies Bands 3 and 4
# and creates an NDVI image.

def landsatNDVI(inputrasterdirectory):
    newpath = inputrasterdirectory+'\\'+'NDVI Results'
    if not os.path.exists(newpath): os.makedirs(newpath) # creates a working folder within the input directory
    
    for item in glob.glob(inputrasterdirectory+'\*B4*.TIF'):
        band4 = arcpy.Raster(item) # put band 4 (infrared) in a variable

    for item in glob.glob(inputrasterdirectory+'\*B3*.TIF'):
        band3 = arcpy.Raster(item) # put band 3 (red) in a varible
        
    above = arcpy.sa.Float(band4 - band3) # NDVI numerator
    below = arcpy.sa.Float(band4 + band3) # NDVI denominator
    ndvi = above/below 
    ndvi.save(newpath + '\\' + 'ndvi.tif') # save ndvi as a tif
    print "NDVI Conversion Finished"
    
    ndvi_layer = arcpy.mapping.Layer(newpath + '\\' + 'ndvi.tif') 
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    arcpy.mapping.AddLayer(df, ndvi_layer)

print landsatNDVI(inputrasterdirectory) # this statement runs the function




