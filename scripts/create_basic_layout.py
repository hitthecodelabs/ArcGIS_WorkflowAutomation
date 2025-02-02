# -*- coding: utf-8 -*-
"""
Script de Python para crear un layout básico de mapa en ArcGIS Pro,
incluyendo un Map Frame, Scale Bar y North Arrow.
"""

import arcpy

try:
    # 1. Obtener el proyecto actual de ArcGIS Pro
    proyecto = arcpy.mp.ArcGISProject("CURRENT")
    print("Proyecto actual obtenido.")

    # 2. Obtener el mapa que queremos incluir en el layout
    mapa_nombre = "Map"  # **¡Asegúrate de que este sea el nombre EXACTO de tu Map en el panel 'Contents'!**
    mapa = proyecto.listMaps(mapa_nombre)[0] # Asume que hay un solo mapa con este nombre
    if mapa:
        print(f"Mapa '{mapa_nombre}' obtenido.")
    else:
        raise Exception(f"No se encontró el mapa con el nombre '{mapa_nombre}' en el proyecto.")

    # 3. Crear un nuevo layout (diseño de mapa)
    layout_nombre = "Layout_Basico_Python" # Nombre para el nuevo layout
    nuevo_layout = proyecto.createLayout(name=layout_nombre, page_size="LETTER", page_orientation="LANDSCAPE") # Tamaño carta, orientación horizontal
    print(f"Layout '{layout_nombre}' creado.")

    # 4. Crear un Map Frame (marco de mapa) y añadirlo al layout
    map_frame_nombre = "MarcoMapa_CentrosComerciales"
    map_frame_ancho = 15  # Ancho en pulgadas
    map_frame_alto = 20   # Alto en pulgadas
    map_frame_posicion_x = 2  # Posición X en pulgadas desde la izquierda
    map_frame_posicion_y = 2  # Posición Y en pulgadas desde la parte inferior

    map_frame = nuevo_layout.addMapFrame(map_to_embed=mapa,
                                       x=map_frame_posicion_x,
                                       y=map_frame_posicion_y,
                                       width=map_frame_ancho,
                                       height=map_frame_alto,
                                       name=map_frame_nombre)
    print(f"Map Frame '{map_frame_nombre}' añadido al layout.")

    # 5. Añadir una Scale Bar (barra de escala) al layout
    scale_bar_estilo = "Alternating Scale Bar 1" # Estilo de barra de escala (puedes cambiarlo)
    scale_bar_posicion_x = 2.5 # Posición X
    scale_bar_posicion_y = 1.5 # Posición Y

    scale_bar = nuevo_layout.addScaleBar(style=scale_bar_estilo,
                                        x=scale_bar_posicion_x,
                                        y=scale_bar_posicion_y)
    print("Scale Bar añadida al layout.")

    # 6. Añadir un North Arrow (flecha de norte) al layout
    north_arrow_estilo = "ESRI North 1" # Estilo de flecha de norte (puedes cambiarlo)
    north_arrow_posicion_x = 18 # Posición X
    north_arrow_posicion_y = 20 # Posición Y
    north_arrow_tamano = 5 # Tamaño de la flecha de norte

    north_arrow = nuevo_layout.addNorthArrow(style=north_arrow_estilo,
                                            x=north_arrow_posicion_x,
                                            y=north_arrow_posicion_y,
                                            size=north_arrow_tamano)
    print("North Arrow añadido al layout.")

    # 7. Guardar el proyecto
    proyecto.save()
    print(f"Proyecto guardado. Layout '{layout_nombre}' creado con éxito.")

    print("Script de Python completado.")

except arcpy.ExecuteError:
    print("Error al ejecutar el script de Python:")
    mensajes = arcpy.GetMessages(2) # Obtener mensajes de error detallados
    print(mensajes)
except Exception as e:
    print(f"Error inesperado: {e}")
