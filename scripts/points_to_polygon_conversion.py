import arcpy
import os

'''
arcpy.conversion.FeatureClassToShapefile(
    Input_Features="SNAP_AreasProtegidas_Ecuador",
    Output_Folder=r"output_folder"
)
'''

'''
arcpy.management.PointsToLine(
    Input_Features="Hoja1$Event",
    Output_Feature_Class=r"Default.gdb\Hoja1Event_PointsToLine1",
    Line_Field=None,
    Sort_Field=None,
    Close_Line="CLOSE",
    Line_Construction_Method="CONTINUOUS",
    Attribute_Source="NONE",
    Transfer_Fields=None
)
'''

def process_points_to_polygon(input_point_feature, output_gdb, output_folder):
    """
    Converts point features to lines and then to polygons, finally exporting the polygon to a shapefile.

    This function takes a point feature layer, converts it to a line feature class,
    then converts the line feature class to a polygon feature class within a specified
    geodatabase. Finally, it exports the resulting polygon feature class to a shapefile
    in a designated output folder.

    Parameters:
        input_point_feature (str): The name of the input point feature layer or table view.
                                     This can be a feature layer name in the current map document,
                                     a path to a feature class, or a table view.
                                     Example: "Hoja1$Event" or r"C:\path\to\your.gdb\PointFeatureClass"
        output_gdb (str): The path to the geodatabase where intermediate and final feature classes
                             will be stored.
                             Example: r"C:\Users\user\Desktop\study\argcis_projs\estudioDeCobertura_gispro\Default.gdb"
        output_folder (str): The path to the folder where the final shapefile will be exported.
                              Example: r"C:\Users\user\Desktop\study\Febrero\10 al 14\OutputShapefiles"

    Returns:
        bool: True if the process completes successfully, False otherwise.
              Prints informative messages to the console about the process and any errors encountered.

    Raises:
        arcpy.ExecuteError: If any ArcGIS tool execution fails. Error messages are printed to the console.
        Exception: For any other unexpected errors during the process.

    Example:
        >>> process_points_to_polygon(
        ...     input_point_feature="Hoja1$Event",
        ...     output_gdb=r"C:\Users\user\Desktop\study\argcis_projs\estudioDeCobertura_gispro\Default.gdb",
        ...     output_folder=r"C:\Users\user\Desktop\study\Febrero\10 al 14\OutputShapefiles"
        ... )
        True
    """
    try:
        # --- Points to Line ---
        line_feature_class_name = f"{input_point_feature.replace('$','').replace(' ', '_')}_PointsToLine" # Generate output line feature class name
        output_line_feature_class = os.path.join(output_gdb, line_feature_class_name)

        print(f"Starting Points To Line conversion for: {input_point_feature}")
        arcpy.management.PointsToLine(
            Input_Features=input_point_feature,
            Output_Feature_Class=output_line_feature_class,
            Line_Field=None,
            Sort_Field=None,
            Close_Line="CLOSE",
            Line_Construction_Method="CONTINUOUS",
            Attribute_Source="NONE",
            Transfer_Fields=None
        )
        print(f"Points to Line conversion completed. Output: {output_line_feature_class}")

        # --- Feature to Polygon ---
        polygon_feature_class_name = f"{input_point_feature.replace('$','').replace(' ', '_')}_Polygon" # Generate output polygon feature class name
        output_polygon_feature_class = os.path.join(output_gdb, polygon_feature_class_name)

        print(f"Starting Feature To Polygon conversion for: {line_feature_class_name}")
        arcpy.management.FeatureToPolygon(
            in_features=output_line_feature_class,
            out_feature_class=output_polygon_feature_class,
            cluster_tolerance=None,
            attributes="ATTRIBUTES",
            label_features=None
        )
        print(f"Feature to Polygon conversion completed. Output: {output_polygon_feature_class}")

        # --- Feature Class to Shapefile ---
        output_shapefile_name = f"{polygon_feature_class_name}.shp" # Generate output shapefile name
        output_shapefile_path = os.path.join(output_folder, output_shapefile_name)

        print(f"Starting Feature Class To Shapefile export for: {polygon_feature_class_name}")
        arcpy.conversion.FeatureClassToShapefile(
            Input_Features=output_polygon_feature_class,
            Output_Folder=output_folder
        )
        print(f"Feature Class to Shapefile export completed. Output: {output_shapefile_path}")

        return True

    except arcpy.ExecuteError:
        msgs = arcpy.GetMessages(2)
        print(f"ArcGIS tool execution failed for input: {input_point_feature}")
        print(msgs)
        return False
    except Exception as e:
        print(f"An unexpected error occurred for input: {input_point_feature}")
        print(e)
        return False

# Example of how to use the function with your provided inputs:
if __name__ == '__main__':
    output_geodatabase = r"Default.gdb"
    base_output_folder = r"output_folder"

    input_features_list = [
        "Hoja1$Event",
        "Hoja1$HonorioAbsalonGarcia"
    ]

    output_folders_list = [
        os.path.join(base_output_folder, "EVENT"), # Example folder name for Event
        os.path.join(base_output_folder, "folder")
    ]

    for input_feature, output_folder_shp in zip(input_features_list, output_folders_list):
        success = process_points_to_polygon(input_feature, output_geodatabase, output_folder_shp)
        if success:
            print(f"\nSuccessfully processed: {input_feature}")
        else:
            print(f"\nFailed to process: {input_feature}")
