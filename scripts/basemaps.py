import arcpy

# Dictionary of map sources and their URLs
map_sources = {
    "Bing Aerial": "http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1",
    "Bing VirtualEarth": "http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1",
    "CartoDb Dark Matter (No Labels)": "http://basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png",
    "CartoDb Dark Matter": "http://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
    "CartoDb Positron (No Labels)": "http://basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
    "CartoDb Positron": "http://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
    "Esri Boundaries Places": "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
    "Esri Gray (dark)": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    "Esri Gray (light)": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    "Esri Hillshade": "http://services.arcgisonline.com/ArcGIS/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}",
    "Esri National Geographic": "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
    "Esri Navigation Charts": "http://services.arcgisonline.com/ArcGIS/rest/services/Specialty/World_Navigation_Charts/MapServer/tile/{z}/{y}/{x}",
    "Esri Ocean": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
    "Esri Physical Map": "https://services.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
    "Esri Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "Esri Shaded Relief": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
    "Esri Standard": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    "Esri Terrain": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
    "Esri Topo World": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
    "Esri Transportation": "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
    "Google Maps": "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    "Google Roads": "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    "Google Satellite Hybrid": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
    "Google Satellite": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    "Google Terrain Hybrid": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
    "Google Terrain": "https://mt1.google.com/vt/lyrs=t&x={x}&y={y}&z={z}",
    "Mapzen Global Terrain": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
    "OpenStreetMap H.O.T.": "http://tile.openstreetmap.fr/hot/%7Bz%7D/%7Bx%7D/%7By%7D.png",
    "OpenStreetMap Standard": "http://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png",
    "OpenStreetMap": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    "OpenTopoMap": "https://tile.opentopomap.org/{z}/{x}/{y}.png",
    "Strava All": "https://heatmap-external-b.strava.com/tiles/all/bluered/{z}/{x}/{y}.png",
    "Strava Run": "https://heatmap-external-b.strava.com/tiles/run/bluered/{z}/{x}/{y}.png?v=19"
}

try:
    # Get the current ArcGIS Pro project and active map
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    active_map = aprx.activeMap

    if active_map is None:
        print("No active map found in the ArcGIS Pro project.")
    else:
        for name, url in map_sources.items():
            try:
                # Create a Layer object for the tiled service URL
                basemap_layer = arcpy.mapping.Layer() # Initialize an empty Layer object
                basemap_layer.name = name # Set the name of the layer
                basemap_layer.connectToTiledService(url) # Connect to the tiled service using the URL
                basemap_layer.serviceConnectionType = "Tiled" # Specify the connection type as Tiled

                # Add the basemap layer to the map's basemap layer collection
                active_map.addLayer(basemap_layer, "BOTTOM") # Add to the bottom of the map layers

                print(f"Successfully added basemap: {name}")

            except Exception as e:
                print(f"Error adding basemap '{name}': {e}")

    # Save the ArcGIS Pro project (optional)
    # aprx.save() # Uncomment if you want to save the project after adding basemaps

except Exception as overall_error:
    print(f"An overall error occurred: {overall_error}")
