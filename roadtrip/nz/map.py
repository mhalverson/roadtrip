import folium

MAP_DEFAULT_LOCATION = [-38.5463, 175.7749]

m = folium.Map(
    location=MAP_DEFAULT_LOCATION,
    zoom_start=6,
    control_scale=True, # show a scale bar e.g. "100 km" or "50 mi"
    #   tiles='Stamen Terrain', # use a terrain-view for the underlying tileset
)

# Sometimes it is useful to enable lat/lng popups on the map. Do so by
# uncommenting the following line:
# m.add_child(folium.LatLngPopup())
