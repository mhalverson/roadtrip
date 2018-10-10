from collections import defaultdict
from datetime import date
import html
import json
from pprint import pprint
from xml.sax.saxutils import escape

import folium
from folium import FeatureGroup, GeoJson, LayerControl, Map, Marker, Popup, plugins
from shapely.geometry import shape, GeometryCollection, Point, mapping

from common import *
import coords
from dateutils import (format_date, format_date_range, break_into_ranges, collapse_date_ranges)
from map import m
from parks import parks
from trip import trip

# next steps --
#
# . populate TRIP! and other summary data (including facebook posts)
# . any other TODOs

PREFIX_FONT_AWESOME = 'fa'

ICON_CAMPING = 'eject'
COLOR_CAMPING = 'green'
ICON_CITY = 'home'
COLOR_CITY = 'blue'
ICON_FRIEND = 'user'
COLOR_FRIEND = 'orange'
# no icon needed for states
COLOR_STATE_VISITED = 'green'
COLOR_STATE_NOT_VISITED = 'yellow'
ICON_PARK = 'tree'
COLOR_PARK = 'green'
PREFIX_PARK = PREFIX_FONT_AWESOME
ICON_ANIMAL = 'binoculars'
COLOR_ANIMAL = 'gray'
PREFIX_ANIMAL = PREFIX_FONT_AWESOME
ICON_GOT_HIGH = 'chevron-up'
COLOR_GOT_HIGH = 'lightgray'
ICON_NSEW = 'compass'
COLOR_NSEW = 'blue'
PREFIX_NSEW = PREFIX_FONT_AWESOME
# no icon needed for Facebook posts
ICON_MEAL = 'cutlery'
COLOR_MEAL = 'orange'
ICON_PIE = 'pie-chart'
COLOR_PIE = 'green'
PREFIX_PIE = PREFIX_FONT_AWESOME
ICON_TIKI = 'glass'
COLOR_TIKI = 'blue'
ICON_WEDDING = 'heart'
COLOR_WEDDING = 'pink'
ICON_OTHER = 'exclamation-sign'
COLOR_OTHER = 'cadetblue'

summary_tables = {}

summary_ints = defaultdict(int)
SUMMARY_DAYS_TOTAL = 'days_total'
SUMMARY_DAYS_CAMPING = 'days_camping'
SUMMARY_DAYS_CITY = 'days_city'
SUMMARY_MILES = 'miles'
SUMMARY_HOURS = 'hours'
SUMMARY_LONGEST_DAY_MILES = 'longest_day_miles'
SUMMARY_LONGEST_DAY_HOURS = 'longest_day_hours'


### BEGINNING OF FEATURE GROUPS

# A feature group has the following properties:
#  - map overlay of markers, where marker popups have date + description
#  - entry in summary_tables, including date + description

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

# 1 Sleep
fg_sleep_name = 'Where we slept (camping in green, cities in blue)'
fg_sleep = FeatureGroup(name=fg_sleep_name, show=False)
fg_sleep.add_to(m)

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

sleep_markers = {} # key is latlng, value is (coord_label, coord_type, icon)
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
        
        sleep_markers[sleep_coord] = (coord_label, coord_type, icon)
    sleep_dates[sleep_coord].append(day[DAY_DATE])
    summary_ints[SUMMARY_DAYS_TOTAL] += 1
    if DAY_MILES in day:
        miles = day[DAY_MILES]
        summary_ints[SUMMARY_MILES] += miles
        if miles > summary_ints[SUMMARY_LONGEST_DAY_MILES]:
            summary_ints[SUMMARY_LONGEST_DAY_MILES] = miles
    if DAY_HOURS in day:
        hours = day[DAY_HOURS]
        summary_ints[SUMMARY_HOURS] += hours
        if hours > summary_ints[SUMMARY_LONGEST_DAY_HOURS]:
            summary_ints[SUMMARY_LONGEST_DAY_HOURS] = hours

