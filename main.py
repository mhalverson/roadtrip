from collections import defaultdict
from datetime import date
import json
from pprint import pprint
from xml.sax.saxutils import escape

import folium
from folium import FeatureGroup, GeoJson, LayerControl, Map, Marker, Popup, plugins
from shapely.geometry import shape, GeometryCollection, Point, mapping

from common import *
import coords
from dateutils import (format_date_range, break_into_ranges, collapse_date_ranges)
from map import m
from parks import parks
from trip import trip

# next steps --
#
# . populate TRIP!

# . fold Facebook etc into trip.py with DAY_FACEBOOK?
# . move feature_group calculation into their own file, move summary/superlative data into its own file

# . look up the park boundaries (some are really really fudged...)
# . figure out icons
# . grep for other TODOs

ICON_CAMPING = 'chevron-up'
COLOR_CAMPING = 'green'
ICON_CITY = 'home'
COLOR_CITY = 'blue'
ICON_FRIEND = 'user'
COLOR_FRIEND = 'orange'
ICON_PARK = 'tree' # TODO this isn't a real icon
COLOR_PARK = 'green'
ICON_STATE = 'state' # TODO
COLOR_STATE_VISITED = 'green'
COLOR_STATE_NOT_VISITED = 'red'

summary = defaultdict(int)
SUMMARY_DAYS_TOTAL = 'days_total'
SUMMARY_DAYS_CAMPING = 'days_camping'
SUMMARY_DAYS_CITY = 'days_city'
SUMMARY_MILES = 'miles'
SUMMARY_HOURS = 'hours'


### BEGINNING OF FEATURE GROUPS

# A feature group has the following properties:
#  - map overlay of markers, where marker popups have date + description
#  - summary table, including date + description

# Route
fg_route = FeatureGroup(name='Route', show=True)
fg_route.add_to(m)

for i, day in enumerate(trip):
    leg = []
    if i == 0 or day.get(DAY_NEW_LEG):
        pass # do nothing!
    else:
        wake_up_coord = trip[i-1][DAY_COORD]
        leg.append(wake_up_coord)
    if day.get(DAY_WAYPOINTS):
        leg.extend(day[DAY_WAYPOINTS])
    sleep_coord = day[DAY_COORD]
    leg.append(sleep_coord)
    
    if len(leg) < 2:
        continue
        
    folium.PolyLine(
        locations=leg,
        color='#FF0000',
        weight=5,
        popup='{}'.format(day[DAY_DATE]),
    ).add_to(fg_route)

# 1 Sleep - subgroups for camping vs city
# Subgroup docs: https://github.com/python-visualization/folium/issues/475
fg_sleep = FeatureGroup(name='Where we slept', show=True)
fg_sleep.add_to(m)

fg_sleep_subgroup_camping = plugins.FeatureGroupSubGroup(fg_sleep, '(Where we slept): camping')
m.add_child(fg_sleep_subgroup_camping)
fg_sleep_subgroup_city = plugins.FeatureGroupSubGroup(fg_sleep, '(Where we slept): cities')
m.add_child(fg_sleep_subgroup_city)

summary_sleep = [] # list of (collapsed date range, place)

# escape() and unescape() takes care of &, < and >.
html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}
def html_escape(strings, sep='<br/>'):
    no_empties = filter(lambda s: s, strings)
    formatted = map(lambda s: '{}'.format(s), no_empties)
    escaped = map(lambda s: escape(s, html_escape_table), formatted)
    return sep.join(escaped)

sleep_markers = {} # key is latlng, value is (coord_label, coord_type, icon, subgroup)
sleep_dates = defaultdict(list)  # key is latlng, value is list of dates we were there

