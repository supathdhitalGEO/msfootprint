import importlib.resources


def get_gpkg_path():
    resource_path = importlib.resources.files("msfootprint.data") / "us_boundary.gpkg"
    return resource_path
