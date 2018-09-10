from datetime import date

from common import *
import coords

trip = [
    # Trip is a list of Day records
    {
        DAY_DATE: date(2018,5,1),
        DAY_COORD: coords.sf,
        DAY_COORD_LABEL: 'San Francisco',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_FRIENDS: {'Nina and Alex': coords.sf},
    },
    {
        DAY_DATE: date(2018,5,2),
        DAY_COORD: (35.354323, -119.045974),
        DAY_COORD_LABEL: 'Bakersfield',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 283,
        DAY_HOURS: 4.5,
    },
    {
        DAY_DATE: date(2018,5,3),
        DAY_WAYPOINTS: [(34.066227, -118.090515), (33.377496, -112.369367)],
        DAY_COORD: coords.tucson,
        DAY_COORD_LABEL: 'Tucson',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 596,
        DAY_HOURS: 9,
        DAY_FRIENDS: {'Lisa and Bill': coords.tucson},
    },
    {
        DAY_DATE: date(2018,5,4),
        DAY_COORD: coords.tucson,
        DAY_FRIENDS: {'Lisa and Bill': coords.tucson},
        DAY_PARKS: ['Saguaro NP'],
    },
    {
        DAY_DATE: date(2018,5,5),
        DAY_COORD: coords.tucson,
        DAY_FRIENDS: {'Lisa and Bill': coords.tucson},
        DAY_MEALS: [('Tucson', "Bill's ribs", coords.tucson)],
        DAY_PIE: ('Shoo-fly', 'Lisa and Bill'),
    },
    {
        DAY_DATE: date(2018,5,6),
        DAY_WAYPOINTS: [(32.766242, -106.260910)],
        DAY_COORD: coords.abq,
        DAY_COORD_LABEL: 'Albuquerque',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 558,
        DAY_HOURS: 8.5,
        DAY_FRIENDS: {'Lisa and Bill': coords.tucson,
                      'Laura and Austin': coords.abq},
        DAY_PARKS: ['White Sands NM'],
    },
    {
        DAY_DATE: date(2018,5,7),
        DAY_COORD: coords.abq,
        DAY_FRIENDS: {'Laura and Austin': coords.abq},
        DAY_GOT_HIGH: [('Sandia Peak', 10678, (35.195697, -106.433777))],
        DAY_MEALS: [('Pueblo Harvest', 'Native American food', (35.110752, -106.658552))],
    },
    {
        DAY_DATE: date(2018,5,8),
        DAY_WAYPOINTS: [(34.599363, -105.129812)],
        DAY_COORD: (32.110461, -104.406751),
        DAY_COORD_LABEL: 'BLM campsite near Carlsbad',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 309,
        DAY_HOURS: 5,
        DAY_FRIENDS: {'Laura and Austin': coords.abq},
        DAY_PARKS: ['Carlsbad Caverns NP'],
        DAY_CAVES: ['Carlsbad Caverns NP'],
    },
    {
        DAY_DATE: date(2018,5,9),
        DAY_COORD: coords.farmersville,
        DAY_COORD_LABEL: 'Farmersville',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 528,
        DAY_HOURS: 9,
        DAY_FRIENDS: {'Jessica, Tommy, Conner, and Brady': coords.farmersville},
    },
    {
        DAY_DATE: date(2018,5,10),
        DAY_COORD: coords.farmersville,
        DAY_FRIENDS: {'Jessica, Tommy, Conner, and Brady': coords.farmersville,
                      'Tom, Lynda, Jennifer, and Andrew': (33.198427, -96.639490)},
        DAY_PIE: ('Strawberry basil', 'Jessica, Tommy, Conner, and Brady'),
    },
    {
        DAY_DATE: date(2018,5,11),
        DAY_COORD: coords.farmersville,
        DAY_FRIENDS: {'Jessica, Tommy, Conner, and Brady': coords.farmersville},
    },
    {
        DAY_DATE: date(2018,5,12),
        DAY_WAYPOINTS: [(32.551131, -95.858304)],
        DAY_COORD: coords.austin,
        DAY_COORD_LABEL: 'Austin',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 289,
        DAY_HOURS: 5,
        DAY_FRIENDS: {'Jessica, Tommy, Conner, and Brady': coords.farmersville,
                      'Amanda, Hunter, Hunter, and Jamie': coords.austin},
        DAY_MEALS: [("Torchy's Tacos", 'Tex-mex tacos', (30.222304, -97.840411))],
    },
    {
        DAY_DATE: date(2018,5,13),
        DAY_COORD: coords.austin,
        DAY_FRIENDS: {'Amanda, Hunter, Hunter, and Jamie': coords.austin},
        DAY_MEALS: [('Stiles Switch BBQ', 'Brisket and beef rib', (30.334569, -97.721526))],
    },
    {
        DAY_DATE: date(2018,5,14),
        DAY_COORD: coords.nola,
        DAY_COORD_LABEL: 'New Orleans',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 511,
        DAY_HOURS: 8,
        DAY_FRIENDS: {'Amanda, Hunter, Hunter, and Jamie': coords.austin,
                      'Alex, Tristan, and Heli': coords.nola},
        DAY_MEALS: [('The Joint', 'Pork ribs', (29.961301, -90.035574))],
    },
    {
        DAY_DATE: date(2018,5,15),
        DAY_COORD: coords.nola,
        DAY_FRIENDS: {'Alex, Tristan, and Heli': coords.nola},
    },
    {
        DAY_DATE: date(2018,5,16),
        DAY_COORD: coords.nola,
        DAY_FRIENDS: {'Alex, Tristan, and Heli': coords.nola},
        DAY_MEALS: [("Commander's Palace", 'Cheesecake', (29.928735, -90.084255))],
        DAY_TIKI: ("Beachbum Berry's Latitude 29", (29.953706, -90.065140)),
    },
    {
        DAY_DATE: date(2018,5,17),
        DAY_COORD: coords.nola,
        DAY_FRIENDS: {'Alex, Tristan, and Heli': coords.nola},
        DAY_MEALS: [("Elizabeth's", 'EVERYTHING', (29.961534, -90.041013))],
    },
    {
        DAY_DATE: date(2018,5,18),
        DAY_COORD: coords.nola,
        DAY_FRIENDS: {'Alex, Tristan, and Heli': coords.nola},
        DAY_PARKS: ['Pearl River WMA'],
        DAY_ANIMAL: ('Alligators', 'Pearl River WMA'),
        DAY_MEALS: [("Cajun Mike's", 'Crawfish', (30.374936, -89.745182))],
    },
    {
        DAY_DATE: date(2018,5,19),
        DAY_WAYPOINTS: [(30.305444, -89.741415), (30.453724, -88.896014), (30.716695, -88.056915), (30.731511, -85.291146), (30.248739, -82.687742)],
        DAY_COORD: coords.orlando,
        DAY_COORD_LABEL: 'Orlando',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 640,
        DAY_HOURS: 9,
        DAY_FRIENDS: {'Alex, Tristan, and Heli': coords.nola},
    },
    {
        DAY_DATE: date(2018,5,20),
        DAY_COORD: coords.orlando,
    },
    {
        DAY_DATE: date(2018,5,21),
        DAY_COORD: coords.orlando,
        DAY_TIKI: ("Trader Sam's Grog Grotto", (28.405814, -81.585497)),
    },
    {
        DAY_DATE: date(2018,5,22),
        DAY_WAYPOINTS: [(27.070162, -80.62702), (25.443468, -80.479716), (25.391608, -80.586881), (25.424487, -80.770536), (25.137725, -80.928198), (25.424487, -80.770536), (25.391608, -80.586881)],
        DAY_COORD: coords.florida_city,
        DAY_COORD_LABEL: 'Florida City',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 366,
        DAY_HOURS: 6,
        DAY_PARKS: ['Everglades NP'],
        DAY_ANIMAL: ('Alligators', 'Everglades NP'),
        DAY_GOT_HIGH: [('Mahogany Hammock', 4, (25.322842, -80.833305))],
    },
    {
        DAY_DATE: date(2018,5,23),
        DAY_WAYPOINTS: [(25.173695, -80.373892), (24.911993, -80.631323), (24.715279, -81.065005), (24.557282, -81.781100), (24.715279, -81.065005), (24.911993, -80.631323), (25.173695, -80.373892)],
        DAY_COORD: coords.florida_city,
        DAY_MILES: 252,
        DAY_HOURS: 6,
        DAY_MEALS: [("Kermit's", 'Key lime pie', (24.560187, -81.806275)),
                    ('Key West Key Lime Pie Company', 'Key lime pie', (24.559538, -81.804682)),
                    ('The Fish House', 'Key lime pie', (25.124260, -80.412978))],
    },
    {
        DAY_DATE: date(2018,5,24),
        DAY_WAYPOINTS: [(25.463643, -80.334882)],
        DAY_COORD: coords.florida_city,
        DAY_PARKS: ['Biscayne NP'],
        DAY_SWIM: ('Biscayne NP', (25.388416, -80.218740)),
        DAY_MEALS: [('Robert is Here Fruit Stand', 'Milkshakes', (25.447392, -80.501892))],
    },
    {
        DAY_DATE: date(2018,5,25),
        DAY_WAYPOINTS: [(26.887272, -80.096351), (30.690850, -81.794611)],
        DAY_COORD: coords.savannah,
        DAY_COORD_LABEL: 'Savannah',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 516,
        DAY_HOURS: 7.5,
    },
    {
        DAY_DATE: date(2018,5,26),
        DAY_COORD: coords.savannah,
        DAY_FRIENDS: {'Laurel and Andy': coords.savannah},
        DAY_MEALS: [("Zunzi's", 'South African sandwiches', (32.077387, -81.090854))],
    },
    {
        DAY_DATE: date(2018,5,27),
        DAY_WAYPOINTS: [(33.409995, -80.484196), (33.810267, -80.637199)],
        DAY_COORD: coords.congaree,
        DAY_COORD_LABEL: 'Congaree NP',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 148,
        DAY_HOURS: 2.5,
        DAY_PARKS: ['Congaree NP'],
    },
    {
        DAY_DATE: date(2018,5,28),
        DAY_COORD: coords.congaree,
        DAY_PARKS: ['Congaree NP'],
    },
    {
        DAY_DATE: date(2018,5,29),
        DAY_WAYPOINTS: [(33.997686, -81.152312)],
        DAY_COORD: coords.north_augusta,
        DAY_COORD_LABEL: 'North Augusta',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 88,
        DAY_HOURS: 1.5,
        DAY_FRIENDS: {'Laurel and Andy': coords.north_augusta},
    },
    {
        DAY_DATE: date(2018,5,30),
        DAY_COORD: coords.north_augusta,
        DAY_FRIENDS: {'Laurel and Andy': coords.north_augusta},
    },
    {
        DAY_DATE: date(2018,5,31),
        DAY_COORD: coords.north_augusta,
        DAY_FRIENDS: {'Laurel and Andy': coords.north_augusta},
        DAY_MEALS: [("Laurel and Andy's", 'Surf and Turf', coords.north_augusta)],
        DAY_PIE: ('Chocolate pecan', 'Laurel and Andy'),
    },
    {
        DAY_DATE: date(2018,6,1),
        DAY_COORD: coords.clemson,
        DAY_COORD_LABEL: 'Clemson',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 109,
        DAY_HOURS: 2.5,
        DAY_FRIENDS: {'Laurel and Andy': coords.north_augusta,
                      'Piper and Anwar': coords.clemson},
        DAY_SWIM: ('Lake Hartwell', (34.681392, -82.860668)),
        DAY_MEALS: [("Piper's", 'Thai soup', coords.clemson)],
        DAY_PIE: ('Strawberry basil', 'Piper and Anwar'),
    },
    {
        DAY_DATE: date(2018,6,2),
        DAY_COORD: coords.clemson,
        DAY_FRIENDS: {'Piper and Anwar': coords.clemson},
    },
    {
        DAY_DATE: date(2018,6,3),
        DAY_WAYPOINTS: [(33.883633, -84.393245)],
        DAY_COORD: coords.nashville,
        DAY_COORD_LABEL: 'Nashville',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 360,
        DAY_HOURS: 5.5,
        DAY_FRIENDS: {'Piper and Anwar': coords.clemson,
                      'Courtney': coords.nashville},
    },
    {
        DAY_DATE: date(2018,6,4),
        DAY_COORD: coords.nashville,
        DAY_FRIENDS: {'Courtney': coords.nashville},
        DAY_MEALS: [("Hattie B's", 'Fried chicken', (36.151459, -86.796612)),
                    ('Broadway Brewhouse', 'Bushwackers', (36.151092, -86.796816))],
        DAY_PIE: ('Buttermilk chess', 'Courtney'),
    },
    {
        DAY_DATE: date(2018,6,5),
        DAY_WAYPOINTS: [(37.005309, -86.378789), (37.097262, -86.050620)],
        DAY_COORD: (37.182846, -86.097319),
        DAY_COORD_LABEL: 'Mammoth Cave NP',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 95,
        DAY_HOURS: 1.5,
        DAY_FRIENDS: {'Courtney': coords.nashville},
        DAY_PARKS: ['Mammoth Cave NP'],
        DAY_CAVES: ['Mammoth Cave NP'],
    },
    {
        DAY_DATE: date(2018,6,6),
        DAY_WAYPOINTS: [(37.694630, -85.825145)],
        DAY_COORD: (38.040067, -84.503315),
        DAY_COORD_LABEL: 'Lexington',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 134,
        DAY_HOURS: 2.5,
        DAY_PARKS: ['Mammoth Cave NP'],
        DAY_CAVES: ['Mammoth Cave NP'],
    },
    {
        DAY_DATE: date(2018,6,7),
        DAY_WAYPOINTS: [(36.412401, -84.354628)],
        DAY_COORD: coords.smokies,
        DAY_COORD_LABEL: 'Smokies',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 241,
        DAY_HOURS: 4.25,
        DAY_PARKS: ['Great Smoky Mountains NP'],
        DAY_ANIMAL: ('Bear and bear cubs', 'Great Smoky Mountains NP'),
        DAY_GOT_HIGH: [("Clingman's Dome", 6643, (35.562761, -83.498481))],
        DAY_MEALS: [('Camp', 'Japanese noodles, tofu, asparagus, mushrooms, hot chili oil, ginger, soy sauce', coords.smokies)],
    },
    {
        DAY_DATE: date(2018,6,8),
        DAY_COORD: coords.smokies,
        DAY_PARKS: ['Great Smoky Mountains NP'],
        DAY_GOT_HIGH: [("Charlie's Bunion", 5564, (35.637334, -83.376645))],
    },
    {
        DAY_DATE: date(2018,6,9),
        DAY_WAYPOINTS: [(35.571276, -82.572326), (36.476052, -82.555409), (37.352349, -79.913128), (38.398393, -78.813557), (38.361570, -78.537517)],
        DAY_COORD: coords.shenandoah,
        DAY_COORD_LABEL: 'Shenandoah',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 427,
        DAY_HOURS: 7,
        DAY_PARKS: ['Shenandoah NP'],
    },
    {
        DAY_DATE: date(2018,6,10),
        DAY_WAYPOINTS: [(38.667338, -78.319074), (38.650482, -78.213130), (38.544839, -78.242732), (38.570363, -78.286417), (38.544839, -78.242732), (38.650482, -78.213130), (38.667338, -78.319074)],
        DAY_COORD: coords.shenandoah,
        DAY_MILES: 79,
        DAY_HOURS: 2.25,
        DAY_PARKS: ['Shenandoah NP'],
        DAY_GOT_HIGH: [('Old Rag', 3284, (38.551721, -78.315814))],
    },
    {
        DAY_DATE: date(2018,6,11),
        DAY_COORD: coords.dc,
        DAY_COORD_LABEL: 'DC',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 102,
        DAY_HOURS: 2.25,
        DAY_FRIENDS: {'Dani and Petra': coords.dc},
    },
    {
        DAY_DATE: date(2018,6,12),
        DAY_COORD: coords.dc,
        DAY_FRIENDS: {'Dani and Petra': coords.dc},
        DAY_PARKS: ['Lincoln Memorial', 'Korean War Veterans Memorial', 'Martin Luther King Jr Memorial', 'FDR Memorial', 'Thomas Jefferson Memorial', 'National Mall', 'Washington Monument'],
        DAY_TIKI: ('Archipelago', (38.917167, -77.028263)),
    },
    {
        DAY_DATE: date(2018,6,13),
        DAY_COORD: coords.dc,
        DAY_FRIENDS: {'Dani and Petra': coords.dc},
        DAY_PARKS: ['White House', 'World War II Memorial', 'Vietnam Veterans Memorial', 'National Mall'],
        DAY_GOT_HIGH: [('Old Post Office', 315, (38.893839, -77.027628))],
        DAY_MEALS: [('Bluejacket', 'Burgers and beers', (38.875084, -77.000776))],
    },
    {
        DAY_DATE: date(2018,6,14),
        DAY_COORD: coords.dc,
        DAY_FRIENDS: {'Dani and Petra': coords.dc,
                      'Nicole Waugh Ryan': (38.888308, -77.093287)},
    },
    {
        DAY_DATE: date(2018,6,15),
        DAY_NEW_LEG: True,
        DAY_COORD: coords.portland,
        DAY_COORD_LABEL: 'Portland',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland}, # and Reid, Laura and Austin, Jones, Sus, Olin, Georgia, Sarah and Cam, Jack and Emily
    },
    {
        DAY_DATE: date(2018,6,16),
        DAY_COORD: coords.portland,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland},
    },
    {
        DAY_DATE: date(2018,6,17),
        DAY_COORD: coords.portland,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland},
    },
    {
        DAY_DATE: date(2018,6,18),
        DAY_NEW_LEG: True,
        DAY_WAYPOINTS: [coords.dc, (39.453061, -76.406932), (39.663724, -75.933302), (39.689691, -75.607679), (39.669572, -75.465606)],
        DAY_COORD: coords.philly,
        DAY_COORD_LABEL: 'Philadelphia',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 161,
        DAY_HOURS: 3,
    },
    {
        DAY_DATE: date(2018,6,19),
        DAY_WAYPOINTS: [(39.951647, -75.163856)],
        DAY_COORD: coords.philly,
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_PARKS: ['Independence Hall NHP'],
        DAY_MEALS: [('Zahav', 'Cocktails and small plates', (39.946198, -75.145269))],
    },
    {
        DAY_DATE: date(2018,6,20),
        DAY_COORD: coords.nyc,
        DAY_COORD_LABEL: 'New York City',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 96,
        DAY_HOURS: 2,
        DAY_FRIENDS: {'Richard and Janice': coords.nyc},
        DAY_MEALS: [('Butter and Scotch', 'Pie, cake, and cocktails', (40.670106, -73.958413)),
                    ("Katz's Delicatessen", 'Pastrami sandwich', (40.722226, -73.987431))],
    },
    {
        DAY_DATE: date(2018,6,21),
        DAY_COORD: coords.nyc,
        DAY_FRIENDS: {'Richard and Janice': coords.nyc},
        DAY_GOT_HIGH: [('Empire State Building', 1250, (40.748416, -73.985661))],
        DAY_MEALS: [('Absolute Bagels', 'Bagels', (40.802516, -73.967452)),
                    ("John's of Times Square", 'Pizza', (40.758222, -73.988382))],
        DAY_PIE: ('Buttercrunch toffee', 'Richard and Janice'),
    },
    {
        DAY_DATE: date(2018,6,22),
        DAY_COORD: coords.nyc,
        DAY_FRIENDS: {'Richard and Janice': coords.nyc,
                      'Hanya and family': (40.779125, -73.962623)},
        DAY_MEALS: [('Cafe du Soleil', 'French food', (40.800096, -73.968394))],
    },
    {
        DAY_DATE: date(2018,6,23),
        DAY_WAYPOINTS: [(41.108643, -73.670943), (41.252613, -73.049129), (41.748156, -72.659509), (42.139693, -72.069508)],
        DAY_COORD: coords.boston,
        DAY_COORD_LABEL: 'Boston',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 216,
        DAY_HOURS: 4,
        DAY_FRIENDS: {'Richard and Janice': coords.nyc,
                      'Meliza and Nick': coords.boston},
    },
    {
        DAY_DATE: date(2018,6,24),
        DAY_COORD: coords.boston,
        DAY_FRIENDS: {'Meliza and Nick': coords.boston},
        DAY_PIE: ('Peanut butter caramel apple', 'Meliza and Nick'),
    },
    {
        DAY_DATE: date(2018,6,25),
        DAY_COORD: coords.boston,
        DAY_FRIENDS: {'Meliza and Nick': coords.boston},
        DAY_MEALS: [("Mike's Pastry", 'Cannoli', (42.364168, -71.054230)),
                    ("Modern Pastry", 'Cannoli', (42.363259, -71.054747)),
                    ("Maria's Pastry Shop", 'Cannoli', (42.363272, -71.056500))],
    },
    {
        DAY_DATE: date(2018,6,26),
        DAY_WAYPOINTS: [coords.providence],
        DAY_COORD: coords.wellesley,
        DAY_COORD_LABEL: 'Wellesley',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 95,
        DAY_HOURS: 2,
        DAY_FRIENDS: {'Meliza and Nick': coords.boston,
                      'Johnny': coords.wellesley,
                      'Jones': coords.providence},
        DAY_PIE: ('Mixed berry', 'Johnny'),
    },
    {
        DAY_DATE: date(2018,6,27),
        DAY_COORD: coords.wellesley,
        DAY_FRIENDS: {'Johnny': coords.wellesley},
        DAY_MEALS: [('Al Dente', 'Italian food', (42.364196, -71.055369))],
    },
    {
        DAY_DATE: date(2018,6,28),
        DAY_WAYPOINTS: [(42.995807, -70.832844), (44.842881, -69.418467)],
        DAY_COORD: (44.490835, -68.373582),
        DAY_COORD_LABEL: 'Acadia Gateway Motel',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 279,
        DAY_HOURS: 4.5,
        DAY_FRIENDS: {'Johnny': coords.wellesley},
        DAY_MEALS: [('Duckfat', 'Fries and blueberry shakes', (43.660239, -70.250404))],
    },
    {
        DAY_DATE: date(2018,6,29),
        DAY_COORD: coords.acadia,
        DAY_COORD_LABEL: 'Acadia NP',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 20,
        DAY_HOURS: 0.5,
        DAY_PARKS: ['Acadia NP'],
    },
    {
        DAY_DATE: date(2018,6,30),
        DAY_WAYPOINTS: [(44.263241, -68.396566), (44.341535, -68.401704), (44.401434, -68.338799), (44.380314, -68.231648), (44.360504, -68.188037), (44.297984, -68.211836), (44.320279, -68.252773), (44.376486, -68.242491), (44.359408, -68.335737)],
        DAY_COORD: coords.acadia,
        DAY_PARKS: ['Acadia NP'],
        DAY_GOT_HIGH: [('The Beehive', 520, (44.333394, -68.188361)),
                       ('Cadillac Mountain', 1530, (44.352562, -68.225097)),],
    },
    {
        DAY_DATE: date(2018,7,1),
        DAY_WAYPOINTS: [(44.793955, -68.629766), (44.833188, -69.421365), coords.gorham, (44.280194, -71.228995), coords.mt_washington, (44.280194, -71.228995), coords.gorham,],
        DAY_COORD: coords.milan_hill,
        DAY_COORD_LABEL: 'Milan Hill SP',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 225,
        DAY_HOURS: 5,
        DAY_PARKS: ['Acadia NP', 'White Mountain NF'],
        DAY_GOT_HIGH: [('Mt Washington', 6288, coords.mt_washington)],
    },
    {
        DAY_DATE: date(2018,7,2),
        DAY_WAYPOINTS: [coords.gorham, (44.240370, -71.679450), (44.146020, -71.687138), (44.240370, -71.679450), coords.gorham],
        DAY_COORD: coords.milan_hill,
        DAY_PARKS: ['White Mountain NF'],
        DAY_GOT_HIGH: [('Little Haystack Mountain', 4760, (44.140622, -71.644763)),
                       ('Mt Lincoln', 5089, (44.148894, -71.644515)),
                       ('Mt Lafayette', 5249, (44.160671, -71.644494))],
    },
    {
        DAY_DATE: date(2018,7,3),
        DAY_WAYPOINTS: [(44.626445, -71.540990), (44.469730, -71.588191), (44.236544, -72.550995)],
        DAY_COORD: coords.burlington,
        DAY_COORD_LABEL: 'Burlington',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 134,
        DAY_HOURS: 2.75,
        DAY_PARKS: ['White Mountain NF'],
        DAY_MEALS: [('The Blue Stone', 'Pizza', (44.337824, -72.755879)),
                    ("Ben and Jerry's Factory", 'Ice cream', (44.352807, -72.740285))],
    },
    {
        DAY_DATE: date(2018,7,4),
        DAY_COORD: coords.burlington,
    },
    {
        DAY_DATE: date(2018,7,5),
        DAY_COORD: coords.burlington,
    },
    {
        DAY_DATE: date(2018,7,6),
        DAY_WAYPOINTS: [(44.090105, -73.251618), (43.090299, -76.076303)],
        DAY_COORD: coords.ithaca,
        DAY_COORD_LABEL: 'Ithaca',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 281,
        DAY_HOURS: 5.5,
        DAY_FRIENDS: {'Collin': coords.ithaca},
        DAY_MEALS: [('Purity', 'Ice Cream', (42.444462, -76.508906))],
    },
    {
        DAY_DATE: date(2018,7,7),
        DAY_WAYPOINTS: [(42.948023, -76.874010), (43.093356, -79.055584), (42.853491, -78.816635), (42.736418, -78.834434), (42.127562, -80.084258), (41.483476, -81.681208), (41.311070, -82.650408), (41.658641, -83.695761)],
        DAY_COORD: coords.ann_arbor,
        DAY_COORD_LABEL: 'Ann Arbor',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 544,
        DAY_HOURS: 9,
        DAY_FRIENDS: {'Collin': coords.ithaca,
                      'Lee': (41.509373, -81.662294),
                      'Jeremy and Christine': coords.ann_arbor},
        DAY_PARKS: ['Niagara Falls SP'],
    },
    {
        DAY_DATE: date(2018,7,8),
        DAY_COORD: coords.ann_arbor,
        DAY_FRIENDS: {'Jeremy and Christine': coords.ann_arbor},
        DAY_SWIM: ('Huron River', coords.huron_river),
        DAY_MEALS: [('Blank Slate', 'Ice cream', (42.279710, -83.751276))],
    },
    {
        DAY_DATE: date(2018,7,9),
        DAY_WAYPOINTS: [coords.detroit],
        DAY_COORD: coords.ann_arbor,
        DAY_MILES: 86,
        DAY_HOURS: 1.5,
        DAY_FRIENDS: {'Jeremy and Christine': coords.ann_arbor,
                      'Larry': coords.detroit,},
        DAY_MEALS: [('Jolly Pumpkin', 'Pizza and beer', (42.351293, -83.065239)),
                    ('Frita Batidos', 'Burgers and milkshakes', (42.280344, -83.749452))],
    },
    {
        DAY_DATE: date(2018,7,10),
        DAY_COORD: coords.ann_arbor,
        DAY_FRIENDS: {'Jeremy and Christine': coords.ann_arbor},
        DAY_MEALS: [('', 'Bacon wrapped pork tenderloin + cantaloupe pico de gallo + mojitos', coords.ann_arbor)],
        DAY_PIE: ('Elvis pie *and* Apple cheddar', 'Jeremy and Christine'),
    },
    {
        DAY_DATE: date(2018,7,11),
        DAY_WAYPOINTS: [(42.152151, -86.298792), (41.698673, -86.851227), (41.606189, -87.254030), (41.638076, -87.501156)],
        DAY_COORD: coords.chicago,
        DAY_COORD_LABEL: 'Chicago',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 240,
        DAY_HOURS: 4,
        DAY_FRIENDS: {'Jeremy and Christine': coords.ann_arbor,
                      'Brenda': coords.chicago},
    },
    {
        DAY_DATE: date(2018,7,12),
        DAY_COORD: coords.chicago,
        DAY_FRIENDS: {'Brenda': coords.chicago},
        DAY_MEALS: [("Wolfy's ", 'Hot Dogs', (41.990723, -87.698579)),
                    ('The Art of Pizza', 'Deep dish pizza', (41.937142, -87.668097))],
        DAY_PIE: ('Irish Car Bomb', 'Brenda'),
        DAY_TIKI: ('Lost Lake', (41.932123, -87.707129)),
    },
    {
        DAY_DATE: date(2018,7,13),
        DAY_COORD: coords.chicago,
        DAY_FRIENDS: {'Brenda': coords.chicago},
        DAY_MEALS: [('Taste of Chicago food festival', 'Kim chi fries', (41.875727, -87.622655))],
        DAY_TIKI: ('Three Dots and a Dash', (41.890313, -87.630560)),
    },
    {
        DAY_DATE: date(2018,7,14),
        DAY_COORD: coords.chicago,
        DAY_FRIENDS: {'Brenda': coords.chicago},
        DAY_GOT_HIGH: [('Hancock Tower 96th Floor Signature Lounge', 1128, (41.898719, -87.622903))],
        DAY_SWIM: ('Lake Michigan', (41.978315, -87.648103)),
    },
    {
        DAY_DATE: date(2018,7,15),
        DAY_WAYPOINTS: [(43.000986, -87.988302), (43.106143, -89.321141), (44.814305, -91.447220)],
        DAY_COORD: coords.minneapolis,
        DAY_COORD_LABEL: 'Minneapolis',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 425,
        DAY_HOURS: 6.5,
        DAY_FRIENDS: {'Brenda': coords.chicago,
                      'Laurie': (43.095183, -89.510684),
                      'Vic and Ari': coords.minneapolis},
    },
    {
        DAY_DATE: date(2018,7,16),
        DAY_COORD: coords.minneapolis,
        DAY_FRIENDS: {'Vic and Ari': coords.minneapolis,
                      'Caleb and Amber': (44.985084, -93.383359)},
        DAY_TIKI: ("Psycho Suzi's Motor Lounge", (45.007461, -93.272400)),
    },
    {
        DAY_DATE: date(2018,7,17),
        DAY_COORD: coords.minneapolis,
        DAY_FRIENDS: {'Vic and Ari': coords.minneapolis,},
        # TODO 7/17 to 7/19 Mom and Dad, Julia Cachi Alex, Anita, Louise and David, Christopher, Flo
        DAY_MEALS: [("Vic and Ari's", "Homemade Indonesian Feast", coords.minneapolis)],
        DAY_PIE: ('Lemon cream pie *and* Bourbon ginger pecan', 'Vic and Ari'),
    },
    {
        DAY_DATE: date(2018,7,18),
        DAY_COORD: coords.minneapolis,
        DAY_FRIENDS: {'Vic and Ari': coords.minneapolis,},
    },
    {
        DAY_DATE: date(2018,7,19),
        DAY_NEW_LEG: True,
        DAY_COORD: coords.sf,
        DAY_COORD_LABEL: 'San Francisco',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_FRIENDS: {'Vic and Ari': coords.minneapolis,
                      'Nina and Alex': coords.sf},
        # TODO Derek and Audrey, and the rest of Banduh
    },
    {
        DAY_DATE: date(2018,7,20),
        DAY_COORD: coords.sf,
        DAY_FRIENDS: {'Nina and Alex': coords.sf},
    },
    {
        DAY_DATE: date(2018,7,21),
        DAY_COORD: coords.sf,
        DAY_FRIENDS: {'Nina and Alex': coords.sf},
        DAY_MEALS: [('Wedding reception', 'Mac and cheese', coords.conservatory_of_flowers)],
    },
    {
        DAY_DATE: date(2018,7,22),
        DAY_COORD: coords.fairfield_murray,
        DAY_COORD_LABEL: 'Fairfield',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 47,
        DAY_HOURS: 1,
        DAY_FRIENDS: {'Nina and Alex': coords.sf,
                      'Julie and Patsy': coords.fairfield_julie,
                      'Murray': coords.fairfield_murray},
    },
    {
        DAY_DATE: date(2018,7,23),
        DAY_COORD: coords.davis,
        DAY_COORD_LABEL: 'Davis',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 30,
        DAY_HOURS: 0.5,
        DAY_FRIENDS: {'Eric, Crissy, Adara, and Nash': coords.davis},
    },
    {
        DAY_DATE: date(2018,7,24),
        DAY_WAYPOINTS: [(40.461333, -122.279960)],
        DAY_COORD: coords.lassen,
        DAY_COORD_LABEL: 'Lassen',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 189,
        DAY_HOURS: 3.25,
        DAY_FRIENDS: {'Eric, Crissy, Adara, and Nash': coords.davis},
        DAY_PARKS: ['Lassen Volcanic NP'],
    },
    {
        DAY_DATE: date(2018,7,25),
        DAY_COORD: coords.lassen,
        DAY_PARKS: ['Lassen Volcanic NP'],
        DAY_ANIMAL: ('Bear', 'Lassen Volcanic NP'),
        DAY_SWIM: ('Ridge Lakes', (40.456450, -121.549242)),
    },
    {
        DAY_DATE: date(2018,7,26),
        DAY_WAYPOINTS: [(40.936430, -121.633770), (41.131893, -121.131687), (41.718455, -121.502742)],
        DAY_COORD: coords.lava_beds,
        DAY_COORD_LABEL: 'Indian Wells Campground',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 151,
        DAY_HOURS: 3,
        DAY_PARKS: ['Lassen Volcanic NP', 'McArthur-Burney Falls Memorial SP', 'Lava Beds NM'],
        DAY_ANIMAL: ('Nesting black swifts', 'McArthur-Burney Falls Memorial SP'),
    },
    {
        DAY_DATE: date(2018,7,27),
        DAY_COORD: coords.lava_beds,
        DAY_PARKS: ['Lava Beds NM'],
        DAY_MEALS: [('Camp', 'Avocado toast', coords.lava_beds)],
        DAY_CAVES: ['Lava Beds NM'],
    },
    {
        DAY_DATE: date(2018,7,28),
        DAY_WAYPOINTS: [(43.331515, -121.757079), (44.022525, -123.072701)],
        DAY_COORD: coords.portland,
        DAY_COORD_LABEL: 'Portland',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 326,
        DAY_HOURS: 5.75,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland},
        DAY_PARKS: ['Lava Beds NM'],
        DAY_MEALS: [('Rimsky Korsakoffee House', 'Dessert', (45.517756, -122.653950))],
    },
    {
        DAY_DATE: date(2018,7,29),
        DAY_WAYPOINTS: [(45.546819, -122.192536), (45.659529, -121.892091)],
        DAY_COORD: coords.skamania,
        DAY_COORD_LABEL: 'Skamania Lodge',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 45,
        DAY_HOURS: 1,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland,
                      'Mike and Kristine, the Alberti family, Pablo, Jake and Adam, Eric Tooley':  coords.skamania},
    },
    {
        DAY_DATE: date(2018,7,30),
        DAY_WAYPOINTS: [(45.567066, -122.249156), (45.628728, -122.543154), (46.462882, -122.884106), (46.801470, -123.010680), (46.841962, -123.247997), (47.011573, -123.386740), (46.970430, -123.617987), (47.225335, -123.983034)],
        DAY_COORD: coords.quinault,
        DAY_COORD_LABEL: 'Quinault Rainforest',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 213,
        DAY_HOURS: 3.75,
        DAY_FRIENDS: {'Mike and Kristine, the Alberti family, Pablo, Jake and Adam, Eric Tooley':  coords.skamania},
        DAY_PARKS: ['Olympic NP'],
    },
    {
        DAY_DATE: date(2018,7,31),
        DAY_WAYPOINTS: [(47.515110, -124.336348), (47.710838, -124.414812), (47.515110, -124.336348)],
        DAY_COORD: coords.quinault,
        DAY_MILES: 80,
        DAY_HOURS: 1.5,
        DAY_PARKS: ['Olympic NP'],
    },
    {
        DAY_DATE: date(2018,8,1),
        DAY_WAYPOINTS: [(47.501910, -123.781564), (47.526326, -123.765148), (47.531591, -123.677405), (47.536856, -123.678365), (47.535717, -123.761219), (47.469342, -123.923109), (47.457686, -123.904730), (47.454964, -123.866874)],
        DAY_COORD: coords.quinault,
        DAY_MILES: 30,
        DAY_HOURS: 1,
        DAY_PARKS: ['Olympic NP'],
    },
    {
        DAY_DATE: date(2018,8,2),
        DAY_WAYPOINTS: [(47.515110, -124.336348), (47.710838, -124.414812), (47.797220, -124.239542), (47.941896, -124.411954), (48.057364, -124.376610), (48.043201, -123.828420), (48.105127, -123.412771), (48.006840, -123.360408), coords.hurricane_ridge, (48.006840, -123.360408), (48.105127, -123.412771), (47.986439, -122.848921), coords.port_townsend, (47.986439, -122.848921), (47.850701, -122.606458), (47.595711, -122.725563), (47.237523, -122.538190), (47.278138, -122.285465), (47.798126, -122.341378), (48.018115, -122.147663), (48.187589, -122.201805), (48.281306, -121.998726), (48.255384, -121.601282), (48.494241, -121.598667), coords.newhalem],
        DAY_COORD: (48.685241, -121.093832),
        DAY_COORD_LABEL: 'North Cascades NP, campsite 1',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 444,
        DAY_HOURS: 9.25,
        DAY_PARKS: ['Olympic NP', 'North Cascades NP'],
        DAY_GOT_HIGH: [('Hurricane Ridge', 5242, coords.hurricane_ridge)],
    },
    {
        DAY_DATE: date(2018,8,3),
        DAY_WAYPOINTS: [(48.708857, -120.909971), (48.497666, -120.712124), (48.522956, -120.654695), (48.497666, -120.712124), (48.708857, -120.909971)],
        DAY_COORD: (48.685325, -121.094081),
        DAY_COORD_LABEL: 'North Cascades NP, campsite 2',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 64,
        DAY_HOURS: 1.5,
        DAY_PARKS: ['North Cascades NP'],
    },
    {
        DAY_DATE: date(2018,8,4),
        DAY_COORD: coords.newhalem,
        DAY_COORD_LABEL: 'North Cascades NP, campsite 3',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_PARKS: ['North Cascades NP'],
        DAY_GOT_HIGH: [('Fourth of July Pass', 3600, (48.658376, -121.034882))],
    },
    {
        DAY_DATE: date(2018,8,5),
        DAY_WAYPOINTS: [(48.494241, -121.598667), (48.255384, -121.601282), (48.281306, -121.998726), (48.187589, -122.201805), (48.018115, -122.147663), (47.798126, -122.341378), (47.480246, -122.196483), (47.450687, -122.089147), (47.157388, -121.902354), (47.148104, -121.626041), (46.867036, -121.540273)],
        DAY_COORD: coords.ohanapecosh,
        DAY_COORD_LABEL: 'Mount Rainier',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 215,
        DAY_HOURS: 4.5,
        DAY_PARKS: ['North Cascades NP', 'Mount Rainier NP'],
    },
    {
        DAY_DATE: date(2018,8,6),
        DAY_WAYPOINTS: [(46.867036, -121.540273), (46.913624, -121.643769), (46.867036, -121.540273)],
        DAY_COORD: coords.ohanapecosh,
        DAY_MILES: 64,
        DAY_HOURS: 2,
        DAY_PARKS: ['Mount Rainier NP'],
        DAY_GOT_HIGH: [('Skyscraper Mountain', 7077, (46.926992, -121.697596))],
        DAY_SWIM: ('Ohanapecosh River', coords.ohanapecosh),
        DAY_MEALS: [('Camp', 'Breakfast sandwiches', coords.ohanapecosh)],
    },
    {
        DAY_DATE: date(2018,8,7),
        DAY_WAYPOINTS: [(46.782962, -121.732846)],
        DAY_COORD: coords.ohanapecosh,
        DAY_MILES: 47,
        DAY_HOURS: 1.5,
        DAY_PARKS: ['Mount Rainier NP'],
        DAY_ANIMAL: ('Mountain goats', 'Mount Rainier NP'),
        DAY_GOT_HIGH: [('Panorama Point', 6800, (46.803712, -121.729529))],
        DAY_SWIM: ('Ohanapecosh River', coords.ohanapecosh),
        DAY_MEALS: [('Camp', 'BBQ tri-tip', coords.ohanapecosh)],
    },
    {
        DAY_DATE: date(2018,8,8),
        DAY_WAYPOINTS: [(46.523201, -121.754401), (46.462882, -122.884106)],
        DAY_COORD: coords.portland,
        DAY_COORD_LABEL: 'Portland',
        DAY_COORD_TYPE: DAY_COORD_CITY,
        DAY_MILES: 149,
        DAY_HOURS: 2.5,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland},
        DAY_PARKS: ['Mount Rainier NP'],
        DAY_MEALS: [('Salt and Straw', 'Ice cream', (45.504927, -122.630573))],
    },
    {
        DAY_DATE: date(2018,8,9),
        DAY_COORD: coords.portland,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland}, # TODO Arbel, Emilie, Jack
    },
    {
        DAY_DATE: date(2018,8,10),
        DAY_COORD: coords.portland,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland}, # TODO and Arbel
        DAY_MEALS: [('Salt and Straw', 'Ice cream', (45.528948, -122.698347))],
        DAY_TIKI: ('Hale Pele', (45.535275, -122.637375)),
    },
    {
        DAY_DATE: date(2018,8,11),
        DAY_WAYPOINTS: [(45.028504, -123.054898), (44.005448, -123.055546), (43.338792, -121.724381), (43.070174, -121.825557), (43.085168, -122.310228)],
        DAY_COORD: (42.683875, -122.619410),
        DAY_COORD_LABEL: 'Joseph H. Stewart State Recreation Area',
        DAY_COORD_TYPE: DAY_COORD_CAMPING,
        DAY_MILES: 282,
        DAY_HOURS: 5,
        DAY_FRIENDS: {'Derek and Marisa': coords.portland},
        DAY_PARKS: ['Crater Lake NP'],
    },
    #{
    #    DAY_DATE: date(2018,8,12),
    #    DAY_WAYPOINTS: [(42.427422, -123.016272), (42.378325, -123.549362), (41.901672, -123.742137), (41.762919, -124.162003), (41.689682, -124.112054), (41.513459, -124.033486), (41.363648, -123.993994), (41.278970, -124.084364), (41.167314, -124.100286)],
    #    DAY_COORD: coords.patricks_point,
    #    DAY_COORD_LABEL: "Patrick's Point SP",
    #    DAY_COORD_TYPE: DAY_COORD_CAMPING,
    #    DAY_MILES: 189,
    #    DAY_HOURS: 4,
    #    DAY_PARKS: ['Jedediah Smith SP', "Patrick's Point SP"],
    #},
    #{
    #    DAY_DATE: date(2018,8,13),
    #    DAY_COORD: coords.patricks_point,
    #    DAY_MILES: 108,
    #    DAY_HOURS: 2.75,
    #    DAY_PARKS: ["Patrick's Point SP", 'Prairie Creek SP'],
    #    DAY_ANIMAL: ('Elk', 'Prairie Creek SP'),
    #},
    #{
    #    DAY_DATE: date(2018,8,14),
    #    DAY_WAYPOINTS: [(41.064452, -124.140061), (41.018133, -124.104305), (40.924984, -124.117554)],
    #    DAY_COORD: coords.arcata,
    #    DAY_COORD_LABEL: 'Arcata',
    #    DAY_COORD_TYPE: DAY_COORD_CITY,
    #    DAY_MILES: 22,
    #    DAY_HOURS: 0.5,
    #    DAY_FRIENDS: {'Ann Tan': coords.arcata},
    #    DAY_PARKS: ["Patrick's Point SP"],
    #},
    #{
    #    DAY_DATE: date(2018,8,15),
    #    DAY_COORD: coords.arcata,
    #    DAY_FRIENDS: {'Ann Tan': coords.arcata},
    #},
]

'''
    {
        DAY_DATE: date(2018,8,),
        DAY_NEW_LEG: True,
        DAY_WAYPOINTS: [(0,0)],
        DAY_COORD: (0, 0),
        DAY_COORD_LABEL: 'Tucson',
        DAY_COORD_TYPE: DAY_COORD_CITY | DAY_COORD_CAMPING,
        DAY_MILES: 0,
        DAY_HOURS: 0,
        DAY_FRIENDS: {'Lisa and Bill': (0,0)},
        DAY_PARKS: ['Saguaro NP'], # don't forget to add to parks dict
        DAY_ANIMAL: ('Bear', 'Lassen Volcanic NP'),
        DAY_GOT_HIGH: [('Empire State Building', 1000, (0,0))],
        DAY_SWIM: ('Huron River', (0,0)),
        DAY_MEALS: [('Tucson', 'Bills ribs', (0,0))],
        DAY_PIE: ('Shoo-fly pie', 'Lisa and Bill'),
        DAY_TIKI: ('Smugglers Cove', (0,0)),
        DAY_CAVES: ['Lava Beds NM'],
    },
'''
