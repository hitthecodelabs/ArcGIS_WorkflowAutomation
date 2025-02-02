# -*- coding: utf-8 -*-
"""
Script de Python para dividir una capa de polígonos (centros comerciales)
en capas individuales basadas en el atributo "Name" usando la herramienta
"Split By Attributes" de ArcGIS Pro.
"""

import arcpy

try:
    # 1. Definir las variables de entrada y salida
    input_layer_name = "malls"  # **¡Asegúrate de que este sea el nombre EXACTO de tu capa en el panel 'Contents'!**
    output_geodatabase = "C:/ruta/a/tu/Default.gdb"  # **¡Reemplaza con la ruta real a tu Geodatabase!**
    split_field = "Name"  # Campo por el cual dividir (asumimos que es 'Name')

    # 2. Ejecutar la herramienta "Split By Attributes"
    arcpy.analysis.SplitByAttributes(
        in_table=input_layer_name,
        target_workspace=output_geodatabase,
        split_field=split_field
        # out_location_table=""  # No necesitamos tabla de ubicación en este caso
    )
    print(f"Herramienta 'Split By Attributes' ejecutada correctamente.")
    print(f"Capas individuales creadas en: {output_geodatabase}")
    print(f"Divididas por el campo: '{split_field}' de la capa '{input_layer_name}'")

    print("Script de Python completado.")

except arcpy.ExecuteError:
    print("Error al ejecutar el script de Python:")
    mensajes = arcpy.GetMessages(2) # Obtener mensajes de error detallados
    print(mensajes)
except Exception as e:
    print(f"Error inesperado: {e}")
