import requests

def find_geo(plz, city, street, house_number):
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["addr:postcode"="{plz}"]["addr:city"="{city}"]["addr:street"="{street}"]["addr:housenumber"="{house_number}"];
    out center;
    """
    response = requests.get(url, params={'data': query})
    data = response.json()

    # Initialize the geo dictionary with default values
    geo = {
        'squaremeters': 100,
        'latitude': None,
        'longitude': None
    }

    # Check for elements in the response
    if 'elements' in data and data['elements']:
        element = data['elements'][0]
        geo['latitude'] = element['lat']
        geo['longitude'] = element['lon']

    return geo