summary_sleep = [] # list of (collapsed date range, place)

for sleep_coord, dates in sleep_dates.iteritems():
    (coord_label, coord_type, icon) = sleep_markers[sleep_coord]
    popup = '{}<br/>{}'.format(coord_label, collapse_date_ranges(dates, sep='<br/>'))
    Marker(
        location=sleep_coord,
        popup=folium.Popup(popup),
        icon=icon,
    ).add_to(fg_sleep)
    
    for first, last in break_into_ranges(dates):
        date_range = format_date_range(first, last)
        summary_sleep.append((date_range, coord_label))
    
    summary_type = {
        DAY_COORD_CAMPING: SUMMARY_DAYS_CAMPING,
        DAY_COORD_CITY: SUMMARY_DAYS_CITY,
    }[coord_type]
    summary_ints[summary_type] += len(dates)

summary_tables[fg_sleep_name] = sorted(summary_sleep)

# 2 Friend
fg_friend_name = 'Who we saw'
fg_friend = FeatureGroup(name=fg_friend_name, show=False)
fg_friend.add_to(m)

# key is coord, value is dict again with key of friend and value of list of dates we saw them
coord_to_friend_to_dates = defaultdict(lambda: defaultdict(list))

for i, day in enumerate(trip):
    if DAY_FRIENDS in day:
        for (friend, coord) in day[DAY_FRIENDS].iteritems():
            date = day[DAY_DATE]
            coord_to_friend_to_dates[coord][friend].append(date)

summary_friend = []

for coord, friend_dict in coord_to_friend_to_dates.iteritems():
    popup_elems = []
    for friend, dates in friend_dict.iteritems():
        # popup will GROUP BY coord
        popup_elems.append((friend, collapse_date_ranges(dates, sep='<br/>')))
        # summary has no coords so we break up all the date ranges
        for first, last in break_into_ranges(dates):
            date_range = format_date_range(first, last)
            summary_friend.append((date_range, friend))
    popup_elems.sort(key=lambda x: x[1])
    formatted_popup_elems = map(lambda x: '{}<br/>{}'.format(x[0], x[1]), popup_elems)
    popup = '<br/>'.join(formatted_popup_elems)
    Marker(
        location=coord,
        popup=popup,
        icon=folium.Icon(icon=ICON_FRIEND, color=COLOR_FRIEND),
    ).add_to(fg_friend)

summary_tables[fg_friend_name] = sorted(summary_friend)

# 3 State
fg_state_name = 'States we drove through'
fg_state = FeatureGroup(name=fg_state_name, show=False)
fg_state.add_to(m)

# Load states data from folium itself o_O A bit weird, but if it's there... why not?
states = None
with open("./folium/examples/data/us-states.json") as f:
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
            'fillColor': COLOR_STATE_VISITED if visited(feature['properties']['abbrev']) else COLOR_STATE_NOT_VISITED,
        },
    )
    gj.add_child(Popup(popup))
    gj.add_to(fg_state)

summary_tables[fg_state_name] = sorted([(collapse_date_ranges(v) or 'did not visit', str(k)) for k, v in summary_state.iteritems()])

# 4 Park
fg_park_name = 'Parks we visited'
fg_park = FeatureGroup(name=fg_park_name, show=False)
fg_park.add_to(m)

summary_park = defaultdict(list)

for day in trip:
    if DAY_PARKS in day:
        for p in day[DAY_PARKS]:
            summary_park[p].append(day[DAY_DATE])

def add_park(park, popup, feature_group, icon):
    geom_raw = parks[park]

    gc_raw = GeometryCollection([shape(geom_raw)])
    gc_simple = GeometryCollection.simplify(gc_raw, 0.01) # I *think* the tolerance units are in degrees latitude/longitude

    geojson_simple = GeoJson(mapping(gc_simple))
    geojson_simple.add_to(feature_group)

    centroid = gc_raw.centroid
    Marker(
        location=(centroid.y, centroid.x),
        popup=popup,
        icon=icon,
    ).add_to(feature_group)

