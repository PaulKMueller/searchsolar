import requests
from area import area
import json

def find_geo(plz, city, street, house_number) -> dict:

    print("Find geo called")

    data = None

    url = f"""https://maps.googleapis.com/maps/api/geocode/json?address={plz}+{city}+{street}+{house_number}&extra_computations=BUILDING_AND_ENTRANCES&key=AIzaSyAJV8oKU2pWmPcebjSiUERaxEOlHeDMzaI"""

    data = requests.get(url).json()
    outline3 = data['results'][0]['buildings'][0]['building_outlines'][0]['display_polygon']['coordinates'][0]
    outline2 = [[coord[1], coord[0]] for coord in outline3]

    # Initialize the geo dictionary with default values
    geo = {
        'squaremeters': 0,
        'outline': None,
    }

    obj = {'type':'Polygon','coordinates':[outline2]}
    roofarea = area(obj)

    geo['squaremeters'] = roofarea
    geo['outline'] = outline2

    geo['longitude'] = outline2[0][1]

    geo['latitude'] = outline2[0][0]

    return geo
