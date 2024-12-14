import os
from qgis.core import QgsApplication, QgsProcessingFeatureSourceDefinition
from qgis import processing

if __name__=="__main__":
    # Initialize QGIS Application
    QgsApplication.setPrefixPath("/usr", True)  # Adjust based on your install path
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Define paths
    input_raster_path = '/mnt/storage/datmh/AI4SmallFarms/input/asia/test/patches/mosaic/8.tif'  # Replace with your raster file path
    polygon_output_path = '/mnt/storage/datmh/AI4SmallFarms/input/asia/test/patches/mosaic/polygons.shp'  # Output vector file path
    simplified_output_path = '/mnt/storage/datmh/AI4SmallFarms/input/asia/test/patches/mosaic/simplified_polygons.shp'  # Output simplified file path

    # Step 1: Polygonize Raster
    params_polygonize = {
        'INPUT': input_raster_path,
        'BAND': 1,
        'EIGHT_CONNECTEDNESS': False,
        'OUTPUT': polygon_output_path
    }
    processing.run("gdal:polygonize", params_polygonize)

    # Step 2: Simplify Polygons
    params_simplify = {
        'INPUT': polygon_output_path,
        'TOLERANCE': 10.0,  # Set tolerance for Douglas-Peucker simplification
        'OUTPUT': simplified_output_path
    }
    processing.run("qgis:simplifygeometries", params_simplify)

    # Exit QGIS when done
    qgs.exitQgis()