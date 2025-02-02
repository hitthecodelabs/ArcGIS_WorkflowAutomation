# Importar la biblioteca arcpy (necesaria para trabajar con ArcGIS)
import arcpy

try:
    # 1. Definir las variables de entrada y salida
    input_kml_file = "C:/ruta/a/tu/archivo.kml"  # **¡Reemplaza con la ruta real a tu archivo KML!**
    output_geodatabase = "C:/ruta/a/tu/Default.gdb" # **¡Reemplaza con la ruta real a tu Geodatabase!**
    output_feature_class_name = "PoligonoEditable_Script" # Nombre para la nueva Feature Class

    # 2. Ejecutar la herramienta "KML to Layer"
    arcpy.management.KMLToLayer(
        in_kml_file=input_kml_file,
        output_location=output_geodatabase,
        output_name=output_feature_class_name
    )
    print(f"Herramienta KML to Layer ejecutada correctamente. Capa creada: {output_feature_class_name}")

    # 3. Cambiar la simbología de la nueva Feature Class (Ejemplo básico: color de relleno y contorno)

    # Obtener una referencia a la capa recién creada
    capa_editable = arcpy.mp.Layer(output_feature_class_name) # Asume que la capa se añadió al mapa

    if capa_editable:
        # Acceder a las propiedades de simbología de la capa (CIM - Cartographic Information Model)
        simbologia = capa_editable.getSymbology()

        # Asegurarse de que la simbología es de símbolo único (Single Symbol)
        if simbologia.renderer.type == 'SimpleRenderer':
            simbologia.renderer.symbol.color = {'RGB': [255, 255, 0, 100]}  # Color de relleno Amarillo (RGBA)
            simbologia.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]} # Color de contorno Negro
            simbologia.renderer.symbol.outlineWidth = 1.5 # Ancho de contorno 1.5 puntos

            # Aplicar la simbología modificada a la capa
            capa_editable.setSymbology(simbologia)
            print(f"Simbología de la capa '{output_feature_class_name}' modificada.")
        else:
            print(f"La capa '{output_feature_class_name}' no usa simbología de Símbolo Único. Script de simbología simple no aplicable.")
    else:
        print(f"No se pudo encontrar la capa '{output_feature_class_name}' en el mapa para modificar la simbología.")


    print("Script de Python completado.")

except arcpy.ExecuteError:
    print("Error al ejecutar el script de Python:")
    mensajes = arcpy.GetMessages(2) # Obtener mensajes de error detallados
    print(mensajes)
except Exception as e:
    print(f"Error inesperado: {e}")
