# Importing the building footprint module
import msfootprint as msf
from pathlib import Path

# Import the boundary: It supports .GPKG, .KML. .SHP, .GEOJSON
boundary_file = Path(
    "../sample_boundary/test.gpkg"
)

# Country that your boundary Falls in title case (eg, Nepal, China, Costa_Rica, Kingdom_of_Saudi_Arabia etc)
country = "US"
out_dir = Path("./BF_output")

# First check if your boundary contained country us actually feature collection or a folder
# If it is a folder, then you need to mention the subboundaries (In the case of US, states)
msf.FindTableorFolder(
    "Indonesia"
)  # It will print whether it is table ot folder (if folder, it will give all the tables in that folder)

# Using 3 letter country ISO code, like 'USA', 'NPL', 'CHN', 'SAU' etc
countryISO = "USA"

msf.BuildingFootprintwithISO(countryISO, boundary_file, out_dir)

#Sometimes it needs earth-engine projectID to access the data even after the credential is authenticated
#that time
geeprojectID = "your_gee_projectID"
msf.BuildingFootprintwithISO(countryISO, boundary_file, out_dir, geeprojectID)
