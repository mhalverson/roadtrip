from datetime import timedelta
import os.path
from xml.sax.saxutils import escape

################################################################################
# Constants

# Day is a dictionary with the following fields
DAY_DATE = 'date'   #required; indicates the date of travel
DAY_NEW_LEG = 'new_leg' #optional; when set to true, indicates that a new leg of the trip began, and the day should not be considered as connected to the previous day. Special case to handle flights and the West Coast leg.
DAY_WAYPOINTS = 'waypoints' #optional; list of coords that should be used as waypoints before DAY_COORD (if present)
DAY_COORD = 'coord' #required; indicates where we slept at the end of DAY_DATE.
DAY_COORD_LABEL = 'coord_label'
DAY_COORD_TYPE = 'coord_type' #   indicates whether we were camping or in a city
DAY_COORD_CAMPING = 'camping'
DAY_COORD_CITY = 'city'
DAY_MILES = 'miles' #optional; indicates how many miles we drove that day
DAY_HOURS = 'hours' #optional; indicates how many hours we drove that day
DAY_FRIENDS = 'friends' #optional; dict where key = friends or family members who we saw on that day (string) and value = latlng
DAY_PARKS = 'parks' #optional; list indicating which parks we visited on that day. The geojson for parks are specified in a separate dict, so you'll have to add an entry in that dict when you add a new park to the list.
DAY_ANIMAL = 'animal' #optional; pair of (animal name, park name)
DAY_GOT_HIGH = 'got_high' #optional; list of triplets of (place name, height, coord) of high elevations we achieved
DAY_MEALS = 'meals' #optional; list of triplets of (place name, description of memorable meal, coord)
DAY_PIE = 'pie' #optional; pair of (pie name, recipient). The coord will be taken from the most recent DAY_COORD
DAY_TIKI = 'tiki' #optional; pair of (bar name, coord)
DAY_WEDDING = 'wedding' #optional; pair of (couple name, coord)
DAY_OTHER = 'other_notable_event' #optional; pair of (event description, coord)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PREFIX_FONT_AWESOME = 'fa'

########################################################################
# Utils

def format_elevation(height_ft):
    height_m = int(height_ft * 0.3048)
    return '{} ft/{} m'.format(height_ft, height_m)


# HTML: escape() and unescape() takes care of &, < and >.
html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}
def html_escape(strings, sep='<br/>'):
    no_empties = filter(lambda s: s, strings)
    formatted = map(lambda s: '{}'.format(s), no_empties)
    escaped = map(lambda s: escape(s, html_escape_table), formatted)
    return sep.join(escaped)


# Date utils
def format_date(d):
    return '{}'.format(d)

def format_date_range(first, last, sep=' to '):
    # collapse the range, joining with sep
    if first == last:
        return format_date(first)
    else:
        return '{}{}{}'.format(format_date(first), sep, format_date(last))

def break_into_ranges(dates):
    '''Given a list of datetime.dates, returns a list of lists of consecutive dates.
    '''
    # break into non-consecutive ranges
    ranges = []
    # pick your start
    first = dates[0]
    last = dates[0]
    for d in dates[1:]:
        # chew through consecutive ones
        if d - last == timedelta(1):
            last = d
            continue

        # we found the start of a new range!
        ranges.append((first, last))
        first = d
        last = d
    ranges.append((first, last))
    return ranges

def format_date_ranges(ranges, sep=', ', inner_sep=' to '):
    formatted_elems = [format_date_range(first,last,sep=inner_sep) for (first, last) in ranges]
    return sep.join(formatted_elems)

def collapse_date_ranges(dates, sep=', ', inner_sep=' to '):
    '''Given a list of datetime.dates, returns a string with consecutive dates collapsed into ranges (first - last).
    If there are multiple ranges, they will be separated by sep.
    '''
    # early return
    if not dates:
        return ''
    if len(dates) == 1:
        return str(dates[0])

    ranges = break_into_ranges(dates)
    return format_date_ranges(ranges, sep=sep, inner_sep=inner_sep)
