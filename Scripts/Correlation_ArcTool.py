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
from arcpy import env
from arcpy.sa import *      # Imports modules from ArcGIS Spatial Analyst
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
from arcpy import env

import os
import glob                 # Imports Module that looks through directories


# Set the working directory below, using one of two options (comment out the other)
# inputrasterdirectory = 'C:\Users\mcecil\Desktop\Landsat' # Option (1), set working directory directly
inputrasterdirectory = arcpy.GetParameterAsText (0) # Option (2), set working directory using an input tool in ArcGIS

env.workspace = inputrasterdirectory # sets the working directory


# This function parses through a Landsat 5 file folder, identfies Bands 3 and 4
# and creates an NDVI image.

outStatFile = inputrasterdirectory+'\\'+'Correlation Results' +'\\' + 'correlationStats.txt' # name of output statistics file

def correlation(inputrasterdirectory):
    newpath = inputrasterdirectory+'\\'+'Correlation Results'
    if not os.path.exists(newpath): os.makedirs(newpath) # creates a working folder within the input directory
    for item in glob.glob(inputrasterdirectory+'\\'+'NDVI Results' + '\\*ndvi*.TIF'):
        ndvi = arcpy.Raster(item) # puts ndvi image in a variable
    for item in glob.glob(inputrasterdirectory+'\\'+'Thermal Conversion Results'+'\\*temp_k*.TIF'):
        kelvin = arcpy.Raster(item) # puts temperature image (kelvin) in a variable
    BandCollectionStats([ndvi, kelvin], outStatFile, "DETAILED") # calculates correlation statistics
    print "Correlation finished"



print correlation(inputrasterdirectory) # this statement runs the function




