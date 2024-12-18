#Importing necessary libraries
import geemap
import ee 
from pathlib import Path
import geopandas as gpd
#%%
# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize()
geemap.ee_initialize()
# %%
#Change the boundary shapefile to a geojson file
def get_eesupported_roi(boundary_file):
    boundary_file = Path(boundary_file)
    valid_extensions = [".shp", ".gpkg", ".kml", ".geojson", ".json"]
    if boundary_file.suffix.lower() not in valid_extensions:
        raise ValueError(f"Unsupported file format: {boundary_file.suffix}. Supported formats are: {', '.join(valid_extensions)}")

    if boundary_file.suffix.lower() == ".kml":
        shp = gpd.read_file(boundary_file, driver="KML")
    else:
        shp = gpd.read_file(boundary_file)
    if shp.crs is None:
        raise ValueError("Input file has no CRS. Please ensure the file has a valid CRS.")
    shp = shp.to_crs(epsg=4326)
    roi_geom = shp.geometry.values[0]
    roi_geojson = roi_geom.__geo_interface__
    roi_ee = ee.Geometry(roi_geojson)
    return roi_ee

#%%
def FindTableorFolder(country):
    asset_path = f'projects/sat-io/open-datasets/MSBuildings/{country}'
    try:
        assets = ee.data.listAssets({'parent': asset_path})
        if assets and 'assets' in assets and assets['assets']:
            print(f"\033[1m'{country}' is a folder and contains the following tables. Please specify one table as: US/table_name to retrieve the building footprint:\033[0m")
            for asset in assets['assets']:
                print(f"\033[1m - {asset['id'].split('/')[-1]}\033[0m")
        else:
            # If no nested assets, check if it's a direct table
            print(f"\033[1mNo nested assets found for '{country}'. Checking if it's a direct table...\033[0m")
            try:
                collection = ee.FeatureCollection(asset_path)
                print(f"\033[1m'{country}' is a direct table. You can use it directly.\033[0m")
            except Exception as e:
                print(f"\033[1mError: '{country}' is neither a folder nor a valid table. Details: {e}\033[0m")
    except Exception as e:
        print(f"\033[1m'{country}' does not appear to be a folder. Checking if it's a direct table...\033[0m")
        try:
            collection = ee.FeatureCollection(asset_path)
            print(f"\033[1m'{country}' is a direct table. You can use it directly.\033[0m")
        except Exception as inner_e:
            print(f"\033[1mError: '{country}' is neither a folder nor a valid table. Details: {inner_e}\033[0m")
            
#%%
#GEE supported ROI
def getBF(country_name, study_area, out_dir):
    studyarea = get_eesupported_roi(study_area)
    collection_BF = ee.FeatureCollection(f'projects/sat-io/open-datasets/MSBuildings/{country_name}')
    filtered_buildings = collection_BF.filterBounds(studyarea)
    filename = out_dir / "building_footprint.geojson"
    geemap.ee_to_geojson(filtered_buildings, filename= filename)

#%%
# Export the building footprint
def getBuildingFootprint(country, ROI, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert EE FeatureCollection to GeoJSON and then to GeoPandas
    getBF(country, ROI, out_dir)
    print(f"Data saved to {out_dir}")