for p, date_ranges in summary_park.iteritems():
    date_range = collapse_date_ranges(date_ranges)
    popup = html_escape([p, date_range])
    icon = folium.Icon(icon=ICON_PARK, prefix=PREFIX_PARK, color=COLOR_PARK)
    add_park(p, popup, fg_park, icon)

summary_tables[fg_park_name] = sorted([(collapse_date_ranges(v), k) for k, v in summary_park.iteritems()])

# 5 Animal sightings
fg_animal_name = 'Animal sightings'
fg_animal = FeatureGroup(name=fg_animal_name, show=False)
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
    icon = folium.Icon(icon=ICON_ANIMAL, prefix=PREFIX_ANIMAL, color=COLOR_ANIMAL)
    add_park(park, popup, fg_animal, icon)

summary_tables[fg_animal_name] = sorted(summary_animal)

# 6 Mountains climbed aka getting high
fg_got_high_name = 'High elevations'
fg_got_high = FeatureGroup(name=fg_got_high_name, show=False)
fg_got_high.add_to(m)

summary_got_high = []

def format_elevation(height_ft):
    height_m = int(height_ft * 0.3048)
    return '{} ft/{} m'.format(height_ft, height_m)

for day in trip:
    if DAY_GOT_HIGH in day:
        date = day[DAY_DATE]
        for (place, height_ft, coord) in day[DAY_GOT_HIGH]:
            height_str = format_elevation(height_ft)
            Marker(
                location=coord,
                popup=html_escape([place, height_str, date]),
                icon=folium.Icon(icon=ICON_GOT_HIGH, color=COLOR_GOT_HIGH),
            ).add_to(fg_got_high)
            summary_got_high.append((format_date(date), place, height_str))

summary_tables[fg_got_high_name] = summary_got_high

# 7 Extreme points NSEW
fg_extreme_nsew_name = 'Extreme points north/south/east/west'
fg_extreme_nsew = FeatureGroup(name=fg_extreme_nsew_name, show=False)
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
        icon=folium.Icon(icon=ICON_NSEW, prefix=PREFIX_NSEW, color=COLOR_NSEW),
        popup=html_escape([direction, place, coord, date]),
    ).add_to(fg_extreme_nsew)

summary_extreme_nsew = map(
    lambda x: (x[0], x[1], '{}: {}'.format(x[2], x[3])),
    extreme_nsew_data,
)
summary_tables[fg_extreme_nsew_name] = summary_extreme_nsew

# 8 Facebook posts
fg_facebook_name = 'Facebook posts'
fg_facebook = FeatureGroup(name=fg_facebook_name, show=False)
fg_facebook.add_to(m)

