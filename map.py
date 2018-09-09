import folium

MAP_DEFAULT_LOCATION = [40.122909,-96.207281] # somewhere in Nebraska

m = folium.Map(
    location=MAP_DEFAULT_LOCATION,
    zoom_start=4,
    control_scale=True, # show a scale bar e.g. "100 km" or "50 mi"
    #   tiles='Stamen Terrain', # use a terrain-view for the underlying tileset
)