for i, day in enumerate(trip):
    sleep_coord = day[DAY_COORD]
    if sleep_coord not in sleep_markers:
        coord_label = day[DAY_COORD_LABEL]
        coord_type = day[DAY_COORD_TYPE]
        icon = {
            DAY_COORD_CAMPING: folium.Icon(icon=ICON_CAMPING, color=COLOR_CAMPING),
            DAY_COORD_CITY: folium.Icon(icon=ICON_CITY, color=COLOR_CITY),
        }[coord_type]
        subgroup = {
            DAY_COORD_CAMPING: fg_sleep_subgroup_camping,
            DAY_COORD_CITY: fg_sleep_subgroup_city,
        }[coord_type]
        
        sleep_markers[sleep_coord] = (coord_label, coord_type, icon, subgroup)
    sleep_dates[sleep_coord].append(day[DAY_DATE])
    summary[SUMMARY_DAYS_TOTAL] += 1
    if DAY_MILES in day:
        summary[SUMMARY_MILES] += day[DAY_MILES]
    if DAY_HOURS in day:
        summary[SUMMARY_HOURS] += day[DAY_HOURS]

for sleep_coord, dates in sleep_dates.iteritems():
    (coord_label, coord_type, icon, subgroup) = sleep_markers[sleep_coord]      
    popup = '{}<br/>{}'.format(coord_label, collapse_date_ranges(dates, sep='<br/>'))
    Marker(
        location=sleep_coord,
        popup=folium.Popup(popup),
        icon=icon,
    ).add_to(subgroup)
    
    for first, last in break_into_ranges(dates):
        date_range = format_date_range(first, last)
        summary_sleep.append((date_range, coord_label))
    
    summary_type = {
        DAY_COORD_CAMPING: SUMMARY_DAYS_CAMPING,
        DAY_COORD_CITY: SUMMARY_DAYS_CITY,
    }[coord_type]
    summary[summary_type] += len(dates)

# 2 Friend
fg_friend = FeatureGroup(name='Who we saw', show=False)
fg_friend.add_to(m)

friend_and_coord_to_dates = defaultdict(list)  # key is tuple of (friend, coord); value is list of dates we saw them
friend_to_dates = defaultdict(list)  # key is friend name; value is list of dates we saw them

for i, day in enumerate(trip):
    if DAY_FRIENDS in day:
        for (friend, coord) in day[DAY_FRIENDS].iteritems():
            date = day[DAY_DATE]
            friend_and_coord_to_dates[(friend, coord)].append(date)
            friend_to_dates[friend].append(date)

summary_friend = []

for friend_data, dates in friend_and_coord_to_dates.iteritems():
    (friend, coord) = friend_data
    
    popup = '{}<br/>{}'.format(friend, collapse_date_ranges(dates, sep='<br/>'))
    Marker(
        location=coord,
        popup=popup,
        icon=folium.Icon(icon=ICON_FRIEND, color=COLOR_FRIEND),
    ).add_to(fg_friend)
    
    for first, last in break_into_ranges(dates):
        date_range = format_date_range(first, last)
        summary_friend.append((date_range, friend))    

# 3 State
fg_state = FeatureGroup(name='States we visited', show=False)
fg_state.add_to(m)

# Load states data from folium itself o_O A bit weird, but if it's there... why not?
states = None
with open("../folium/examples/data/us-states.json") as f:
    states = json.load(f)["features"]

# add abbreviation as a property!
for i in range(len(states)):
    abbrev = states[i]['id']
    states[i]['properties']['abbrev'] = abbrev

state_geometries = {}
for s in states:
    # coerce to shapely geometries from https://medium.com/@pramukta/recipe-importing-geojson-into-shapely-da1edf79f41d
    abbrev = s['id']
    geo = GeometryCollection([shape(s['geometry']).buffer(0)])
    state_geometries[abbrev] = geo
    
def state_for_coord(coord):
    # returns the US state containing the coordinate ('CA', 'NY', ...), or None if not in the USA
    lat, lng = coord
    point = Point(lng, lat)
    for s, geo in state_geometries.iteritems():
        if geo.contains(point):
             return s
    return None

summary_state = defaultdict(list)