facebook_data = {
    tuple([((-122.9260, 38.1086), (-122.9260, 37.4749), (-121.9647, 37.4749), (-121.9647, 38.1086), (-122.9260, 38.1086))]):
    [('2018-05-01 to 2018-05-03',
      'San Francisco, departure day',
      'https://www.facebook.com/photo.php?fbid=10155154109205946'),
     ('2018-07-19 to 2018-07-22',
      'San Francisco, wedding',
      'https://www.facebook.com/mhhalverson/posts/10215173199177064'),
    ],

    tuple([((-111.364628, 32.605047), (-111.364628, 32.048667), (-110.421808, 32.048667), (-110.421808, 32.605047), (-111.364628, 32.605047))]):
    [('2018-05-03 to 2018-05-06',
      'Arizona',
      'https://www.facebook.com/mhhalverson/posts/10214603370971715'),
    ],

    tuple([((-107.052234, 35.437892), (-106.686764, 32.610222), (-104.714319, 32.064686), (-104.064285, 32.064755), (-104.730264, 34.796961), (-107.052234, 35.437892))]):
    [('2018-05-06 to 2018-05-09',
       'New Mexico',
       'https://www.facebook.com/mhhalverson/posts/10214611861183965'),
    ],

    tuple([((-98.486359, 33.423138), (-98.486359, 30.071288), (-95.812688, 30.071288), (-95.812688, 33.423138), (-98.486359, 33.423138))]):
    [('2018-05-09 to 2018-05-14',
      'Texas',
      'https://www.facebook.com/mhhalverson/posts/10214647074024264'),
    ],

    tuple([((-90.994541, 30.981744), (-90.994541, 29.45283), (-89.452761, 29.45283), (-89.452761, 30.981744), (-90.994541, 30.981744))]):
    [('2018-05-14 to 2018-05-19',
      'New Orleans',
      'https://www.facebook.com/mhhalverson/posts/10214686987822084'),
    ],

    tuple([((-82.260209, 28.722341), (-82.260209, 24.345069), (-79.892713, 24.345069), (-79.892713, 28.722341), (-82.260209, 28.722341))]):
    [('2018-05-19 to 2018-05-25',
      'Florida',
      'https://www.facebook.com/mhhalverson/posts/10214716057188800'),
    ],

    tuple([((-83.449913, 35.048522), (-83.449913, 31.900097), (-80.760202, 31.900097), (-80.760202, 35.048522), (-83.449913, 35.048522))]):
    [('2018-05-25 to 2018-06-03',
      'Georgia and South Carolina', 
      'https://www.facebook.com/mhhalverson/posts/10214783041263360'),
    ],

    tuple([((-86.291668, 37.933145), (-87.247854, 35.958984), (-86.006265, 35.729173), (-85.446752, 37.154989), (-83.987198, 37.80856), (-84.190357, 38.3527), (-86.291668, 37.933145))]):
    [('2018-06-03 to 2018-06-07',
      'Tennessee and Kentucky',
      'https://www.facebook.com/mhhalverson/posts/10214815490914581'),
    ],

    tuple([((-83.8477, 35.7822), (-83.3892, 35.1941), (-77.8081, 38.4988), (-78.4233, 38.9103), (-83.8477, 35.7822))]):
    [('2018-06-07 to 2018-06-11',
      'Great Smoky Mountains and Shenandoah',
      'https://www.facebook.com/mhhalverson/posts/10214849564246393'),
    ],

    tuple([((-77.3218, 39.1258), (-77.3218, 38.7069), (-76.7340, 38.7069), (-76.7340, 39.1258), (-77.3218, 39.1258))]):
    [('2018-06-11 to 2018-06-15',
      'Washington DC',
      'https://www.facebook.com/mhhalverson/posts/10214895582196813'),
    ],

    tuple([((-122.9260, 45.6716), (-122.9260, 45.2788), (-122.3273, 45.2788), (-122.3273, 45.6716), (-122.9260, 45.6716))]):
    [('2018-06-15 to 2018-06-18',
      'Portland part I',
      'https://www.facebook.com/mhhalverson/posts/10214917720030245'),
     ('2018-08-08 to 2018-08-20',
      'Portland part II and NorCal Coast',
      'https://www.facebook.com/mhhalverson/posts/10215340132510293'),
    ],

    tuple([((-75.4181, 39.9506), (-75.0666, 39.7060), (-73.6493, 40.7544), (-74.1397, 40.9254), (-75.4181, 39.9506))]):
    [('2018-06-18 to 2018-06-23',
      'Philadelphia and New York City',
      'https://www.facebook.com/mhhalverson/posts/10214961746130870'),
    ],

    tuple([((-71.8428, 42.6259), (-71.8428, 41.5250), (-70.5542, 41.5250), (-70.5542, 42.6259), (-71.8428, 42.6259))]):
    [('2018-06-23 to 2018-06-28',
      'Boston and Rhode Island',
      'https://www.facebook.com/mhhalverson/posts/10214991754041049'),
    ],

    tuple([((-68.8843, 44.7779), (-68.8843, 44.0560), (-67.8625, 44.0560), (-67.8625, 44.7779), (-68.8843, 44.7779))]):
    [('2018-06-28 to 2018-07-01',
      'Maine',
      'https://www.facebook.com/mhhalverson/posts/10215024532660494'),
    ],

    tuple([((-71.8127, 44.8415), (-71.8127, 44.0257), (-71.0327, 44.0257), (-71.0327, 44.8415), (-71.8127, 44.8415))]):
    [('2018-07-01 to 2018-07-03',
      'New Hampshire',
      'https://www.facebook.com/mhhalverson/posts/10215046110919937'),
    ],

    tuple([((-73.2458, 44.8169), (-76.5198, 43.2132), (-79.2993, 43.2772), (-79.2041, 42.7963), (-81.9946, 41.6246), (-81.6870, 41.3035), (-78.3801, 42.7318), (-76.4355, 42.1806), (-75.8062, 42.7993), (-72.8069, 44.0283), (-72.7844, 44.3710), (-73.2458, 44.8169))]):
    [('2018-07-03 to 2018-07-07',
      'Vermont and Upstate NY',
      'https://www.facebook.com/mhhalverson/posts/10215064045648294'),
    ],

    tuple([((-84.2651, 42.6824), (-84.2651, 42.0167), (-82.7930, 42.0167), (-82.7930, 42.6824), (-84.2651, 42.6824))]):
    [('2018-07-07 to 2018-07-11',
      'Michigan',
      'https://www.facebook.com/mhhalverson/posts/10215082670073893'),
    ],

    tuple([((-88.0510, 42.3179), (-88.0510, 41.7549), (-87.2644, 41.7549), (-87.2644, 42.3179), (-88.0510, 42.3179))]):
    [('2018-07-11 to 2018-07-15',
      'Chicago',
      'https://www.facebook.com/mhhalverson/posts/10215136384056709'),
    ],

    tuple([((-93.7473, 45.2764), (-93.5276, 44.7249), (-91.6269, 44.5372), (-89.4516, 42.8937), (-89.0226, 43.22770), (-91.2968, 44.9711), (-93.7473, 45.2764))]):
    [('2018-07-15 to 2018-07-19',
      'Minneapolis',
      'https://www.facebook.com/mhhalverson/posts/10215155600417106'),
    ],

    # there's a "San Francisco" entry here that's doubled up with the first entry of this list.

    tuple([((-121.8961, 38.4666), (-121.5720, 38.4752), (-120.8623, 41.0062), (-121.3182, 41.9037), (-121.6972, 41.8996), (-122.4784, 40.4709), (-121.8961, 38.4666))]):
    [('2018-07-22 to 2018-07-28',
      'Northeastern California',
      'https://www.facebook.com/mhhalverson/posts/10215199932285375'),
    ],

    tuple([((-121.9592, 45.4986), (-121.5637, 45.6832), (-123.6401, 47.6321), (-124.0961, 47.4504), ( -121.9592, 45.4986))]):
    [('2018-07-28 to 2018-08-02',
      'Washington part I',
      'https://www.facebook.com/mhhalverson/posts/10215279409032244'),
    ],

    tuple([((-121.5258, 48.8304), (-121.9263, 46.6947), (-121.3330, 46.5966), (-120.2124, 48.7707), (-121.5258, 48.8304))]):
    [('2018-08-02 to 2018-08-08',
      'Washington part II',
      'https://www.facebook.com/mhhalverson/posts/10215307816702418'),
    ],

    tuple([((-122.4613, 43.3003), (-124.4421, 41.9677), (-124.3982, 40.7140), (-123.8269, 40.7473), (-123.1677, 42.1145), (-122.0273, 42.9352), (-122.4613, 43.3003))]):
    [('2018-08-08 to 2018-08-20',
      'Portland part II and NorCal Coast', # the Portland polygon also has this entry :)
      'https://www.facebook.com/mhhalverson/posts/10215340132510293'),
    ],

    tuple([((-92.2711, 48.2353), (-92.2711, 47.7943), (-88.8873, 47.7943), (-88.8873, 48.2353), (-92.2711, 48.2353))]):
    [('2018-08-20 to 2018-08-27',
      'Northern Minnesota',
      'https://www.facebook.com/mhhalverson/posts/10215397078453906'),
    ],

    tuple([((-105.1282, 44.7857), (-105.1282, 43.1972), (-101.4587, 43.1972), (-101.4587, 44.7857), (-105.1282, 44.7857))]):
    [('2018-08-27 to 2018-09-02',
      'South Dakota',
      'https://www.facebook.com/mhhalverson/posts/10215497401161911'),
    ],

    tuple([((-117.7147, 52.4110), (-117.7147, 50.9119), (-115.0999, 50.9119), (-115.0999, 52.4110), (-117.7147, 52.4110))]):
    [('2018-09-02 to 2018-09-07',
      'Banff',
      'https://www.facebook.com/mhhalverson/posts/10215526934940237'),
    ],

    tuple([((-123.2281, 38.8761), (-123.2281, 38.3395), (-122.3959, 38.3395), (-122.3959, 38.8761), (-123.2281, 38.8761))]):
    [('2018-09-07 to 2018-09-10',
      'Santa Rosa',
      'https://www.facebook.com/mhhalverson/posts/10215559846483005'),
    ],

    tuple([((-114.0381, 49.1242), (-114.0381, 48.6039), (-113.1152, 48.6039), (-113.1152, 49.1242), (-114.0381, 49.1242))]):
    [('2018-09-10 to 2018-09-14',
      'Glacier',
      'https://www.facebook.com/mhhalverson/posts/10215571606456997'),
    ],

    tuple([((-111.2476, 44.9181), (-111.2476, 44.3199), (-110.2588, 44.3199), (-110.2588, 44.9181), (-111.2476, 44.9181))]):
    [('2018-09-14 to 2018-09-20',
      'Yellowstone',
      'https://www.facebook.com/mhhalverson/posts/10215583821122356'),
    ],

    tuple([((-111.2974, 43.8931), (-106.4980, 41.1776), (-105.9082, 40.0276), (-104.5459, 40.0276), (-104.9414, 41.5250), (-110.1654, 43.9731), (-111.2974, 43.8931))]):
    [('2018-09-20 to 2018-09-26',
      'Grand Teton and Rocky Mountain',
      'https://www.facebook.com/mhhalverson/posts/10215609289959061'),
    ],

    tuple([((-110.2764, 38.4458), (-109.5074, 37.5541), (-108.2824, 37.0297), (-108.2153, 37.4182), (-109.4788, 38.9551), (-110.2764, 38.4458))]):
    [('2018-09-26 to 2018-10-02',
      'Mesa Verde and Utah part 1',
      'https://www.facebook.com/mhhalverson/posts/10215629675508687'),
    ],

    tuple([((-113.2877, 37.5215), (-113.0790, 37.0408), (-112.0407, 37.4038), (-111.9968, 37.7304), (-112.6010, 37.8649), (-113.2877, 37.5215))]):
    [('2018-10-02 to 2018-10-08',
      'Utah part 2',
      ''), # TODO, make sure it's public
    ],

    # '2018-10-08 to 2018-10-', 'Grand Canyon, Scottsdale, and SoCal deserts', '', [[]], # TODO, make sure it's public
    # TODO finish filling this out
}

