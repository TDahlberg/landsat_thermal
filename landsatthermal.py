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


##import arcpy                # Imports the ArcGIS Python bindings
##from arcpy.sa import *      # Imports modules from ArcGIS Spatial Analyst
import os
import glob                 # Imports Module that looks through directories
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *

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

    newpath = inputrasterdirectory+'\\'+'results'
    if not os.path.exists(newpath): os.makedirs(newpath) # Creates directory
    ##arcpy.env.overwriteOutput = True                     #turns on overwriting
    ##arcpy.CreateFolder_management(inputrasterdirectory,'work')
    ##arcpy.env.workspace = arcpy.env.ScratchWorkspace = inputrasterdirectory + \
    '\\' + 'results'
    ##arcpy.CheckOutExtension('spatial')



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
        dataset = gdal.Open(item, GA_ReadOnly)  # opens raster in GDAL
    outFile = "output.tiff" #creates an output file placeholder

    # Reads the dataset into a band
    band = dataset.GetRasterBand(1)  #Retreives band 1 from dataset

    # Reads the data into a Numpy Array
    data = BandReadAsArray(band)

    # Converts the raster image from DN values to top-of-atmosphere
    # radiance and stores it in memory
    qcalmax = 255     # Given
    qcalmin = 1       # Given
    TOA = (((lmax - lmin) / (qcalmax - qcalmin)) * (data - qcalmin)) + lmin


    # Converts top-of-atmosphere radiance to surface-leaving radiance and \
    # stores it in memory. radianceup and radiancedown are parameters from
    # the NASA Atmospheric Parameter Calculator.
    emissivity = 0.95            # Assumed emissivity from the YALE paper
    transmissivity = 0.66        # Assumed transmissivity from the YALE paper
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


    # Writes the kelvin output file
    driver = gdal.GetDriverByName('GTiff')  # Calls the GDAL tiff creator
    kelvinOut = driver.Create("temp_k.tiff", dataset.RasterXSize,
    dataset.RasterYSize, 1, band.DataType)
    CopyDatasetInfo(dataset,kelvinOut)
    bandOutK = kelvinOut.GetRasterBand(1)
    BandWriteArray(bandOut,tempkelvin)

    # Writes the celcius output file
    driver = gdal.GetDriverByName('GTiff')  # Calls the GDAL tiff creator
    celciusOut = driver.Create("temp_c.tiff", dataset.RasterXSize,
    dataset.RasterYSize, 1, band.DataType)
    CopyDatasetInfo(dataset,celciusOut)
    bandOutC = celciusOut.GetRasterBand(1)
    BandWriteArray(bandOut,tempcelcius)


    ##arcpy.CheckInExtension('spatial') # This releases the hold on the license
    ##print "Thermal conversion finished"

print landsatthermal('D:\Landsat Downloader\Downloads\LE70290302002347EDC00.tar\LE70290302002347EDC00',2.84,4.49)
