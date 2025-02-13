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
