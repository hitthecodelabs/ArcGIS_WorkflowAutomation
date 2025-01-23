# ArcGIS Scripts for Automated Geospatial Tasks and Map Layouts

This script provides a series of functions to automate common tasks in ArcGIS Pro using ArcPy, including loading layers, calculating areas and centroids, and creating print layouts. It is designed to streamline workflows involving geospatial data and simplify tasks like map creation and data analysis within the ArcGIS Pro environment.

## Features

- **Layer Management**:
  - Load raster layers (e.g., Esri World Imagery basemap, or imagery from URLs).
  - Load vector layers from KML/KMZ, GeoJSON, shapefiles (.shp), and geodatabase feature classes.
  - Remove existing layers from the map to avoid duplication.

- **Data Processing**:
  - Calculate the area (in hectares or other units) of polygon features.
  - Determine centroids of polygon features.

- **Visualization & Layout**:
  - Add styled polygon and marker layers to the ArcGIS Pro map.
  - Create and customize a simple print layout with map frames, legends, titles, and export to PDF or PNG.

## Requirements

- **Software**:
  - ArcGIS Pro (version 2.x or 3.x recommended)
  - Python 3.x (comes standard with ArcGIS Pro)

- **Python Libraries**:
  - `arcpy` (ArcGIS Python API - included with ArcGIS Pro)

## Usage

### 1. Import the Script
Ensure you are running this script within the ArcGIS Pro Python environment. You can use the Python window in ArcGIS Pro, a standalone Python IDE configured for ArcPy, or run it as a script tool within a geoprocessing toolbox. Import this script into your project or environment.

### 2. Functions Overview

#### Layer Management
- `remove_existing_layer(aprx, map_name, layer_name)`
  Removes a layer from a specific map within the ArcGIS Pro project (`.aprx`) by layer name.

- `load_kmz_layer(aprx, map_name, file_path)`
  Loads vector layers from KMZ or KML files into a specified map in the ArcGIS Pro project.

- `load_raster_layer(aprx, map_name, layer_name, raster_path=None, service_url=None)`
  Adds raster layers to a map in the ArcGIS Pro project. Can load from a file path or a web service URL (e.g., Esri World Imagery, custom tile services).

#### Data Processing
- `calculate_area_and_centroid(polygon_layer)`
  Calculates the area and centroid of features in a polygon layer. Returns the total area and adds centroid coordinates as attributes to the feature class.

#### Visualization & Layout
- `create_marker_layer(aprx, map_name, centroid_point, layer_name="CentroidsLayer")`
  Creates a point feature class in memory and adds a marker feature at a given point. Adds this layer to the specified map.

- `create_simple_layout(aprx, layout_name, map_name, polygon_layer, raster_layer, output_path, output_format="PDF")`
  Generates a basic print layout in the ArcGIS Pro project. Includes a map frame showing the polygon and raster layers, a title, and exports the layout to a PDF or PNG file.

### 3. Run the Main Workflow
The `main_demo` function demonstrates the script's capabilities. **You'll need to adapt the file paths and project path to your specific data and ArcGIS Pro project.**

```python
# Example usage (adapt paths and project)
project_path = r"C:\\Path\\To\\Your\\ArcGISProProject.aprx" # Replace with your project path
kml_file = r"C:\\Path\\To\\Your\\PolygonData.kml" # Replace with your KML/KMZ path
output_folder = r"C:\\Path\\To\\Output\\Folder" # Replace with desired output folder

main_demo(project_path, kml_file, output_folder)
