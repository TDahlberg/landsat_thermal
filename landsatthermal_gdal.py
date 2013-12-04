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
"""
def main():
    pass

if __name__ == '__main__':
    main()
"""


import sys, os, struct
import osgeo.gdal as gdal
import glob                 # Imports Module that looks through directories
import numpy


# Function to parse through a Landsat 5 file folder downloaded from USGS
# Bulk Downloader, identify the correct thermal image, identify its metadata,
# and convert it from a DN value image to Top-of-Atmosphere radiance, to
# Surface-Leaving radiance, to thermal values in degrees kelvin and celcius
# and output the resulting images into a new directory.

# This function requires that you use emissivity and transmissivity, as well as
# upwelling and downwelling radiances. These can all be obtained by entering
# the date and dimensions of the image you downloaded into NASA's Atmospheric
# Correction Parameter Calculator located at http://atmcorr.gsfc.nasa.gov/



def createOutputImage(outFilename,inDataset):
    driver = gdal.GetDriverByName('GTiff')
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
       print 'Driver GTiff supports Create() method.'
    else:
       print 'Driver GTiff does not support Create().'
       sys.exit(-1)
    geoTransform = inDataset.GetGeoTransform()
    geoProjection = inDataset.GetProjection()
    newDataset = driver.Create(outFilename, inDataset.RasterXSize,\
    inDataset.RasterYSize, 1, gdal.GDT_Float32)
    newDataset.SetGeoTransform(geoTransform)
    newDataset.SetProjection(geoProjection)
    return newDataset



def calcTemp(inputrasterdirectory,radianceup,radiancedown,outputrasterdirectory):
	#newpath = inputrasterdirectory+'\\'+'results'
	#if not os.path.exists(newpath): os.makedirs(newpath) # Creates directory
	# Searches directory for metadata text and reads Lmin and Lmax from it
    outFilename = 'thermal'

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
	    dataset = gdal.Open(str(item), gdal.GA_ReadOnly)

    # Creates output dataset
    outDataset = createOutputImage(outFilename,dataset)
    band = dataset.GetRasterBand(1) # Gets thermal band
    numLines = band.YSize  # Gets number of lines in image

    # Loops through each line in the image in order to keep memory
    # requirements down
    for line in range(numLines):

        # Defines variable for output lines
        outputLine = ''

        # Reads information from band
        band_scanline = band.ReadRaster(0,line,band.XSize,1,band.XSize,1,
        gdal.GDT_Float32)

        # Unpacks the line data as floating point data with 'struct'
        band_tuple = struct.unpack('f' * band.XSize, band_scanline)

        #Sets up constants for equations
        emissivity = 0.95      # Assumed emissivity from the YALE paper
        transmissivity = 0.66  # Assumed transmissivity from the YALE paper
        qcalmax = 255          # Given
        qcalmin = 1            # Given
        k1 = 607.76            # Temperature for blackbody conversion
        k2 = 1260.56           # Temperature for blackbody conversion
        # Loops through the columns inside the image
        for i in range(len(band_tuple)):

        # Runs all the calculations to convert from DN -> LST
        # Converts the raster image from DN values to top-of-atmosphere
        # radiance and stores it in memory

            TOA = (((lmax - lmin) / (qcalmax - qcalmin)) * (band_tuple[i] \
		    - qcalmin)) + lmin

            # Converts top-of-atmosphere radiance to surface-leaving radiance and \
		    # stores it in memory. radianceup and radiancedown are parameters from
		    # the NASA Atmospheric Parameter Calculator.

            SLR = ((TOA - radianceup)/(emissivity * transmissivity)) - ((1 \
		    - emissivity) / (emissivity)) * radiancedown
            tempkelvin = k2 / (numpy.log(( k1 / SLR) + 1 )) #SLR -> Kelvin
            tempcelcius = tempkelvin - 273.15              #Kelvin -> Celcius

            # Adds current calcualted pixels to output lines
            outputLine_k = outputLine + struct.pack('f',tempkelvin)
            outDataset.GetRasterBand(1).WriteRaster(0,line,band.XSize,1,\
            outputLine_k, buf_xsize = band.XSize, buf_ysize = 1,\
            buf_type = gdal.GDT_Float32)
            del outputLine_k

            print 'Temperature in Degrees Kelvin calculated.'
            print "Thermal conversion finished"

inputrasterdirectory = 'D:\Landsat Downloader\Downloads\LE70290302002347EDC00.tar\LE70290302002347EDC00'
outputrasterdirectory = inputrasterdirectory+'\\'+'results'
radianceup = 2.84
radiancedown = 4.49

print calcTemp(inputrasterdirectory,radianceup,radiancedown,outputrasterdirectory)



