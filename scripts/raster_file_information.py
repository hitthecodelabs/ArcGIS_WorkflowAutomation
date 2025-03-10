import arcpy

# ----------------------
# Raster Setup
# ----------------------
# Define the raster file path (using raw string with backslashes)
raster_path = "raster.tif"
# Alternative raster (commented out): raster_path = r"Guayas/Salinas_2_.img"

# Create raster description and object
desc = arcpy.Describe(raster_path)
raster_obj = arcpy.Raster(raster_path)

# ----------------------
# Spatial Properties
# ----------------------
# Extent in UTM coordinates
print(f"Extent (UTM): {desc.extent}")

# Spatial reference name
print(f"Spatial Reference: {desc.spatialReference.name}")

# Cell size (resolution in meters)
print(f"Cell Size: {raster_obj.meanCellWidth}, {raster_obj.meanCellHeight}")

# Convert extent to Lat/Long
extent = desc.extent
sr_utm = arcpy.SpatialReference("WGS 1984 UTM Zone 17S")
sr_wgs84 = arcpy.SpatialReference(4326)  # EPSG code for WGS84 geographic
extent_utm = arcpy.Extent(extent.XMin, extent.YMin, extent.XMax, extent.YMax, spatial_reference=sr_utm)
extent_wgs84 = extent_utm.projectAs(sr_wgs84)
print(f"Extent (Lat/Long): {extent_wgs84.XMin}, {extent_wgs84.YMin}, {extent_wgs84.XMax}, {extent_wgs84.YMax}")

# Full spatial reference details
sr = desc.spatialReference
print(f"Full Spatial Reference: {sr.exportToString()}")

# ----------------------
# Raster Attributes
# ----------------------
# File format
print(f"Format: {desc.format}")

# NoData value
print(f"NoData Value: {raster_obj.noDataValue}")

# Raster dimensions
print(f"Width (Columns): {raster_obj.width}")
print(f"Height (Rows): {raster_obj.height}")

# Number of bands
print(f"Number of Bands: {raster_obj.bandCount}")

# Compression type
print(f"Compression Type: {desc.compressionType}")
