"""Clip a raster image using a shapefile"""

# http://git.io/vqsRH

import operator
from osgeo import gdal, gdal_array, osr
import shapefile
try:
    import Image
    import ImageDraw
except:
    from PIL import Image, ImageDraw

def imageToArray(i):
    """
    Converts a Python Imagings Library array to a gdal_array image.
    """
    #a = gdal_array.numpy.fromstring(i.tostring(), 'b')
    a = gdal_array.numpy.frombuffer(i.tobytes(), 'b')
    a.shape = i.im.size[1], i.im.size[0]
    return a


def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / abs(yDist))
    return (pixel, line)


def ClipImage(raster,shp,output):

    # Load the source data as a gdal_array array
    srcArray = gdal_array.LoadFile(raster)

    # Also load as a gdal image to get geotransform (world file) info
    srcImage = gdal.Open(raster)
    geoTrans = srcImage.GetGeoTransform()

    # Use pyshp to open the shapefile
    r = shapefile.Reader(shp)

    # Convert the layer extent to image pixel coordinates
    minX, minY, maxX, maxY = r.bbox
    ulX, ulY = world2Pixel(geoTrans, minX, maxY)
    lrX, lrY = world2Pixel(geoTrans, maxX, minY)
    print(ulX, ulY, lrX, lrY)

    # Calculate the pixel size of the new image
    pxWidth = int(lrX - ulX)
    pxHeight = int(lrY - ulY)
    clip = srcArray[:, ulY:lrY, ulX:lrX]

    # Create a new geomatrix for the image
    # to contain georeferencing data
    geoTrans = list(geoTrans)
    geoTrans[0] = minX
    geoTrans[3] = maxY

    # Map points to pixels for drawing the county boundary
    # on a blank 8-bit, black and white, mask image.
    pixels = []
    for p in r.shape(0).points:
        pixels.append(world2Pixel(geoTrans, p[0], p[1]))
    rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)

    # Create a blank image in PIL to draw the polygon.
    rasterize = ImageDraw.Draw(rasterPoly)
    rasterize.polygon(pixels, 0)

    # Convert the PIL image to a NumPy array
    mask = imageToArray(rasterPoly)

    # Clip the image using the mask
    clip = gdal_array.numpy.choose(mask, (clip, 0)).astype(
                                    gdal_array.numpy.uint8)

    # Save ndvi as tiff
    output = gdal_array.SaveArray(clip, "./Data/{}.tif".format(output),
                          format="GTiff", prototype=raster)
    output = None
    return geoTrans

def TransGeo(raster,output,geoTrans):
    sds = gdal.Open("./Data/{}.tif".format(raster))
    im_geotrans = sds.GetGeoTransform()
    im_proj = sds.GetProjection()
    im_data = sds.ReadAsArray()
    im_width = sds.RasterXSize
    im_height = sds.RasterYSize
    im_bands = sds.RasterCount
    band1 = sds.GetRasterBand(1)
    datatype = band1.DataType

    myArray = gdal_array.LoadFile("./Data/{}.tif".format(raster))

    geoTrans = [350543.58083010436, 30.0, 0.0, 4324830.653359352, 0.0, -30.0]

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create("./Data/{}.tif".format(output), im_width, im_height, im_bands, datatype)
    dataset.SetProjection(im_proj)  # 写入投影
    dataset.SetGeoTransform(geoTrans)  # 写入仿射变换参数
    dataset.GetRasterBand(1).WriteArray(myArray[0,:])  # 写入数组数据
    dataset.GetRasterBand(2).WriteArray(myArray[1,:])
    dataset.GetRasterBand(3).WriteArray(myArray[2,:])

    dataset = None
    sds = None



if __name__ == "__main__":
   
    raster = "./Data/fushion.tif"   # Raster image to clip    
    shp = "./Data/shp/dalian_pro.shp"  # Polygon shapefile used to clip    
    output = "fushion_clip"  # Name of clipped raster file(s)
    trans = "fushion_clip_trans"
    geoTrans = ClipImage(raster,shp,output)
    TransGeo(output,trans,geoTrans)