for i, day in enumerate(trip):
    if i > 0:  # skip the first day
        woke_up_coord_list = [trip[i-1][DAY_COORD]]
    else:
        woke_up_coord_list = []
    
    waypoint_list = day.get(DAY_WAYPOINTS, [])
    sleep_coord = day[DAY_COORD]

    states_dupes_nones = map(state_for_coord,
                             woke_up_coord_list + waypoint_list + [sleep_coord])
    states_dupes = filter(None, states_dupes_nones)
    states_deduped = set(states_dupes)
    date = day[DAY_DATE]
    for s in states_deduped:
        summary_state[s].append(date)

def visited(state_abbrev):
    return bool(summary_state[state_abbrev])

for s in states:
    abbrev = s['id']
    date_ranges = summary_state[abbrev]
    
    if visited(abbrev):
        popup = '{}<br/>{}'.format(abbrev, collapse_date_ranges(date_ranges, sep='<br/>'))
    else:
        popup = '{}<br/>{}'.format(abbrev, '(Did not visit)')

    gj = folium.GeoJson(
        s,
        style_function=lambda feature: {
            'fillColor': 'green' if visited(feature['properties']['abbrev']) else '#ffff00',
        },
    )
    gj.add_child(Popup(popup))
    gj.add_to(fg_state)

# 4 Park
fg_park = FeatureGroup(name='Parks we visited', show=False)
fg_park.add_to(m)

summary_park = defaultdict(list)

for day in trip:
    if DAY_PARKS in day:
        for p in day[DAY_PARKS]:
            summary_park[p].append(day[DAY_DATE])

def add_park(park, popup, feature_group):
    geom_raw = parks[park]

    gc_raw = GeometryCollection([shape(geom_raw)])
    gc_simple = GeometryCollection.simplify(gc_raw, 0.01) # TODO 0.01 is made up from thin air, what should it really be?

    geojson_simple = GeoJson(mapping(gc_simple))
    geojson_simple.add_to(feature_group)

    centroid = gc_raw.centroid
    Marker(
        location=(centroid.y, centroid.x),
        popup=popup,
    ).add_to(feature_group)

for p, date_ranges in summary_park.iteritems():
    date_range = collapse_date_ranges(date_ranges)
    popup = html_escape([p, date_range])
    add_park(p, popup, fg_park)

# 5 Superlative cities # TODO revisit when done
fg_superlative_cities = FeatureGroup(name='Favourite (+least) city', show=False)
fg_superlative_cities.add_to(m)

superlative_cities_data = [
    ('2018-06-11 to 2018-06-15', 'Favorite for Matt: DC', coords.dc),
    ('2018-07-11 to 2018-07-15', 'Favorite for Claire: Chicago', coords.chicago),
    ('2018-05-29 to 2018-06-01', 'Least favorite for Matt: Augusta', coords.north_augusta),
    ('2018-05-09 to 2018-05-12', 'Least favorite for Claire: Dallas', (32.783057, -96.798872)),
]

for dates, desc, coord in superlative_cities_data:
    Marker(
        location=coord,
        # TODO custom icon
        popup=html_escape([desc, dates]),
    ).add_to(fg_superlative_cities)

summary_superlative_city = map(lambda x: x[:2], superlative_cities_data)

# 6 Superlative nature # TODO revisit when done
fg_superlative_nature = FeatureGroup(name='Favourite (+least) nature', show=False)
fg_superlative_nature.add_to(m)

superlative_nature_data = [
    ('2018-09-02 to 2018-09-07', 'Favorite for Matt and Claire', 'Banff NP'),
    ('2018-05-27 to 2018-05-29', 'Least favorite for Matt and Claire', 'Congaree NP'),
]

for dates, desc, park in superlative_nature_data:
    popup = html_escape(['{}: {}'.format(desc, park), dates])
    add_park(park, popup, fg_superlative_nature)

summary_superlative_nature = map(
    lambda x: (x[0], '{}: {}'.format(x[1], x[2])),
    superlative_nature_data,
)

# 7 Animal sightings
fg_animal = FeatureGroup(name='Animal sightings', show=False)
fg_animal.add_to(m)

park_to_animal = defaultdict(list)  # key is park name; value is list of tuples of (animal, date)