for polygon, visits in facebook_data.iteritems():
    gj = folium.GeoJson(data={
        'type': 'Polygon',
        'coordinates': polygon,
    })

    popups = []
    for date, place, link in visits:
        popups.append('{}<br/>{}<br/><a href={}>link</a>'.format(place, date, link))

    gj.add_child(folium.Popup('<br/>'.join(popups)))
    gj.add_to(fg_facebook)

summary_facebook = []
for _, visits in facebook_data.iteritems():
    summary_facebook.extend(visits)
summary_facebook = sorted(list(set(summary_facebook)))

summary_tables[fg_facebook_name] = summary_facebook

# 9 Memorable meals
fg_meal_name = 'Memorable meals'
fg_meal = FeatureGroup(name=fg_meal_name, show=False)
fg_meal.add_to(m)

summary_meal = []

coord_to_meals = defaultdict(list)  # key is latlng; value is list of tuples of (place name, meal description, date)

for day in trip:
    if DAY_MEALS in day:
        date = day[DAY_DATE]
        for place, meal_desc, coord in day[DAY_MEALS]:
            coord_to_meals[coord].append((place, meal_desc, date))
            summary_meal.append((format_date(date), '{}: {}'.format(place, meal_desc)))

for coord, meal_data in coord_to_meals.iteritems():
    popup_elems = [meal_data[0][0]]
    for _, meal_desc, date in meal_data:
        popup_elems.append('{} on {}'.format(meal_desc, date))
    popup = folium.Popup(html_escape(popup_elems))
    Marker(
        location=coord,
        icon=folium.Icon(icon=ICON_MEAL, color=COLOR_MEAL),
        popup=popup,
    ).add_to(fg_meal)

