import requests
from area import area

def find_geo(plz, city, street, house_number) -> dict:
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
        [out:json];
        (
        node["building"]["addr:postcode"="{plz}"]["addr:street"="{street}"]["addr:housenumber"="{house_number}"]["addr:city"="{city}"];
        way["building"]["addr:postcode"="{plz}"]["addr:street"="{street}"]["addr:housenumber"="{house_number}"]["addr:city"="{city}"];
        relation["building"]["addr:postcode"="{plz}"]["addr:street"="{street}"]["addr:housenumber"="{house_number}"]["addr:city"="{city}"];
        );
        out body;
        >>;
        out skel;
    """
    response = requests.get(url, params={'data': query})
    data = response.json()

    print(data)

    # Initialize the geo dictionary with default values
    geo = {
        'squaremeters': 0,
        'outline': None,
    }

    outline = data['elements'][1:]
    lat_lon_list = [[item['lat'], item['lon']] for item in outline]

    obj = {'type':'Polygon','coordinates':[lat_lon_list]}
    roofarea = area(obj)

    geo['squaremeters'] = roofarea
    geo['outline'] = lat_lon_list

    return geo
