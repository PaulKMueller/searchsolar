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

    if plz == "76137" and city == "Karlsruhe" and street == "Morgenstraße" and house_number == "5":
        data = {'version': 0.6, 'generator': 'Overpass API 0.7.62.1 084b4234', 'osm3s': {'timestamp_osm_base': '2024-10-25T17:43:41Z', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'}, 'elements': [{'type': 'way', 'id': 97892155, 'nodes': [1133026383, 1133026015, 1133026344, 4301480944, 4301480945, 4301480939, 4301480938, 1133026215, 1133025932, 1133026383], 'tags': {'addr:city': 'Karlsruhe', 'addr:country': 'DE', 'addr:housenumber': '5', 'addr:postcode': '76137', 'addr:street': 'Morgenstraße', 'building': 'apartments', 'building:levels': '4', 'roof:levels': '2', 'roof:shape': 'gabled', 'source': 'LA-KA'}}, {'type': 'node', 'id': 1133025932, 'lat': 49.0024739, 'lon': 8.4133456}, {'type': 'node', 'id': 1133026015, 'lat': 49.0026068, 'lon': 8.4132066}, {'type': 'node', 'id': 1133026215, 'lat': 49.0024745, 'lon': 8.4133731}, {'type': 'node', 'id': 1133026344, 'lat': 49.0026102, 'lon': 8.4133644}, {'type': 'node', 'id': 1133026383, 'lat': 49.0024711, 'lon': 8.4132132}, {'type': 'node', 'id': 4301480938, 'lat': 49.0025218, 'lon': 8.4133708}, {'type': 'node', 'id': 4301480939, 'lat': 49.0025222, 'lon': 8.4133907}, {'type': 'node', 'id': 4301480944, 'lat': 49.0025592, 'lon': 8.4133669}, {'type': 'node', 'id': 4301480945, 'lat': 49.0025597, 'lon': 8.4133889}]}
    else:
        response = requests.get(url, params={'data': query})
        data = response.json()

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
    print(f"Lat lon list: {lat_lon_list}")

    geo['longitude'] = lat_lon_list[0][1]

    print(f"Longitude: {geo['longitude']}")

    geo['latitude'] = lat_lon_list[0][0]
    print(f"Latitude: {geo['latitude']}")

    return geo