summary_tables[fg_meal_name] = summary_meal

# 10 Pies
fg_pie_name = 'Pies baked'
fg_pie = FeatureGroup(name=fg_pie_name, show=False)
fg_pie.add_to(m)

summary_pie = []

for i, day in enumerate(trip):
    if DAY_PIE in day:
        date = day[DAY_DATE]
        pie, recipient = day[DAY_PIE]
        coord = day[DAY_COORD]
        Marker(
            location=coord,
            icon=folium.Icon(icon=ICON_PIE, prefix=PREFIX_PIE, color=COLOR_PIE),
            popup=html_escape(['{} pie'.format(pie), 'for {}'.format(recipient), date]),
        ).add_to(fg_pie)
        summary_pie.append((format_date(date), '{} pie for {}'.format(pie, recipient)))

summary_tables[fg_pie_name] = summary_pie

# 11 Tiki bars
fg_tiki_name = 'Tiki bars'
fg_tiki = FeatureGroup(name=fg_tiki_name, show=False)
fg_tiki.add_to(m)

summary_tiki = []

for day in trip:
    if DAY_TIKI in day:
        date = day[DAY_DATE]
        bar, coord = day[DAY_TIKI]
        Marker(
            location=coord,
            icon=folium.Icon(icon=ICON_TIKI, color=COLOR_TIKI),
            popup=html_escape([bar, date]),
        ).add_to(fg_tiki)
        summary_tiki.append((format_date(date), bar))
 
