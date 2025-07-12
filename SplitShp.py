import geopandas as gpd
from shapely.geometry import box
import os

# Load the district shapefile
input_shapefile = r"C:\Users\Rohit Btech\Downloads\SAR-OPT_fusion_GEE-main\SAR-OPT_fusion_GEE-main\AOI\Nashik_Boundary_Shapefile.shp"  # Change this to your shapefile path
output_folder = r"C:\Users\Rohit Btech\Desktop\Shapefiles4x4km"  # Folder to store individual grids

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the district shapefile
district = gpd.read_file(input_shapefile)

# Get the bounding box of the district
minx, miny, maxx, maxy = district.total_bounds

# Define grid size (4x4 km in degrees, approximate conversion needed)
grid_size = 4 / 111  # Convert km to degrees (1 degree ≈ 111 km)

# Generate grid cells
grid_cells = []
x = minx
while x < maxx:
    y = miny
    while y < maxy:
        grid = box(x, y, x + grid_size, y + grid_size)
        if district.intersects(grid).any():  # Keep only grids intersecting the district
            grid_cells.append(grid)
        y += grid_size
    x += grid_size

# Convert grid to GeoDataFrame
grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs=district.crs)

# Save each grid as a separate shapefile
for i, grid in enumerate(grid_gdf.geometry):
    grid_df = gpd.GeoDataFrame(geometry=[grid], crs=district.crs)
    grid_df.to_file(f"{output_folder}/grid_{i}.shp")

print(f"Grids saved in '{output_folder}'")