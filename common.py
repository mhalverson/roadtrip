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

# For a day template, see trip.py.
