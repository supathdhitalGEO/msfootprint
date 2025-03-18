[![Version](https://img.shields.io/github/v/release/supathdhitalGEO/msfootprint)](https://github.com/supathdhitalGEO/msfootprint/releases)
![Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/supathdhitalGEO/msfootprint&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Views&edge_flat=false)
[![PyPI version](https://badge.fury.io/py/msfootprint.svg)](https://pypi.org/project/msfootprint/)
[![PyPI Downloads](https://static.pepy.tech/badge/msfootprint)](https://pepy.tech/projects/msfootprint)
[![DOI](https://zenodo.org/badge/905441761.svg)](https://doi.org/10.5281/zenodo.14597326)

## ```msfootprint```: A Python package for extracting Microsoft's global building footprints based on user-defined boundaries

This tool allows users to retrieve microsoft global building footprint data based on a specified boundary (such as a shapefile or GeoJSON). The footprints are then saved as Geopackage file to a specified output directory.

The computational engine of ```msfootprint``` leverages PySpark and split large areas into smaller tiles for parallel processing. Each tile is processed concurrently, significantly reducing execution time. PySpark's distributed architecture ensures efficient data handling and fault tolerance, enabling fast and reliable downloading of large geospatial datasets.  

### Features

- Supports multiple boundary input file formats: `.shp`, `.gpkg`, `.kml`, `.geojson`.
- Allows users to specify a boundary and retrieve building footprint data for a specific country or region or small study area.
- Faster downloading, feasible for large scale data download.
- Compatible with Google Earth Engine (GEE)/ required GEE authentications.

## Usage
**It needs a GEE account to access the data.**
  
To install the required dependencies, run the following:

```bash
pip install msfootprint
```

Once installed, 
import it in notebook or any python compiler.

```bash
import msfootprint as msf
```
**Initialize all the variables**
```bash
#Import all necessary things
import pathlib as Path
boundary_shp = Path('./shapefile_directory')
out_dir = Path('./output_directory')

#Import the 3 letter country ISO code of your study area, Eg. For Nepal, NPL, for United States of America it will be 'USA'
countryISO = 'USA'
```

**For US, it is automated, so no need to give statename but for other countries having multiple tables need to follow aforementioned step**

**Now, run the main script**
```bash
msf.BuildingFootprintwithISO(countryISO, boundary_shp, out_dir)
```
It will save the building footprint as geojson format in designated location.

**Sometimes if above code doesnot works and has a error on accessing data, it needs earth-engine projectID to access the building footprint data**
If so, 

```bash
#mention the ee projectID
geeprojectID = 'your-earth-engine-existing-projrct-id'

#run the code
msf.BuildingFootprintwithISO(countryISO, boundary_shp, out_dir, geeprojectID)
```

## Cite this Work
If you use ```msfootprint``` in your work, please cite it as follows:

```
Dhital, S. (2025). msfootprint: A Python package for extracting Microsoft's global building footprints based on user-defined boundaries (v0.1.24). Zenodo. https://doi.org/10.5281/zenodo.14597326
```
in BibTex,
```
@software{dhital2025msfootprint,
  author       = {S. Dhital},
  title        = {msfootprint: A Python package for extracting Microsoft's global building footprints based on user-defined boundaries},
  version      = {v0.1.24},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.14597326},
  url          = {https://doi.org/10.5281/zenodo.14597326}
}
```
## For Any Information

Feel free to reach out to me:
**Supath Dhital**  
Email: [sdhital@crimson.ua.edu](mailto:sdhital@crimson.ua.edu)
