import requests

def find_geo(plz, city, street, house_number):
    # Basic Overpass API call to get building information
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["addr:postcode"="{plz}"]["addr:city"="{city}"]["addr:street"="{street}"]["addr:housenumber"="{house_number}"];
    out center;
    """
    response = requests.get(url, params={'data': query})
    data = response.json()

    geo = dict()
    if 'elements' in data and data['elements']:
        element = data['elements'][0]
        geo['squaremeters'] = 100 
        geo['latitude'] = element['lat']
        geo['longitude'] = element['lon']
    else:
        geo['latitude'], geo['longitude'] = None, None

    return geo
