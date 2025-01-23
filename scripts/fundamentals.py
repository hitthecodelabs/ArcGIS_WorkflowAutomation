import arcpy

def remove_existing_layer(aprx, map_name, layer_name):
    """
    Remove an existing layer from an ArcGIS Pro map within a project by its name.

    Parameters
    ----------
    aprx : arcpy.mp.ArcGISProject
        The ArcGIS Pro project instance.
    map_name : str
        The name of the map within the project.
    layer_name : str
        The name of the layer to remove if it exists in the specified map.

    Returns
    -------
    bool
        True if a layer was found and removed; False otherwise.

    Notes
    -----
    - If multiple layers share the same name, only the first encountered will be removed.
    - This function is useful for ensuring a fresh state before adding a new layer.
    """
    try:
        m = aprx.listMaps(map_name)[0]  # Get the map object by name
        for lyr in m.listLayers():
            if lyr.name == layer_name:
                m.removeLayer(lyr)
                print(f"Removed existing layer: {layer_name} from map: {map_name}")
                return True
        return False
    except IndexError:
        print(f"Error: Map '{map_name}' not found in the project.")
        return False

def replace_layer_with_raster(aprx, map_name, layer_name, service_url):
    """
    Replace (or add) a raster layer in an ArcGIS Pro map using a service URL.

    Parameters
    ----------
    aprx : arcpy.mp.ArcGISProject
        The ArcGIS Pro project instance.
    map_name : str
        The name of the map within the project.
    layer_name : str
        Name to assign to the new raster layer (and to remove any old layer with this name).
    service_url : str
        The URL for the raster service (e.g., ArcGIS Online imagery service).

    Returns
    -------
    arcpy.mapping.Layer or None
        The newly added raster layer if valid; otherwise None.

    Notes
    -----
    - This function adds a raster layer from a service URL.
    - If a layer with the same name already exists, it will be removed before adding the new one.
    """
    # Remove old layer if present
    remove_existing_layer(aprx, map_name, layer_name)

    try:
        m = aprx.listMaps(map_name)[0]  # Get the map object
        raster_layer = arcpy.mp.Layer(layer_name)  # Create a layer object (in-memory for now)
        raster_layer.dataSource = service_url
        raster_layer.name = layer_name

        m.addLayer(raster_layer) # Add the layer to the map
        print(f"Successfully loaded raster layer: {layer_name} from URL: {service_url} to map: {map_name}")
        return raster_layer
    except Exception as e:
        print(f"Error: Could not load raster layer: {layer_name} from URL: {service_url}. Error details: {e}")
        return None

def transform_layer_crs(layer, target_epsg):
    """
    Sets the spatial reference of a layer to a target CRS.

    Parameters
    ----------
    layer : arcpy.mp.Layer
        The ArcGIS Pro layer whose spatial reference will be set.
    target_epsg : int or str
        The EPSG code (e.g., 4326 or "EPSG:3857") of the target CRS.

    Returns
    -------
    None

    Notes
    -----
    - This function directly sets the spatial reference property of the layer object.
    - It's important to ensure that the data is actually in or can be correctly interpreted in the target CRS.
    """
    try:
        target_sr = arcpy.SpatialReference(target_epsg)
        if layer.isFeatureLayer or layer.isRasterLayer: # Check if it's a layer type that supports spatial reference
            layer.spatialReference = target_sr
            print(f"Set spatial reference of layer '{layer.name}' to EPSG:{target_epsg}.")
        else:
            print(f"Warning: Layer '{layer.name}' does not support setting spatial reference directly.")
    except Exception as e:
        print(f"Error setting spatial reference for layer '{layer.name}' to EPSG:{target_epsg}. Error details: {e}")