for day in trip:
    if DAY_ANIMAL in day:
        date = day[DAY_DATE]
        for animal, park in day[DAY_ANIMAL]:
            park_to_animal[park].append((animal, date))

summary_animal = []
for park, animal_data in park_to_animal.iteritems():
    
    animal_to_dates = defaultdict(list)
    for animal, date in animal_data:
        animal_to_dates[animal].append(date)
    
    # popup text should be "Elk on 2018-09-03 to 2018-09-04 <br/> Ptarmigan on 2018-09-05 <br/> in Banff NP"
    popup_lines = []
    for animal, dates in animal_to_dates.iteritems():
        date_range = collapse_date_ranges(dates)
        summary_animal.append((date_range, animal, park)) # fill in summary while we're at it
        
        popup_lines.append('{} on {}'.format(animal, date_range))
    popup_lines.append('in {}'.format(park))

    popup = html_escape(popup_lines)
    add_park(park, popup, fg_animal)


# 8 Mountains climbed aka getting high
fg_got_high = FeatureGroup(name='High elevations', show=False)
fg_got_high.add_to(m)

summary_got_high = []

for day in trip:
    if DAY_GOT_HIGH in day:
        date = day[DAY_DATE]
        for (place, height_ft, coord) in day[DAY_GOT_HIGH]:
            height_m = int(height_ft * 0.3048)
            height_str = '{} ft/{} m'.format(height_ft, height_m)
            Marker(
                location=coord,
                # TODO custom icon
                popup=html_escape([place, height_str, date]),
            ).add_to(fg_got_high)
            summary_got_high.append((date, height_str))

# 9 Swimming
fg_swim = FeatureGroup(name='Places we swam', show=False)
fg_swim.add_to(m)

swim_to_dates = defaultdict(list)  # key is (place name, latlng), value is list of dates

for day in trip:
    if DAY_SWIM in day:
        swim_data = day[DAY_SWIM]
        date = day[DAY_DATE]
        swim_to_dates[swim_data].append(date)

summary_swim = {}

for swim_data, dates in swim_to_dates.iteritems():
    (place, coord) = swim_data
    
    popup = '{}<br/>{}'.format(place, collapse_date_ranges(dates, sep='<br/>', inner_sep=' and '))
    Marker(
        location=coord,
        # TODO custom icon
        popup=popup,
    ).add_to(fg_swim)
    
    summary_swim[place] = collapse_date_ranges(dates)

# 10 Extreme points NSEW
fg_extreme_nsew = FeatureGroup(name='Extreme points north/south/east/west', show=False)
fg_extreme_nsew.add_to(m)

extreme_nsew_data = [
    ('NORTH', '2018-09-04', 'Columbia Icefield, Jasper NP', (52.219966, -117.224376)),
    ('SOUTH', '2018-05-23', 'Key West', (24.546522, -81.797472)),
    ('EAST', '2018-06-30', 'Acadia NP', (44.328572, -68.174185)),
    ('WEST', '2018-08-01', 'Ruby Beach, Olympic NP', (47.709942, -124.416106)),
]

for direction, date, place, coord in extreme_nsew_data:
    Marker(
        location=coord,
        # TODO custom icon
        popup=html_escape([direction, place, coord, date]),
    ).add_to(fg_extreme_nsew)

summary_extreme_nsew = map(
    lambda x: (x[0], x[1], '{} - {}'.format(x[2], x[3])),
    extreme_nsew_data,
)

# 11 Facebook posts
fg_facebook = FeatureGroup(name='Facebook posts', show=False)
fg_facebook.add_to(m)

