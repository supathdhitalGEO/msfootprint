## Microsoft Building Footprint Extracter based on user defined boundary

This tool allows users to retrieve microsoft global building footprint data based on a specified boundary (such as a shapefile or GeoJSON). The footprints are then saved as GeoJSON files to a specified output directory.

### Features

- Supports multiple boundary input file formats: `.shp`, `.gpkg`, `.kml`, `.geojson`.
- Allows users to specify a boundary and retrieve building footprint data for a specific country or region or small study area.
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

#Import the name of country where the boundary is located
country = 'Nepal'

#In some cases, like 'Indonesia', it has seperate feature collection so to get the information about whether you can directly pass country boundary or need to be more specific with which table  contains your ROI, try this:
msf.FindTableorFolder('Indonesia')

#It is not direct table, it contains several statewise table so it will reflect sub collections name/boundaries.

#So if your boundary falls within specific table inside the country (incase it  contains multiple tables) defined as
country = "Indonesia/{table_name}"
```

**For US, it is automated, so no need to give statename but for other countries having multiple tables need to follow aforementioned step**

**Now, run the main script**
```bash
msf.getBuildingFootprint(country, boundary_shp, out_dir)
```
It will save the building footprint as geojson format in designated location.

**For more information about how building footprints are hosted online and to learn about the tables and folder structure, [visit here](https://gee-community-catalog.org/projects/msbuildings/).**

## For Any Information

Feel free to reach out to me:
**Supath Dhital**  
Email: [sdhital@crimson.ua.edu](mailto:sdhital@crimson.ua.edu)