def set_layer_opacity(layer, opacity=0.5):
    """
    Set the opacity (transparency) for a layer in ArcGIS Pro.

    Parameters
    ----------
    layer : arcpy.mp.Layer
        The ArcGIS Pro layer (feature layer or raster layer) for which to set opacity.
    opacity : float, optional
        Opacity value, ranging from 0.0 (fully transparent) to 1.0 (fully opaque).
        Default is 0.5 (50% opacity).

    Returns
    -------
    None

    Notes
    -----
    - ArcGIS Pro interprets opacity as a percentage, where 0 is fully opaque and 100 is fully transparent.
    - The input 'opacity' (0.0-1.0) is converted to percentage (0-100) for ArcGIS Pro.
    """
    if not layer.valid:
        print(f"Cannot set opacity; layer '{layer.name}' is invalid.")
        return
    layer.transparency = int((1 - opacity) * 100)  # Convert 0-1 to 100-0 percentage
    print(f"Set opacity of layer '{layer.name}' to {opacity} (ArcGIS Transparency: {layer.transparency}%).")

def create_basic_marker_layer(
    aprx,
    map_name,
    layer_name,
    point_geometry_xy,
    layer_crs=4326, # EPSG:4326 as default
    marker_color="Red", # Basic color name
    marker_size=8 # Points
):
    """
    Create and add an in-memory point feature class layer with a single marker feature in ArcGIS Pro.

    Parameters
    ----------
    aprx : arcpy.mp.ArcGISProject
        The ArcGIS Pro project instance to which the layer will be added.
    map_name : str
        The name of the map within the project.
    layer_name : str
        A name for the in-memory feature class layer.
    point_geometry_xy : tuple(float, float)
        A tuple representing the X and Y coordinates (longitude, latitude) of the marker.
    layer_crs : int or str, optional
        The EPSG code for the in-memory feature class layer (default 4326 - EPSG:4326).
    marker_color : str, optional
        Color of the marker (using ArcGIS color names, e.g., "Red", "Blue", "Green"). Default is "Red".
    marker_size : float, optional
        Marker size in points (default 8).

    Returns
    -------
    arcpy.mp.Layer or None
        The created memory layer if successful; None otherwise.

    Notes
    -----
    - Removes any existing layer with the same name before creating this one.
    - Uses an in-memory feature class to avoid creating files.
    - Basic marker symbol is applied using layer properties. For advanced symbology, CIM should be used.
    """
    remove_existing_layer(aprx, map_name, layer_name)

    try:
        m = aprx.listMaps(map_name)[0]
        sr = arcpy.SpatialReference(layer_crs)
        point = arcpy.Point(point_geometry_xy[0], point_geometry_xy[1])
        point_geometry = arcpy.PointGeometry(point, sr)

        # Create an in-memory feature class
        temp_fc = "in_memory/" + layer_name
        arcpy.CreateFeatureclass_management("in_memory", layer_name, "POINT", spatial_reference=sr)

        # Insert the point feature
        with arcpy.da.InsertCursor(temp_fc, ["SHAPE@"]) as cursor:
            cursor.insertRow([point_geometry])

        # Create a layer object from the in-memory feature class
        memory_layer = arcpy.mp.Layer(temp_fc)
        memory_layer.name = layer_name

        # Basic symbology - simple marker symbol
        memory_layer.symbology.renderer.symbol.color = marker_color
        memory_layer.symbology.renderer.symbol.size = marker_size

        m.addLayer(memory_layer)
        print(f"Marker layer '{layer_name}' created at ({point_geometry_xy[0]}, {point_geometry_xy[1]}) in map '{map_name}'.")
        return memory_layer

    except Exception as e:
        print(f"Error creating marker layer '{layer_name}'. Error details: {e}")
        return None