facebook_data = [
    #('2018-05-01 to 2018-05-03',
    # 'San Francisco',
    # '',
    # [[]],
    #),
    ('2018-05-03 to 2018-05-06',
     'Arizona',
     'https://www.facebook.com/mhhalverson/posts/10214603370971715',
     [[(-111.364628, 32.605047), (-111.364628, 32.048667), (-110.421808, 32.048667), (-110.421808, 32.605047), (-111.364628, 32.605047)]],
    ),
    ('2018-05-06 to 2018-05-09',
     'New Mexico',
     'https://www.facebook.com/mhhalverson/posts/10214611861183965',
     [[(-107.052234, 35.437892), (-106.686764, 32.610222), (-104.714319, 32.064686), (-104.064285, 32.064755), (-104.730264, 34.796961), (-107.052234, 35.437892)]],
    ),
    ('2018-05-09 to 2018-05-14',
     'Texas',
     'https://www.facebook.com/mhhalverson/posts/10214647074024264',
     [[(-98.486359, 33.423138), (-98.486359, 30.071288), (-95.812688, 30.071288), (-95.812688, 33.423138), (-98.486359, 33.423138)]],
    ),
    ('2018-05-14 to 2018-05-19',
     'New Orleans',
     'https://www.facebook.com/mhhalverson/posts/10214686987822084' and 'https://www.facebook.com/photo.php?fbid=10106654355949163&set=a.763822147163.2423144.3204198&type=3&theater',
     [[(-90.994541, 30.981744), (-90.994541, 29.45283), (-89.452761, 29.45283), (-89.452761, 30.981744), (-90.994541, 30.981744)]],
    ),
    ('2018-05-19 to 2018-05-25',
     'Florida',
     'https://www.facebook.com/mhhalverson/posts/10214716057188800',
     [[(-82.260209, 28.722341), (-82.260209, 24.345069), (-79.892713, 24.345069), (-79.892713, 28.722341), (-82.260209, 28.722341)]],
    ),
    ('2018-05-25 to 2018-06-03',
     'Georgia and South Carolina', 
     'https://www.facebook.com/mhhalverson/posts/10214783041263360',
     [[(-83.449913, 35.048522), (-83.449913, 31.900097), (-80.760202, 31.900097), (-80.760202, 35.048522), (-83.449913, 35.048522)]],
    ),
    ('2018-06-03 to 2018-06-07',
     'Tennessee and Kentucky',
     'https://www.facebook.com/mhhalverson/posts/10214815490914581',
     [[(-86.291668, 37.933145), (-87.247854, 35.958984), (-86.006265, 35.729173), (-85.446752, 37.154989), (-83.987198, 37.80856), (-84.190357, 38.3527), (-86.291668, 37.933145)]],
    ),
    # '2018-06-07 to 2018-06-11', 'Great Smoky Mountains and Shenandoah', 'https://www.facebook.com/mhhalverson/posts/10214849564246393'
    # '2018-06-11 to 2018-06-15', 'Washington DC', 'https://www.facebook.com/mhhalverson/posts/10214895582196813'
    # '2018-06-15 to 2018-06-18', 'Portland part I', 'https://www.facebook.com/mhhalverson/posts/10214917720030245'
    # '2018-06-18 to 2018-06-23', 'Philadelphia and New York City', 'https://www.facebook.com/mhhalverson/posts/10214961746130870'
    # '2018-06-23 to 2018-06-28', 'Boston and Rhode Island', 'https://www.facebook.com/mhhalverson/posts/10214991754041049'
    # '2018-06-28 to 2018-07-01', 'Maine', 'https://www.facebook.com/mhhalverson/posts/10215024532660494'
    # '2018-07-01 to 2018-07-03', 'New Hampshire', 'https://www.facebook.com/mhhalverson/posts/10215046110919937'
    # '2018-07-03 to 2018-07-07', 'Vermont and Upstate NY', 'https://www.facebook.com/mhhalverson/posts/10215064045648294'
    # '2018-07-07 to 2018-07-11', 'Michigan', 'https://www.facebook.com/mhhalverson/posts/10215082670073893'
    # '2018-07-11 to 2018-07-15', 'Chicago', 'https://www.facebook.com/mhhalverson/posts/10215136384056709'
    # '2018-07-15 to 2018-07-19', 'Minneapolis', 'https://www.facebook.com/mhhalverson/posts/10215155600417106'
    # '2018-07-19 to 2018-07-22', 'San Francisco', 'https://www.facebook.com/mhhalverson/posts/10215173199177064'
    # '2018-07-22 to 2018-07-28', 'Northeastern California', 'https://www.facebook.com/mhhalverson/posts/10215199932285375'
    # '2018-07-28 to 2018-08-02', 'Washington part I', 'https://www.facebook.com/mhhalverson/posts/10215279409032244'
    # '2018-08-02 to 2018-08-08', 'Washington part II', 'https://www.facebook.com/mhhalverson/posts/10215307816702418'
    # '2018-08-08 to 2018-08-20', 'Portland part II and NorCal Coast', 'https://www.facebook.com/mhhalverson/posts/10215340132510293'
    # '2018-08-20 to 2018-08-27', 'Northern Minnesota', 'https://www.facebook.com/mhhalverson/posts/10215397078453906'
    # '2018-08-27 to 2018-09-02', 'South Dakota', ''
    # '2018-09-02 to 2018-09-07', 'Banff', ''
    # '2018-09-07 to 2018-09-10', 'Santa Rosa', ''
    # '2018-09-10 to 2018-09-14', 'Glacier', ''
    # '2018-09-14 to 2018-09-', 'Yellowstone', ''
    # TODO fill this out
]

