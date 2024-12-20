import geopandas as gpd
import pandas as pd
from pathlib import Path

from .utils import get_gpkg_path


def load_USStates():
    us_states = gpd.read_file(get_gpkg_path())
    return us_states


def get_intersecting_states(study_area, us_states):
    study_area = study_area.to_crs(us_states.crs)
    intersecting_states = us_states[
        us_states.geometry.intersects(study_area.unary_union)
    ]
    return intersecting_states


# Check if the boundary is in a single state or multiple states
def getstates(boundary_file):
    boundary = gpd.read_file(boundary_file)
    us_states = load_USStates()
    intersecting_states = get_intersecting_states(boundary, us_states)
    if len(intersecting_states) > 1:
        return intersecting_states["STATE"].tolist()
    elif len(intersecting_states) == 1:
        return [intersecting_states.iloc[0]["STATE"]]
    else:
        raise ValueError("The boundary does not intersect any US states.")


# Get building footprints for a single or multiple states
def BFonboundary(country, states, boundary_file):
    from .buildingfootprint import getBF

    all_buildings = []
    for state in states:
        country_state = f"{country}/{state}"
        geojson_data = getBF(country_state, boundary_file)
        buildings_gdf = gpd.GeoDataFrame.from_features(
            geojson_data["features"], crs="EPSG:4326"
        )
        all_buildings.append(buildings_gdf)

    # Combine all GeoDataFrames into one
    combined_buildings = gpd.GeoDataFrame(
        pd.concat(all_buildings, ignore_index=True), crs="EPSG:4326"
    )
    return combined_buildings
