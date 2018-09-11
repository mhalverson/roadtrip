# The main export of this module is the "parks" dict.

import json

park_data = {
    # For national parks and national monuments, specify the four-letter
    # abbreviation and the program will attempt to look it up in the
    # nationalparkservice data repository
    # (https://github.com/nationalparkservice/data).
    #
    # Otherwise, just specify the GeoJson data inline.
    'Saguaro NP': 'sagu',
    'White Sands NM': 'whsa',
    'Carlsbad Caverns NP': 'cave',
    'Pearl River WMA': { # TODO find the actual coordinates
        'type': 'Polygon',
        'coordinates': [[[-89.874454, 30.654826], [-89.637247, 30.165645], [-89.584897, 30.186527], [-89.802218, 30.664677], [-89.874454, 30.654826]]],
    },
    'Everglades NP': 'ever',
    'Biscayne NP': 'bisc',
    'Congaree NP': 'cong',
    'Mammoth Cave NP': 'maca',
    'Great Smoky Mountains NP': 'grsm',
    'Shenandoah NP': 'shen',
    'Lincoln Memorial': 'linc',
    'Korean War Veterans Memorial': 'kowa',
    'Martin Luther King Jr Memorial': 'mlkm',
    'FDR Memorial': 'frde',
    'Thomas Jefferson Memorial': 'jefm',
    'National Mall': 'mall',
    'Washington Monument': 'wamo',
    'White House': 'whho',
    'World War II Memorial': 'wwii',
    'Vietnam Veterans Memorial': 'vive',
    'Independence Hall NHP': 'inde',
    'Acadia NP': 'acad',
    'White Mountain NF' : { # TODO find the actual coordinates
        'type': 'MultiPolygon',
        'coordinates': [[
            [[-71.500434, 44.609651], [-71.463335, 44.4102], [-71.268277, 44.389532], [-71.215473, 44.484534], [-71.316292, 44.609905], [-71.500434, 44.609651]],
            [[-71.444706, 44.366346], [-71.920069, 44.139882], [-71.954988, 43.92721], [-71.838359, 43.797644], [-71.468333, 43.833549], [-71.126165, 43.998153], [-70.773962, 44.23821], [-70.783941, 44.342397], [-70.89789, 44.406709], [-71.444706, 44.366346]],
        ]],
    },
    'Niagara Falls SP': { # TODO find the actual coordinates
        'type': 'Polygon',
        'coordinates': [[[-79.062836, 43.095095], [-79.075203, 43.080161], [-79.066207, 43.077104], [-79.050378, 43.079702], [-79.051901, 43.082363], [-79.061175, 43.094785], [-79.062836, 43.095095]]],
    },
    'Lassen Volcanic NP': 'lavo',
    'McArthur-Burney Falls Memorial SP': { # TODO find the actual coordinates
        'type': 'Polygon',
        'coordinates': [[[-121.659265, 41.029214], [-121.659265, 41.017494], [-121.657896, 41.017494], [-121.657896, 41.00803], [-121.650417, 41.00803], [-121.650417, 41.004942], [-121.639275, 41.004942], [-121.639275, 41.015551], [-121.643722, 41.015551], [-121.622792, 41.016617], [-121.659265, 41.029214]]],
    },
    'Lava Beds NM': 'labe',
    'Olympic NP': 'olym',
    'North Cascades NP': 'noca',
    'Mount Rainier NP': 'mora',
    'Crater Lake NP': 'crla',
    'Jedediah Smith SP': { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
    'Prairie Creek SP': { # TODO find the actual coordinates
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]
],
    },
    "Patricks Point SP": { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
    'Isle Royale NP': 'isro',
    'Boundary Waters Canoe Wilderness Area': { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
    'Badlands NP': 'badl',
    'Mount Rushmore NM': 'moru',
    'Custer SP': { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
    'Wind Cave NP': 'wica',
    'Jewel Cave NM': 'jeca',
    "Devil's Tower NM": 'deto',
    'Banff NP': { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
    'Jasper NP': { # TODO find the actual coordinates... this is prairie creek
        'type': 'Polygon',
        'coordinates': [[(-124.046819, 41.415622), (-124.016537, 41.416374), (-124.008453, 41.384539), (-124.04632, 41.384742), (-124.046819, 41.415622)]],
    },
}

parks = {}
for p, data in park_data.iteritems():
    # coerce to shapely geometries from https://medium.com/@pramukta/recipe-importing-geojson-into-shapely-da1edf79f41d
    if isinstance(data, str):
        with open('../data/base_data/boundaries/parks/{}.geojson'.format(data)) as f:
            geom = json.load(f)["geometry"]
    else:
        geom = data
    parks[p] = geom