for date, place, link, coordinates in facebook_data:
    gj = folium.GeoJson(data={
        'type': 'Polygon',
        'coordinates': coordinates,
    })
    gj.add_child(folium.Popup('{}<br/>{}<br/><a href={}>link</a>'.format(place, date, link)))
    gj.add_to(fg_facebook)

summary_facebook = map(lambda f: f[:3], facebook_data)

# 12 Memorable meals
fg_meal = FeatureGroup(name='Memorable meals', show=False)
fg_meal.add_to(m)

summary_meal = []

coord_to_meals = defaultdict(list)  # key is latlng; value is list of tuples of (place name, meal description, date)

for day in trip:
    if DAY_MEALS in day:
        date = day[DAY_DATE]
        for place, meal_desc, coord in day[DAY_MEALS]:
            coord_to_meals[coord].append((place, meal_desc, date))
            summary_meal.append((date, '{}: {}'.format(place, meal_desc)))

for coord, meal_data in coord_to_meals.iteritems():
    popup_elems = [meal_data[0][0]]
    for _, meal_desc, date in meal_data:
        popup_elems.append('{} on {}'.format(meal_desc, date))
    popup = folium.Popup(html_escape(popup_elems))
    Marker(
        location=coord,
        # TODO custom icon
        popup=popup,
    ).add_to(fg_meal)

# 13 Pies
fg_pie = FeatureGroup(name='Pies baked', show=False)
fg_pie.add_to(m)

summary_pie = []

for i, day in enumerate(trip):
    if DAY_PIE in day:
        date = day[DAY_DATE]
        pie, recipient = day[DAY_PIE]
        coord = day[DAY_COORD]
        Marker(
            location=coord,
            # TODO custom icon
            popup=html_escape(['{} pie'.format(pie), 'for {}'.format(recipient), date]),
        ).add_to(fg_pie)
        summary_pie.append((date, '{} pie for {}'.format(pie, recipient)))

# 14 Tiki bars
fg_tiki = FeatureGroup(name='Tiki bars', show=False)
fg_tiki.add_to(m)

summary_tiki = []

for day in trip:
    if DAY_TIKI in day:
        date = day[DAY_DATE]
        bar, coord = day[DAY_TIKI]
        Marker(
            location=coord,
            # TODO custom icon
            popup=html_escape([bar, date]),
        ).add_to(fg_tiki)
        summary_tiki.append((date, bar))
        
# 15 Weddings
fg_wedding = FeatureGroup(name='Weddings', show=False)
fg_wedding.add_to(m)

summary_wedding = []

for day in trip:
    if DAY_WEDDING in day:
        date = day[DAY_DATE]
        couple, coord = day[DAY_WEDDING]
        
        Marker(
            location=coord,
            # TODO custom icon
            popup=html_escape([couple, date]),
        ).add_to(fg_wedding)

        summary_wedding.append((date, couple))