def add_frame_to_layout(layout, margin_mm=1.0, outline_width_mm=0.65):
    """
    Add a rectangular frame around an entire ArcGIS Pro layout.

    Parameters
    ----------
    layout : arcpy.mp.Layout
        The ArcGIS Pro layout where the frame will be added.
    margin_mm : float, optional
        The margin (in millimeters) from each page border. Default is 1.0 mm.
    outline_width_mm : float, optional
        The width (in millimeters) of the frame’s outline. Default is 0.65 mm.

    Returns
    -------
    arcpy.mp.GraphicElement
        The newly created frame graphic element for further customization if desired.

    Notes
    -----
    - The frame is drawn as a rectangle matching the page size minus the margins.
    - Its default fill is no color, and only the outline is visible.
    """
    try:
        page_width_points = layout.pageWidth * 72 / 25.4  # mm to points (1mm = 72/25.4 points)
        page_height_points = layout.pageHeight * 72 / 25.4
        margin_points = margin_mm * 72 / 25.4
        outline_width_points = outline_width_mm * 72 / 25.4

        frame_width_points = page_width_points - (2 * margin_points)
        frame_height_points = page_height_points - (2 * margin_points)

        frame_element = layout.graphics.appendRectangle(
            polygon=arcpy.Polygon(arcpy.Array([
                arcpy.Point(margin_points, margin_points),
                arcpy.Point(page_width_points - margin_points, margin_points),
                arcpy.Point(page_width_points - margin_points, page_height_points - margin_points),
                arcpy.Point(margin_points, page_height_points - margin_points)
            ])),
            symbol_outline_width=outline_width_points,
            symbol_outline_color="Black",
            symbol_fill_color="No Color" # Transparent fill
        )
        print(f"Added a rectangular frame to layout '{layout.name}'.")
        return frame_element

    except Exception as e:
        print(f"Error adding frame to layout '{layout.name}'. Error details: {e}")
        return None

def add_scale_bar(layout, map_frame_name, position_x, position_y, bar_width, bar_height, units="KILOMETERS", units_per_division=1, division_units="KILOMETERS", num_divisions=2, font_name="Arial", font_size=8, style="Line Ticks Above"):
    """
    Adds a scale bar to an ArcGIS Pro print layout.

    Parameters:
        layout (arcpy.mp.Layout): The layout where the scale bar will be added.
        map_frame_name (str): The name of the map frame to which the scale bar will be linked.
        position_x (float): X position of the scale bar's lower-left corner in layout units (e.g., inches, points).
        position_y (float): Y position of the scale bar's lower-left corner in layout units.
        bar_width (float): Width of the scale bar in layout units.
        bar_height (float): Height of the scale bar in layout units.
        units (str, optional): The distance units to be displayed (e.g., "METERS", "KILOMETERS"). Default is "KILOMETERS".
        units_per_division (float, optional): The length of each division of the scale bar in the specified units. Default is 1.
        division_units (str, optional): The units for the division length (must match 'units'). Default is "KILOMETERS".
        num_divisions (int, optional): Number of divisions on the right side of the scale bar. Default is 2.
        font_name (str, optional): Font family for the scale bar labels. Default is "Arial".
        font_size (int, optional): Font size for the scale bar labels. Default is 8.
        style (str, optional): Style of the scale bar (e.g., "Line Ticks Above", "Stepped Line"). Default is "Line Ticks Above".

    Returns:
        arcpy.mp.ScaleBar: The created scale bar item.

    Raises:
        ValueError: If the linked map frame is not found.
    """
    try:
        map_frame = layout.listElements("MAPFRAME_ELEMENT", map_frame_name)[0]
        if not map_frame:
            raise ValueError(f"Map frame '{map_frame_name}' not found in the layout.")

        scale_bar = layout.scaleBars.create(map_frame)
        scale_bar.elementPositionX = position_x
        scale_bar.elementPositionY = position_y
        scale_bar.elementWidth = bar_width
        scale_bar.elementHeight = bar_height
        scale_bar.units = units
        scale_bar.unitsPerDivision = units_per_division
        scale_bar.divisionUnits = division_units
        scale_bar.numberOfDivisions = num_divisions
        scale_bar.labelFontName = font_name
        scale_bar.labelFontSize = font_size
        scale_bar.style = style

        print(f"Scale bar added to layout '{layout.name}' linked to map frame '{map_frame_name}'.")
        return scale_bar

    except Exception as e:
        print(f"Error adding scale bar to layout '{layout.name}'. Error details: {e}")
        return None


