import arcpy

# Crear un mensaje "Hello World" usando la herramienta AddMessage
arcpy.AddMessage("Hello, World!")
# print("Hello, World!")

# Especifica la ruta al proyecto de ArcGIS Pro (.aprx)
proyecto_aprx = arcpy.mp.ArcGISProject(r"C:\Ruta\A\Tu\Proyecto.aprx")

# Obtiene el layout por su nombre (si ya existe)
layout = proyecto_aprx.listLayouts("MiLayout")[0]

if layout:
    # Obtiene el marco de mapa (map frame) por su nombre
    marco_mapa = layout.listElements("MAPFRAME_ELEMENT", "MarcoMapaPrincipal")[0]

    if marco_mapa:
        # Obtiene el mapa dentro del marco de mapa
        mapa = marco_mapa.map

        # Modifica la extensión del mapa (por ejemplo, a una capa específica)
        capa_extension = mapa.listLayers("CapasDeInteres")[0]
        if capa_extension:
            marco_mapa.camera.setExtent(arcpy.Extent(capa_extension.getExtent()))

        # Actualiza el texto dinámico (ejemplo, asumiendo que tienes un elemento de texto con nombre "TituloDinamico")
        titulo_elemento = layout.listElements("TEXT_ELEMENT", "TituloDinamico")[0]
        if titulo_elemento:
            titulo_elemento.text = "Mapa de la Zona Actualizada"

        # Exporta el layout a PDF
        ruta_pdf_export = r"output.pdf"
        layout.exportToPDF(ruta_pdf_export, resolution=300)
        print(f"Layout exportado a PDF: {ruta_pdf_export}")

    else:
        print("No se encontró el marco de mapa 'MarcoMapaPrincipal'")
else:
    print("No se encontró el layout 'MiLayout'")

del proyecto_aprx # Libera el proyecto
