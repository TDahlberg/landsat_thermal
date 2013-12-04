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

#Thermal Conversion
         # Open up an image
           #Look for "Layer_6"
           #Input upwelling radiance, downwelling radiance, emissivity
                  #Converts from TOA radiance > SL Radiance > Temperature in K


import arcpy                # Imports the ArcGIS Python bindings
from arcpy import env
from arcpy.sa import *      # Imports modules from ArcGIS Spatial Analyst
import glob                 # Imports Module that looks through directories
arcpy.env.overwriteOutput = True

# The following allows the script to be read by script tool parameters:
# 1: input workspace defined
# 2: input effective bandpass upwelling radiance
# 3: input effective bandpass downwelling radiance

inputrasterdirectory = arcpy.GetParameterAsText (0)
radianceupstr = arcpy.GetParameterAsText (1)
radiancedownstr = arcpy.GetParameterAsText (2)
env.workspace = inputrasterdirectory

#This converts string input into floating numbers for calculation

radianceup = float(radianceupstr)
radiancedown = float(radiancedownstr)

# Function to parse through a Landsat 5 file folder downloaded from USGS
# Bulk Downloader, identify the correct thermal image, identify its metadata,
# and convert it from a DN value image to Top-of-Atmosphere radiance, to
# Surface-Leaving radiance, to thermal values in degrees kelvin and celcius
# and output the resulting images into a new directory.

# This function requires that you use emissivity and transmissivity, as well as
# upwelling and downwelling radiances. These can all be obtained by entering
# the date and dimensions of the image you downloaded into NASA's Atmospheric
# Correction Parameter Calculator located at http://atmcorr.gsfc.nasa.gov/


def landsatthermal(inputrasterdirectory,radianceup,radiancedown):

    arcpy.env.overwriteOutput = True
    arcpy.CreateFolder_management(inputrasterdirectory,'Thermal Conversion Results')
    arcpy.env.workspace = arcpy.env.ScratchWorkspace = inputrasterdirectory +'\\' + 'Thermal Conversion Results'
    arcpy.CheckOutExtension('spatial')



    # Searches directory for metadata text and reads Lmin and Lmax from it
    for item in glob.glob(inputrasterdirectory+'\*MTL.txt'):
        with open(item, 'r') as f:
             for line in f:

                 if 'RADIANCE_MAXIMUM_BAND_6' in line:
                    print line
                    line = line.split('= ')
                    lmax = float(line[1])

                 elif 'RADIANCE_MINIMUM_BAND_6' in line:
                      print line
                      line = line.split('= ')
                      lmin = float(line[1])


    # Searches directory for landsat thermal images matching band 6
    for item in glob.glob(inputrasterdirectory+'\*B6*.TIF'):
        band6 = arcpy.Raster(item)                         # opens raster


    # Converts the raster image from DN values to top-of-atmosphere
    # radiance and stores it in memory
    qcalmax = 255     # Given
    qcalmin = 1       # Given
    TOA = (((lmax - lmin) / (qcalmax - qcalmin)) * (band6 - qcalmin)) + lmin


    # Converts top-of-atmosphere radiance to surface-leaving radiance and
    # stores it in memory
    emissivity = 0.95            # Assumed emissivity from the YALE paper
    transmissivity = 0.66        # Assumed transmissivity from the YALE paper
    # radianceup = 2.84            # From NASA atmcorr tool
    # radiancedown = 4.49          # From NASA atmcorr tool
    SLR = ((TOA - radianceup)/(emissivity * transmissivity)) - ((1 - emissivity)
    / (emissivity)) * radiancedown


    # Converts top-of-atmosphere radiance to Temperature in degrees
    # kelvin
    k1 = 607.76
    k2 = 1260.56
    tempkelvin = k2 / (arcpy.sa.Ln((k1/SLR)+1))

    #This equation converts temperature in degrees kelvin to temperature in
    #degrees fahrenheit
    tempcelcius = tempkelvin - 273.15
    tempkelvin2 = tempcelcius + 273.15
    # Saves the thermal results
    
    tempcelcius.save('temp_c.tif')
    tempkelvin.save('temp_k.tif')
    arcpy.CheckInExtension('spatial') # This releases the hold on the license
    print "Thermal conversion finished"

    #Displays them in ArcMap
    thermal_c_layer = arcpy.mapping.Layer(r"temp_c.tif")
    thermal_k_layer = arcpy.mapping.Layer(r"temp_k.tif")
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd) [0]
    arcpy.mapping.AddLayer(df, thermal_c_layer)
    arcpy.mapping.AddLayer(df, thermal_k_layer)

#This statement runs the function

print landsatthermal(inputrasterdirectory,radianceup,radiancedown)

