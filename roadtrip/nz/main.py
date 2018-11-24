from collections import defaultdict
from datetime import date
import html
import json
import os.path
from pprint import pprint
from xml.sax.saxutils import escape

import folium
from folium import FeatureGroup, GeoJson, LayerControl, Map, Marker, Popup, plugins
from shapely.geometry import shape, GeometryCollection, Point, mapping

from roadtrip.common import *

import roadtrip.nz.coords as coords
from roadtrip.nz.map import m
from roadtrip.nz.trip import trip

ICON_START_END = 'flag'
COLOR_START_END = 'blue'
ICON_CAMPING = 'eject'
COLOR_CAMPING = 'green'
ICON_CITY = 'home'
COLOR_CITY = 'blue'
ICON_FRIEND = 'user'
COLOR_FRIEND = 'orange'
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
ICON_OTHER = 'exclamation-sign'
COLOR_OTHER = 'cadetblue'

summary_tables = {}

summary_ints = defaultdict(int)
SUMMARY_DAYS_TOTAL = 'days_total'
SUMMARY_DAYS_CAMPING = 'days_camping'
SUMMARY_DAYS_CITY = 'days_city'
SUMMARY_KMS = 'kilometres'
SUMMARY_HOURS = 'hours'
SUMMARY_LONGEST_DAY_KMS = 'longest_day_kms'
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

# Start/End
fg_start_end = FeatureGroup(name='Start/End', show=True)
fg_start_end.add_to(m)

Marker(
    location=coords.auckland,
    popup='Start: 2018-11-10',
    icon=folium.Icon(icon=ICON_START_END, color=COLOR_START_END),
).add_to(fg_start_end)
Marker(
    location=coords.wellington,
    popup='End: 2018-12-17',
    icon=folium.Icon(icon=ICON_START_END, color=COLOR_START_END),
).add_to(fg_start_end)

# 1 Sleep
fg_sleep_name = 'Where we slept (camping in green, cities in blue)'
fg_sleep = FeatureGroup(name=fg_sleep_name, show=False)
fg_sleep.add_to(m)

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
    if DAY_KMS in day:
        kms = day[DAY_KMS]
        summary_ints[SUMMARY_KMS] += kms
        if kms > summary_ints[SUMMARY_LONGEST_DAY_KMS]:
            summary_ints[SUMMARY_LONGEST_DAY_KMS] = kms
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
    ('NORTH', '2018-11-20', 'Kapowairua (Spirits Bay)', coords.spirits_bay),
    ('SOUTH', '', '', (24.546522, -81.797472)), # TODO
    ('EAST', '2018-11-27', 'East Cape', (-37.690286, 178.548075)), # TODO
    ('WEST', '2018-11-20', 'Cape Reinga', coords.cape_reinga),
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
    tuple([((-36.755888, 174.683553), (-36.927996, 174.683553), (-36.927996, 174.910715), (-36.755888, 174.910715), (-36.755888, 174.683553))]):
    [('2018-11-10 to 2018-11-17',
      'Auckland',
      'https://www.facebook.com/mhhalverson/posts/10215947570215856')],

    tuple([((-34.343887, 172.537870), (-35.786629, 172.537870), (-35.786629, 174.483424), (-34.343887, 174.483424), (-34.343887, 172.537870))]):
    [('2018-11-17 to 2018-11-21',
      'Northland',
      'https://www.facebook.com/mhhalverson/posts/10215979806901753')],

    # TODO
    # tuple([]): 
    # [('2018-11-21 to 2018-11-',
    #   '',
    #   '')],
}

for polygon, visits in facebook_data.iteritems():
    lng_lat_polygon = [[(lng, lat) for (lat, lng) in polygon[0]]]
    gj = folium.GeoJson(data={
        'type': 'Polygon',
        'coordinates': lng_lat_polygon,
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

# key is coord, value is list of tuples of (date, pie, recipient)
coord_to_pies = defaultdict(list)

summary_pie = []

for day in trip:
    if DAY_PIE in day:
        date = day[DAY_DATE]
        (pie, recipient) = day[DAY_PIE]
        coord = day[DAY_COORD]
        coord_to_pies[coord].append((date, pie, recipient))

        summary_pie.append((format_date(date), '{} pie for {}'.format(pie, recipient)))

for coord, pie_data in coord_to_pies.iteritems():
    # popup text should be "Samoa pie for Neil on 2018-11-10 <br/> Manhattan pie for Emma and Kenny on 2018-11-15"
    popup_lines = []
    for (date, pie, recipient) in pie_data:
        line = html_escape(['{} pie'.format(pie), 'for {}'.format(recipient), 'on {}'.format(date)], sep=' ')
        popup_lines.append(line)
        Marker(
            location=coord,
            icon=folium.Icon(icon=ICON_PIE, prefix=PREFIX_PIE, color=COLOR_PIE),
            popup='<br/>'.join(popup_lines),
        ).add_to(fg_pie)

summary_tables[fg_pie_name] = summary_pie

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

# Summary generation # TODO revisit at end
executive_summary = [
 ('Total days on the road', str(summary_ints[SUMMARY_DAYS_TOTAL])),
 ('Days of camping', str(summary_ints[SUMMARY_DAYS_CAMPING])),
 ('Days in cities', str(summary_ints[SUMMARY_DAYS_CITY])),
 ('Total kms of driving', str(summary_ints[SUMMARY_KMS])),
 ('Total hours of driving', str(summary_ints[SUMMARY_HOURS])),
 ('Longest driving day', '{} kms / {} hours'.format(
     summary_ints[SUMMARY_LONGEST_DAY_KMS],
     summary_ints[SUMMARY_LONGEST_DAY_HOURS])),
 ('Number of car accidents', '0'),
 ('Number of hospital visits', '0'),
 ('Number of thefts', '0'),
 ('Highest elevation', '{} on 2018-09-24 on Trail Ridge Road Summit in Rocky Mountain NP'.format(format_elevation(12183))),
 ('Lowest elevation', '{} on 2018-10-15 at the Salton Sea'.format(format_elevation(-236))),
 ('Highest temperature', ''),
 ('Lowest temperature', ''),
 ('Favourite city', ''),
 ('Least favourite city', ''),
 ('Favourite nature', ''),
 ('Least favourite nature', ''),
 ('Books read', 'Skyward by Brandon Sanderson'),
 ('', 'Kokoda by Peter FitzSimons'),
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
    map_filename = os.path.join(BASE_DIR, 'nz.rendered_map.html')
    print 'Writing map HTML to file: {}'.format(map_filename)
    with open(map_filename, 'w'):
        m.save(map_filename)

    summary_filename = os.path.join(BASE_DIR, 'nz.summary_data.js')
    print 'Writing summary data to file: {}'.format(summary_filename)
    with open(summary_filename, 'w') as f:
        f.write('var summary_data = ')
        f.write(json.dumps(summary_tables_html))
        f.write(';')
