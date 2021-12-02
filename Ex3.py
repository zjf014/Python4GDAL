from osgeo import gdal
import os


def get_dataset_band(bandfile):   
    input_dataset = gdal.Open(bandfile)
    input_band = input_dataset.GetRasterBand(1)
    return input_dataset, input_band

def Ex3():
    datasets = ['./Data/ls7/L71119033_03320030513_B20.TIF',
                './Data/ls7/L71119033_03320030513_B30.TIF',
                './Data/ls7/L71119033_03320030513_B40.TIF']
    bandfile = []
    bandnames=[]
    for ds in datasets:
        bandfile.append(ds)
        names=os.path.basename(ds)
        print(names)
        bandnames.append(names)

    inputdata=[]
    for i in range(len(bandfile)):
        inputdata.append(get_dataset_band(bandfile[i]))

    inputdataset_1, inputband_1 = inputdata[0]

    driver=gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create("./Data/fushion.tif", inputband_1.XSize, inputband_1.YSize, 3, inputband_1.DataType)
    output_dataset.SetProjection(inputdataset_1.GetProjection())
    output_dataset.SetGeoTransform(inputdataset_1.GetGeoTransform())

    for i in range(len(bandfile)):
         inputband_data = inputdata[i][1].ReadAsArray(0,0,inputband_1.XSize,inputband_1.YSize)
         raster_band = output_dataset.GetRasterBand(i + 1)
         raster_band.SetDescription(bandnames[i])
         raster_band.WriteArray(inputband_data,0,0)

    # output_dataset.BuildOverviews('average',[2,4,8,16,32])  #建立pyramid

if __name__ == "__main__":
    Ex3()
