import requests
from area import area
import json

def find_geo(plz, city, street, house_number) -> dict:

    print("Find geo called")

    data = None

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

    try:
        with open('cache.json', 'r') as f:
            cache = json.load(f)  # Use json.load to read the file contents
    except FileNotFoundError:
        cache = {}  # Initialize an empty cache if the file doesn't exist

    # Create the key for the current query
    cache_key = f'{plz}{city}{street}{house_number}'

    if cache_key in cache:

        print("USING CACHED DATA")
        # Use the cached data
        data = cache[cache_key]
    else:
        print("Making request to overpass api")
        # Make the request and update the cache
        data = requests.get(url, params={'data': query}).json()
        print(f"Data {data}")
        # Update the cache and save it back to the file
        cache[cache_key] = data
        with open('cache.json', 'w') as f:
            json.dump(cache, f, indent=4)

    # Initialize the geo dictionary with default values
    geo = {
        'squaremeters': 0,
        'outline': None,
    }

    print(f"DATA {data}")

    outline = data['elements'][1:]
    print(f"OUTLINE {outline}")
    lat_lon_list = [[item['lat'], item['lon']] for item in outline if 'lat' in item and 'lon' in item]

    obj = {'type':'Polygon','coordinates':[lat_lon_list]}
    roofarea = area(obj)

    geo['squaremeters'] = roofarea
    geo['outline'] = lat_lon_list

    geo['longitude'] = lat_lon_list[0][1]

    geo['latitude'] = lat_lon_list[0][0]
    print(f"GEO {geo}")

    return geo