# 16 Caves explored
fg_cave = FeatureGroup(name='Caves explored', show=False)
fg_cave.add_to(m)

summary_cave = defaultdict(list)

for day in trip:
    if DAY_CAVES in day:
        for c in day[DAY_CAVES]:
            summary_cave[c].append(day[DAY_DATE])

for cave, date_ranges in summary_cave.iteritems():
    date_range = collapse_date_ranges(date_ranges)
    popup = html_escape([cave, date_range])
    add_park(cave, popup, fg_cave)

# 17 Highest/lowest elevation
fg_elevation = FeatureGroup(name='Highest/lowest elevation', show=False)
fg_elevation.add_to(m)

elevation_data = [
    ('2018-09-24', 'Trail Ridge Road Summit', 12183, coords.trail_ridge_road_summit),
    ('2018-05-14 to 2018-05-19', 'New Orleans', -4, coords.nola),
]

for date, place, elev, coord in elevation_data:
    Marker(
        location=coord,
        # TODO custom icon
        popup=html_escape([place, '{} ft'.format(elev), date]),
    ).add_to(fg_elevation)

summary_elevation = map(lambda w: w[:3], elevation_data)

# 18 Highest/lowest temperature
fg_temperature = FeatureGroup(name='Highest/lowest temperature', show=False)
fg_temperature.add_to(m)

temperature_data = [
    # TODO revisit at end for the actual high/low
    ('2018-05-05', 'Tucson', '100F/38C', coords.tucson),
    ('2018-09-03', 'Banff', '33F/1C', coords.two_jack)
]

for date, place, temp, coord in temperature_data:
    Marker(
        location=coord,
        # TODO custom icon
        popup=html_escape([place, temp, date]),
    ).add_to(fg_temperature)

summary_temperature = map(lambda w: w[:3], temperature_data)

# 19 Other notable events
fg_other = FeatureGroup(name='Other notable events', show=False)
fg_other.add_to(m)

summary_other = []

for day in trip:
    if DAY_OTHER in day:
        date = day[DAY_DATE]
        for event, coord in day[DAY_OTHER]:
        
            Marker(
                location=coord,
                # TODO custom icon
                popup=html_escape([event, date]),
            ).add_to(fg_other)

            summary_other.append((date, event))

### END OF FEATURE GROUPS

# Map finalize
LayerControl().add_to(m)

# Summary table
SUMMARY_BOOKS_READ = [
    'Iron Druid Chronicles #1: Hounded',
    'Iron Druid Chronicles #2: Hexed',
    'Iron Druid Chronicles #3: Hammered',
    'Iron Druid Chronicles #4: Tricked',
    'Iron Druid Chronicles #5: Trapped',
    'Iron Druid Chronicles #6: Hunted',
    'Iron Druid Chronicles #7: Shattered',
    'Iron Druid Chronicles #8: Staked',
    'Iron Druid Chronicles #8.5: Besieged',
    'Iron Druid Chronicles #9: Scourged',
    "Man's Search for Meaning",
    'The Lost City of Z',
    'The Slow Regard of Silent Things',
    'Red Rising',
    'Golden Son',
    'Morning Star',
    'The Great War for New Zealand',
    'Blood Meridian',
    # 'The Luminaries',
    # 'Iron Gold',
] # TODO render this somehow
# TODO add authors

executive_summary = [('Total days on the road', summary[SUMMARY_DAYS_TOTAL]),
 ('Days of camping', summary[SUMMARY_DAYS_CAMPING]),
 ('Days in cities', summary[SUMMARY_DAYS_CITY]),
 ('Total miles of driving', summary[SUMMARY_MILES]),
 ('Total hours of driving', summary[SUMMARY_HOURS]),
 ('Tanks of gas', 31 + #before MN
                  11 + #west coast leg
                  0),  #TODO after MN
 ('Number of flights', 6 + # from dc to portland / santa barbara and back
                       2 + # from mpls to sf and back
                       2 # from calgary to sf and back
 ),
 ('Number of books read', len(SUMMARY_BOOKS_READ)),
]
