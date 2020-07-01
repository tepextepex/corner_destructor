import os
import os.path
import gdal
import numpy as np
from scipy import ndimage
import argparse


def eliminate_corners(input_raster, output_dir=None):
    if output_dir is not None and os.path.isdir(output_dir):
        render = os.path.join(output_dir, "%s_render.tif" % os.path.basename(input_raster)[:-4])
    else:
        render = "%s_render.tif" % input_raster[:-4]

    ds = gdal.Warp("", input_raster, dstSRS="EPSG:4326", format="MEM")  # fixes the annoying non-zero skew parameter

    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()

    array = ds.GetRasterBand(1).ReadAsArray()

    binary_array = np.zeros_like(array, dtype=np.dtype("B"))
    binary_array[array > 0] = 1

    nogaps_array = ndimage.binary_fill_holes(binary_array)  # fills in small gaps in the image data

    new_nodata = -9999
    nodata_array = np.full(array.shape, new_nodata)

    masked_array = np.where(nogaps_array, array, nodata_array)

    driver = gdal.GetDriverByName("GTiff")

    out_ds = driver.Create(render, array.shape[1], array.shape[0], 1, gdal.GDT_Int16)
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(proj)
    out_ds.GetRasterBand(1).WriteArray(masked_array)
    out_ds.GetRasterBand(1).SetNoDataValue(new_nodata)

    out_ds.FlushCache()

    ds = None


def cli_eliminate_corners():
    parser = argparse.ArgumentParser()
    parser.add_argument("raster", help="Raster to process (full path)")
    parser.add_argument('-o', '--outdir', default=None,
                        help='output directory path (if not specified, the result will be stored in the same directory as the input raster)')
    args = parser.parse_args()
    eliminate_corners(args.raster, output_dir=args.outdir)


if __name__ == "__main__":
    # raster = "/home/tepex/NIERSC/IEPI/20200629/terrasar/dims_op_oc_dfd2_644615490_1/TSX-1.SAR.L1B/TSX1_SAR__MGD_RE___SC_S_SRA_20200629T021043_20200629T021103/IMAGEDATA/IMAGE_HH_SRA_wide_002.tif"
    # eliminate_corners(raster)
    cli_eliminate_corners()
