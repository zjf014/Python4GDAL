#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from osgeo import gdal

def Ex2_1():    
    rds = gdal.Open("./Data/ls8/LC08_L1TP_119033_20180428_20180502_01_T1_B4.TIF")
    band = rds.GetRasterBand(1)

def Ex2_2():
    rds = gdal.Open("./Data/ls8/LC08_L1TP_119033_20180428_20180502_01_T1_B4.TIF")
    array = rds.ReadAsArray(2500,2500,3,3)
    print(array)

def Ex2_3():
    rds = gdal.Open("./Data/ls8/LC08_L1TP_119033_20180428_20180502_01_T1_B4.TIF")
    band = rds.GetRasterBand(1)
    array = band.ReadAsArray(2500,2500,5,5)
    print(array)
    array = band.ReadAsArray(2500,2500,5,5,10,10)
    print(array)


if __name__ == "__main__":
    Ex2_2()
    Ex2_3()
