# Sentinel-Scripts

Source for Sentinel-Scripts/Sentinel 2/Scripts/gdal_merge.py
[gdal_merge.py](https://svn.osgeo.org/gdal/trunk/gdal/swig/python/scripts/gdal_merge.py)


S2 examples
------------

Here are a few examples for Sentinel-2 Level 2a products.

To generated merged tif run tiff-generator.py and input path to zipped product when prompted.

```sh

$ python3 tiff-generator.py
$ Input Path? Inputs/S2A_OPER_PRD_MSIL1C_PDMC_20160527T131839_R080_V20150728T113618_20150728T113618.zip

```

This will generate a resampled(20m) geotif containg all band in the order
1
2
3
4
5
6
7
8
9
10
11
12
8A

