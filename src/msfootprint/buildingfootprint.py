# Importing necessary libraries
import geemap
import ee
import os
from shapely.geometry import box
import pandas as pd
from pathlib import Path
import geopandas as gpd
from pyspark.sql import SparkSession
from shapely.wkt import loads
import shutil

from .find_footprinttable import get_intersecting_states
from .find_footprinttable import load_USStates

# Suppress the warnings
import warnings

warnings.filterwarnings("ignore")

# %%
# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize()
geemap.ee_initialize()


# %%
def FindTableorFolder(country):
    asset_path = f"projects/sat-io/open-datasets/MSBuildings/{country}"
    try:
        assets = ee.data.listAssets({"parent": asset_path})
        if assets and "assets" in assets and assets["assets"]:
            print(
                f"\033[1m'{country}' is a folder and contains the following tables. Please specify one table as: US/table_name to retrieve the building footprint:\033[0m"
            )
            for asset in assets["assets"]:
                print(f"\033[1m - {asset['id'].split('/')[-1]}\033[0m")
        else:
            # If no nested assets, check if it's a direct table
            print(
                f"\033[1mNo nested assets found for '{country}'. Checking if it's a direct table...\033[0m"
            )
            try:
                collection = ee.FeatureCollection(asset_path)
                print(
                    f"\033[1m'{country}' is a direct table. You can use it directly.\033[0m"
                )
            except Exception as e:
                print(
                    f"\033[1mError: '{country}' is neither a folder nor a valid table. Details: {e}\033[0m"
                )
    except Exception as e:
        print(
            f"\033[1m'{country}' does not appear to be a folder. Checking if it's a direct table...\033[0m"
        )
        try:
            collection = ee.FeatureCollection(asset_path)
            print(
                f"\033[1m'{country}' is a direct table. You can use it directly.\033[0m"
            )
        except Exception as inner_e:
            print(
                f"\033[1mError: '{country}' is neither a folder nor a valid table. Details: {inner_e}\033[0m"
            )


# %%
def split_into_tiles(boundary, tile_size=0.1):
    bounds = boundary.total_bounds
    x_min, y_min, x_max, y_max = bounds
    tiles = []
    x = x_min
    while x < x_max:
        y = y_min
        while y < y_max:
            tile = box(x, y, x + tile_size, y + tile_size)
            if tile.intersects(boundary.unary_union):
                tiles.append(tile)
            y += tile_size
        x += tile_size
    return gpd.GeoDataFrame(geometry=tiles, crs=boundary.crs)


# Merge the final geojson files
def mergeGeoJSONfiles(output_dir, merged_file):
    output_dir = Path(output_dir)
    files = list(output_dir.glob("*.geojson"))
    gdfs = [gpd.read_file(file) for file in files]
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs="EPSG:4326")
    merged_gdf.to_file(merged_file, driver="GPKG")


# Process each batch with number of tiles
def process_batch(partition, collection_name, output_dir, boundary_wkt):
    ee.Initialize()

    # Convert WKT boundary to geometry
    boundary = loads(boundary_wkt)
    results = []

    for tile_wkt in partition:
        try:
            tile = loads(tile_wkt)
            aoi = ee.Geometry(tile.__geo_interface__)
            collection = ee.FeatureCollection(collection_name).filterBounds(aoi)

            # Download features and filter by boundary
            gdf = geemap.ee_to_gdf(collection)
            gdf = gdf[gdf.geometry.intersects(boundary)]

            # Save each tile as a GeoJSON file
            tile_id = f"tile_{hash(tile)}"
            output_file = Path(output_dir) / f"{tile_id}.geojson"
            gdf.to_file(output_file, driver="GeoJSON")
            results.append(f"Saved: {output_file}")
        except Exception as e:
            results.append(f"Error processing tile: {e}")

    return results


def getBuildingFootprintSpark(country, boundary_file, out_dir, tile_size):
    spark = SparkSession.builder.appName("BuildingFootprints").getOrCreate()

    # Make temporary directory
    temp_dir = out_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Load and process boundary
    boundary = gpd.read_file(boundary_file).to_crs("EPSG:4326")
    tiles = split_into_tiles(boundary, tile_size)
    boundary_wkt = boundary.unary_union.wkt

    # Collection name(s)
    if country == "US":
        us_states = load_USStates()
        states = get_intersecting_states(boundary, us_states)["STATE"].tolist()
        collection_names = [
            f"projects/sat-io/open-datasets/MSBuildings/{country}/{state}"
            for state in states
        ]
    else:
        collection_names = [f"projects/sat-io/open-datasets/MSBuildings/{country}"]

    # Distribute processing
    for collection_name in collection_names:
        tiles_rdd = spark.sparkContext.parallelize(
            tiles.geometry.apply(lambda x: x.wkt).tolist(), numSlices=10
        )
        results = tiles_rdd.mapPartitions(
            lambda partition: process_batch(
                partition, collection_name, str(temp_dir), boundary_wkt
            )
        ).collect()

    # Merge GeoJSON files
    mergeGeoJSONfiles(temp_dir, out_dir / "building_footprint.gpkg")

    # Clean up the temp directory
    shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"Building footprint data saved to {out_dir / 'building_footprint.gpkg'}")


# %%
# Export the building footprint
def getBuildingFootprint(country, ROI, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = out_dir / "building_footprint.gpkg"

    if filename.exists():
        os.remove(filename)

    getBuildingFootprintSpark(country, ROI, out_dir, tile_size=0.05)