summary_tables[fg_tiki_name] = summary_tiki

# 12 Weddings
fg_wedding_name = 'Weddings'
fg_wedding = FeatureGroup(name=fg_wedding_name, show=False)
fg_wedding.add_to(m)

summary_wedding = []

for day in trip:
    if DAY_WEDDING in day:
        date = day[DAY_DATE]
        couple, coord = day[DAY_WEDDING]
        
        Marker(
            location=coord,
            icon=folium.Icon(icon=ICON_WEDDING, color=COLOR_WEDDING),
            popup=html_escape([couple, date]),
        ).add_to(fg_wedding)

        summary_wedding.append((format_date(date), couple))

summary_tables[fg_wedding_name] = summary_wedding

# 14 Other notable events
fg_other_name = 'Other notable events'
fg_other = FeatureGroup(name=fg_other_name, show=False)
fg_other.add_to(m)

summary_other = []

for day in trip:
    if DAY_OTHER in day:
        date = day[DAY_DATE]
        for event, coord in day[DAY_OTHER]:
        
            Marker(
                location=coord,
                icon=folium.Icon(icon=ICON_OTHER, color=COLOR_OTHER),
                popup=html_escape([event, date]),
            ).add_to(fg_other)

            summary_other.append((format_date(date), event))

summary_tables[fg_other_name] = summary_other

