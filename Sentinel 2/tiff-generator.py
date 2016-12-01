import sys
import subprocess
sys.path.append('Scripts/')
import gdal_merge
import zipfile  
import os
import time
import readline, glob
from pathlib import Path

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def generate_geotiffs(inputProductPath, outputPath):

	basename =  os.path.basename(inputProductPath)
	if os.path.isdir(outputPath + basename[:-3] + "SAFE") :
		print('Already extracted')
	else:
		zip = zipfile.ZipFile(inputProductPath) 
		zip.extractall(outputPath) 
		print("Extracting Done") 

	
	directoryName = outputPath + basename[:-3] + "SAFE/GRANULE"

	productName = os.path.basename(inputProductPath)[:-4]
	outputPathSubdirectory = outputPath + productName + "_PROCESSED"

	if not os.path.exists(outputPathSubdirectory):
		os.makedirs(outputPathSubdirectory)

	subDirectorys = get_immediate_subdirectories(directoryName)

	results = []

	for granule in subDirectorys:
		unprocessedBandPath = outputPath + productName + ".SAFE/GRANULE/" + granule + "/" + "IMG_DATA/"
		results.append(generate_all_bands(unprocessedBandPath, granule, outputPathSubdirectory))
	
	#gdal_merge.py -n 0 -a_nodata 0 -of GTiff -o /home/daire/Desktop/merged.tif /home/daire/Desktop/aa.tif /home/daire/Desktop/rgbTiff-16Bit-AllBands.tif
	merged = outputPathSubdirectory + "/merged.tif"
	params = ['',"-of", "GTiff", "-o", merged]

	for granule in results:
		params.append(granule)

	gdal_merge.main(params)


def generate_all_bands(unprocessedBandPath, granule, outputPathSubdirectory):

	granuleBandTemplate =  granule[:-6]

	outputPathSubdirectory = outputPathSubdirectory 
	if not os.path.exists(outputPathSubdirectory+ "/IMAGE_DATA"):
		os.makedirs(outputPathSubdirectory+ "/IMAGE_DATA")
	
	outPutTiff = '/'+granule[:-6]+'16Bit-AllBands.tif'
	outPutVRT = '/'+granule[:-6]+'16Bit-AllBands.vrt'

	outPutFullPath = outputPathSubdirectory + "/IMAGE_DATA/" + outPutTiff
	outPutFullVrt = outputPathSubdirectory + "/IMAGE_DATA/" + outPutVRT
	inputPath = unprocessedBandPath + granuleBandTemplate

	bands = {"band_01" :  inputPath + "B01.jp2",
	"band_02" :  inputPath + "B02.jp2",
	"band_03" :  inputPath + "B03.jp2",
	"band_04" :  inputPath + "B04.jp2",
	"band_05" :  inputPath + "B05.jp2",
	"band_06" :  inputPath + "B06.jp2",
	"band_07" :  inputPath + "B07.jp2",
	"band_08" :  inputPath + "B08.jp2",
	"band_8A" :  inputPath + "B8A.jp2",
	"band_09" :  inputPath + "B09.jp2",
	"band_10" :  inputPath + "B10.jp2",
	"band_11" :  inputPath + "B11.jp2",
	"band_12" :  inputPath + "B12.jp2"}


	cmd = ['gdalbuildvrt', '-resolution', 'user', '-tr' ,'20', '20', '-separate' ,outPutFullVrt]


	for band in sorted(bands.values()):
		cmd.append(band)
           
	my_file = Path(outPutFullVrt)
	if not my_file.is_file():
		# file exists
		subprocess.call(cmd)

	#, '-a_srs', 'EPSG:3857'
	cmd = ['gdal_translate', '-of' ,'GTiff', outPutFullVrt, outPutFullPath]

	my_file = Path(outPutTiff)
	if not my_file.is_file():
		# file exists
		subprocess.call(cmd)



	#params = ['', '-o', outPutFullPath, '-separate', band_01, band_02, band_03, band_04, band_05, band_06, band_07, band_08, band_8A, band_09, band_10, band_11, band_12]

	#gdal_merge.main(params)
	
	return(outPutFullPath)




outputPath = '../Output/'
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
inputPath = input("Input Path? ")

start_time = time.time()

generate_geotiffs(inputPath, outputPath)

print("--- %s seconds ---" % (time.time() - start_time))
