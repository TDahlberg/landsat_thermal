lansdsat_thermal
================

ArcMap toolbox that converts Landsat 5 and 7 band 6 imagery downloaded from the glovis.usgs.gov from Digital Numbers to Land Surface Temperature Tiffs in Kelvin and Celcius. Also calculates NDVI images from red and nir bands, and also performs a correlation between NDVI and land surface temperature.


Requires 3 input parameters:
  
  	rasterinputdirectory = directory where the unzipped directory of Landsat images is located 
  
  	radianceup = upwelling radiance, parameter derived from NASA Atmospheric Parameter Calculator
  
  	radiancedown = downwelling radiance, "" ""
  
  
Add the toolbox to ArcMap, and then:

	1. Download an image from glovis.usgs.gov through the bulk download application
	2. Unzip the downloaded image from its tar.gz format into a directory
	3. Open the metadata (...MTL.txt)
	4. Navigate to http://atmcorr.gsfc.nasa.gov/ and input the required parameters based on the image metadata
	5. The tool will send you an email and also immediately display results containing up- and downwelling radiance
	6. Enter upwelling radiance, downwelling radiance, and Landsat band directory into the script and run.