### END OF FEATURE GROUPS

# Map finalization
LayerControl().add_to(m)

# Summary generation
executive_summary = [ # TODO revisit when done
 ('Total days on the road', str(summary_ints[SUMMARY_DAYS_TOTAL])),
 ('Days of camping', str(summary_ints[SUMMARY_DAYS_CAMPING])),
 ('Days in cities', str(summary_ints[SUMMARY_DAYS_CITY])),
 ('Total miles of driving', str(summary_ints[SUMMARY_MILES])), # TODO compare this to the gas logs from van + Elantra
 ('Total hours of driving', str(summary_ints[SUMMARY_HOURS])),
 ('Longest driving day', '{} miles / {} hours'.format(
     summary_ints[SUMMARY_LONGEST_DAY_MILES],
     summary_ints[SUMMARY_LONGEST_DAY_HOURS])),
 ('Highest elevation', '{} on 2018-09-24 on Trail Ridge Road Summit in Rocky Mountain NP'.format(format_elevation(12183))),
 ('Lowest elevation', '{} from 2018-05-14 to 2018-05-19 in New Orleans'.format(format_elevation(-4))),
 ('Highest temperature', '100F/38C on 2018-05-05 in Tucson'),
 ('Lowest temperature', '26F/-3C on 2018-09-26 in Rocky Mountain NP'),
 ('Favourite city', 'Chicago for Claire, DC for Matt'),
 ('Least favourite city', 'Dallas for Claire, Augusta for Matt'),
 ('Favourite nature', 'Banff NP for both of us'),
 ('Least favourite nature', 'Congaree NP for both of us'),
 ('Tanks of gas', str(31 + #before MN
                      11 + #west coast leg
                      0)),  #TODO after MN
 ('Number of flights', str(6 + # from dc to portland / santa barbara and back
                           2 + # from mpls to sf and back
                           2)), # from calgary to sf and back
 ('Books read', 'Iron Druid Chronicles #1: Hounded by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #2: Hexed by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #3: Hammered by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #4: Tricked by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #5: Trapped by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #6: Hunted by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #7: Shattered by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #8: Staked by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #8.5: Besieged by Kevin Hearne'),
 ('', 'Iron Druid Chronicles #9: Scourged by Kevin Hearne'),
 ('', "Man's Search for Meaning by Viktor Frankl"),
 ('', 'The Lost City of Z by David Grann'),
 ('', 'The Slow Regard of Silent Things by Patrick Rothfuss'),
 ('', 'Red Rising by Pierce Brown'),
 ('', 'Golden Son by Pierce Brown'),
 ('', 'Morning Star by Pierce Brown'),
 ('', 'Iron Gold by Pierce Brown'),
 ('', "The Great War for New Zealand by Vincent O'Malley"),
 ('', 'Blood Meridian by Cormac McCarthy'),
 # ('', 'The Luminaries by Eleanor Catton'),
]
summary_tables['executive_summary'] = executive_summary

summary_tables_html = {}
for k, v in summary_tables.iteritems():
    h = html.HTML()
    t = h.table(border='1')
    for row in v:
        r = t.tr()
        for item in row:
            if k == fg_facebook_name and item == row[-1]:
                r.td(h.a(item, href=item), style='padding:10px', escape=False)
            else:
                r.td(item, style='padding:10px')
    summary_tables_html[k] = '{}'.format(t)


if __name__=='__main__':
    map_filename = 'rendered_map.html'
    m.save(map_filename)

    summary_filename = 'summary_data.js'
    with open(summary_filename, 'w') as f:
        f.write('var summary_data = ')
        f.write(json.dumps(summary_tables_html))
        f.write(';')