def add_symbology_legend(layout, map_frame_name, title="Symbology", position_x=220, position_y=50, width=40, height=60):
    """
    Adds a legend (symbology) item to the layout, referencing a map frame in ArcGIS Pro.

    Parameters:
        layout (arcpy.mp.Layout): The layout where the legend should be placed.
        map_frame_name (str): The name of the map frame that the legend will reference.
        title (str, optional): Legend title (top text). Default is "Symbology".
        position_x (float, optional): X position (mm) for the legend’s top-left corner. Default is 220 mm.
        position_y (float, optional): Y position (mm) for the legend’s top-left corner. Default is 50 mm.
        width (float, optional): Width (mm) of the legend box. Default is 40 mm.
        height (float, optional): Height (mm) of the legend box. Default is 60 mm.
    """
    try:
        map_frame = layout.listElements("MAPFRAME_ELEMENT", map_frame_name)[0]
        if not map_frame:
            raise ValueError(f"Map frame '{map_frame_name}' not found in the layout.")

        legend = layout.listElements("LEGEND_ELEMENT")[0] # Assuming only one legend, or get by name if needed.
        if not legend:
            legend = layout.legends.createLegend(map_frame) # Create if not existing

        legend.mapFrameName = map_frame_name # Ensure it's linked to the correct map frame
        legend.title = title
        legend.elementPositionX = position_x * 72 / 25.4 # mm to points
        legend.elementPositionY = position_y * 72 / 25.4
        legend.elementWidth = width * 72 / 25.4
        legend.elementHeight = height * 72 / 25.4
        legend.frame = True  # Enable frame around the legend

        print(f"Symbology legend added to layout '{layout.name}' linked to map frame '{map_frame_name}'.")

    except Exception as e:
        print(f"Error adding symbology legend to layout '{layout.name}'. Error details: {e}")


# Example Usage (ArcGIS Pro)
if __name__ == '__main__':
    # Replace with the actual path to your ArcGIS Pro project file (.aprx)
    project_path = r"C:\Path\To\Your\ArcGISProProject.aprx" # Change this to your project path
    aprx = arcpy.mp.ArcGISProject(project_path)
    map_name = "Map" # Assuming your map is named "Map"
    layout_name = "Layout" # Assuming your layout is named "Layout"

    # 1) Replace an existing layer with a new raster
    replace_layer_with_raster(
        aprx,
        map_name=map_name,
        layer_name="World Imagery", # Desired layer name in ArcGIS Pro
        service_url="https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer" # Esri World Imagery service URL
    )

    # 2) Set spatial reference of a layer to EPSG:3857 (Web Mercator)
    districts_layer_name = "Districts" # Replace with the actual name of your districts layer in ArcGIS Pro
    districts_layer = aprx.listMaps(map_name)[0].listLayers(districts_layer_name)[0]
    if districts_layer:
        transform_layer_crs(districts_layer, 3857) # EPSG code for Web Mercator
    else:
        print(f"Warning: Layer '{districts_layer_name}' not found in map '{map_name}'.")

    # 3) Set partial opacity on a layer
    if districts_layer:
        set_layer_opacity(districts_layer, 0.6) # 60% opacity

    # 4) Create a marker at a given coordinate (Longitude, Latitude)
    create_basic_marker_layer(
        aprx,
        map_name=map_name,
        layer_name="Capital Marker",
        point_geometry_xy=(-77.0369, 38.9072), # Washington D.C. coordinates
        layer_crs=4326, # EPSG:4326 (Latitude/Longitude)
        marker_color="Blue",
        marker_size=10
    )

    # 5) Add a frame to a layout
    try:
        lyt = aprx.listLayouts(layout_name)[0]
        add_frame_to_layout(lyt)

        # 6) Add a scale bar to the layout, linked to the map frame named "Map Frame" (adjust name if needed)
        add_scale_bar(
            lyt,
            map_frame_name="Map Frame", # Default map frame name, adjust if different
            position_x=10, position_y=10, # Position in points
            bar_width=70, bar_height=5, # Size in points
            units="KILOMETERS", units_per_division=5, division_units="KILOMETERS"
        )

        # 7) Add a symbology legend, linked to "Map Frame"
        add_symbology_legend(
            lyt,
            map_frame_name="Map Frame",
            title="Legend Title",
            position_x=20, position_y=80, # Position in mm
            width=50, height=70 # Size in mm
        )


        aprx.save() # Save the changes to the project
        print(f"Project '{project_path}' saved with updates.")

    except IndexError:
        print(f"Error: Layout '{layout_name}' not found in the project.")
    except Exception as e:
        print(f"An error occurred: {e}")

    del aprx # Clean up project object
