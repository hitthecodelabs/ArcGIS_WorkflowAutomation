import arcpy
import os

def create_polygon_from_utm(coordinates, output_folder, shapefile_name="polygon.shp", utm_zone=17, hemisphere="S"):
    """
    Creates a polygon shapefile from given UTM coordinates.
    
    Parameters:
    - coordinates: List of (X, Y) tuples representing UTM coordinates.
    - output_folder: Path to the folder where the shapefile will be saved.
    - shapefile_name: Name of the output shapefile (default: "polygon.shp").
    - utm_zone: UTM Zone number (default: 17).
    - hemisphere: "N" for North or "S" for South (default: "S" for Southern Hemisphere).
    
    Returns:
    - Path to the created shapefile.
    """
    
    # Select correct EPSG code based on hemisphere
    epsg_code = 32600 + utm_zone if hemisphere.upper() == "N" else 32700 + utm_zone
    spatial_ref = arcpy.SpatialReference(epsg_code)

    # Ensure the polygon is closed
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])  # Closing the polygon

    # Create Polygon Geometry
    polygon = arcpy.Polygon(arcpy.Array([arcpy.Point(x, y) for x, y in coordinates]), spatial_ref)

    # Define output path
    shapefile_path = os.path.join(output_folder, shapefile_name)

    # Check if output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the shapefile
    arcpy.CreateFeatureclass_management(output_folder, shapefile_name, "POLYGON", spatial_reference=spatial_ref)

    # Insert the polygon into the shapefile
    with arcpy.da.InsertCursor(shapefile_path, ["SHAPE@"]) as cursor:
        cursor.insertRow([polygon])

    print(f"Polygon created successfully at: {shapefile_path}")
    return shapefile_path

# usage
utm_coordinates = [
    (..., ...), 
]

# Call the function with desired output location
output_shapefile = create_polygon_from_utm(utm_coordinates, 
                                           output_folder="C:/GIS", ### replace it to the desired directory
                                           shapefile_name="polygon.shp"
                                          )
