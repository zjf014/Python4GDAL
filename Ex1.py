#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from osgeo import gdal

def Ex1_1():
    drv_count = gdal.GetDriverCount()
    print(drv_count)
    for idx in range(drv_count):
        driver = gdal.GetDriver(idx)
        print("%10s: %s" % (driver.ShortName, driver.LongName))
      

def Ex1_2():
    
    driver = gdal.GetDriverByName("GTiff")
    rds = gdal.Open("./Data/ls8/LC08_L1TP_119033_20180428_20180502_01_T1_B4.TIF")
    # dir(rds)
    print(rds.GetMetadata())
    print(rds.GetDescription())
    print(rds.RasterCount)

    img_width,img_height=rds.RasterXSize,rds.RasterYSize
    print(img_width,img_height)

    print(rds.GetGeoTransform())
    print(rds.GetProjection())

    band = rds.GetRasterBand(1)
    print(band.XSize)
    print(band.YSize)
    print(band.DataType)

    print(band.GetStatistics(1,1))
    print(band.GetNoDataValue())
    # band.ComputeRasterMinMax()
    print(band.GetMaximum())
    print(band.GetMinimum())


if __name__ == '__main__':
    #Ex1_1()
    Ex1_2()

    
