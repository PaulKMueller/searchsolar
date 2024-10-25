from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd

# Example DataFrame of annual sunshine hours
csv_file_path = 'places_and_hours.csv'

# Read the CSV file into a DataFrame
df_sunshine = pd.read_csv(csv_file_path)

# Comprehensive list of major German cities with their coordinates
# Comprehensive list of major German cities with their coordinates
major_cities = [
    {'name': 'Berlin', 'latitude': 52.5200, 'longitude': 13.4050},
    {'name': 'Hamburg', 'latitude': 53.5511, 'longitude': 9.9937},
    {'name': 'Munich', 'latitude': 48.1351, 'longitude': 11.5820},
    {'name': 'Cologne', 'latitude': 50.9375, 'longitude': 6.9603},
    {'name': 'Frankfurt am Main', 'latitude': 50.1109, 'longitude': 8.6821},
    {'name': 'Stuttgart', 'latitude': 48.7758, 'longitude': 9.1829},
    {'name': 'Düsseldorf', 'latitude': 51.2277, 'longitude': 6.7735},
    {'name': 'Dortmund', 'latitude': 51.5136, 'longitude': 7.4653},
    {'name': 'Essen', 'latitude': 51.4556, 'longitude': 7.0116},
    {'name': 'Leipzig', 'latitude': 51.3397, 'longitude': 12.3731},
    {'name': 'Bremen', 'latitude': 53.0793, 'longitude': 8.8017},
    {'name': 'Dresden', 'latitude': 51.0504, 'longitude': 13.7373},
    {'name': 'Hanover', 'latitude': 52.3759, 'longitude': 9.7320},
    {'name': 'Nuremberg', 'latitude': 49.4521, 'longitude': 11.0767},
    {'name': 'Duisburg', 'latitude': 51.4344, 'longitude': 6.7623},
    {'name': 'Bochum', 'latitude': 51.4818, 'longitude': 7.2162},
    {'name': 'Wuppertal', 'latitude': 51.2562, 'longitude': 7.1508},
    {'name': 'Bielefeld', 'latitude': 52.0302, 'longitude': 8.5325},
    {'name': 'Bonn', 'latitude': 50.7374, 'longitude': 7.0982},
    {'name': 'Münster', 'latitude': 51.9607, 'longitude': 7.6261},
    {'name': 'Karlsruhe', 'latitude': 49.0069, 'longitude': 8.4037},
    {'name': 'Mannheim', 'latitude': 49.4875, 'longitude': 8.4660},
    {'name': 'Augsburg', 'latitude': 48.3705, 'longitude': 10.8978},
    {'name': 'Wiesbaden', 'latitude': 50.0826, 'longitude': 8.2417},
    {'name': 'Gelsenkirchen', 'latitude': 51.5177, 'longitude': 7.0857},
    {'name': 'Mönchengladbach', 'latitude': 51.1805, 'longitude': 6.4428},
    {'name': 'Braunschweig', 'latitude': 52.2689, 'longitude': 10.5268},
    {'name': 'Chemnitz', 'latitude': 50.8278, 'longitude': 12.9214},
    {'name': 'Kiel', 'latitude': 54.3233, 'longitude': 10.1228},
    {'name': 'Aachen', 'latitude': 50.7753, 'longitude': 6.0839},
    {'name': 'Halle (Saale)', 'latitude': 51.4828, 'longitude': 11.9690},
    {'name': 'Magdeburg', 'latitude': 52.1205, 'longitude': 11.6276},
    {'name': 'Freiburg im Breisgau', 'latitude': 47.9990, 'longitude': 7.8421},
    {'name': 'Krefeld', 'latitude': 51.3388, 'longitude': 6.5853},
    {'name': 'Lübeck', 'latitude': 53.8655, 'longitude': 10.6866},
    {'name': 'Oberhausen', 'latitude': 51.4963, 'longitude': 6.8638},
    {'name': 'Erfurt', 'latitude': 50.9848, 'longitude': 11.0299},
    {'name': 'Mainz', 'latitude': 49.9929, 'longitude': 8.2473},
    {'name': 'Rostock', 'latitude': 54.0924, 'longitude': 12.0991},
    {'name': 'Kassel', 'latitude': 51.3127, 'longitude': 9.4797},
    {'name': 'Hagen', 'latitude': 51.3671, 'longitude': 7.4633},
    {'name': 'Hamm', 'latitude': 51.6739, 'longitude': 7.8150},
    {'name': 'Saarbrücken', 'latitude': 49.2400, 'longitude': 6.9969},
    {'name': 'Mülheim an der Ruhr', 'latitude': 51.4325, 'longitude': 6.8797},
    {'name': 'Potsdam', 'latitude': 52.3906, 'longitude': 13.0645},
    {'name': 'Ludwigshafen', 'latitude': 49.4774, 'longitude': 8.4452},
    {'name': 'Oldenburg', 'latitude': 53.1435, 'longitude': 8.2146},
    {'name': 'Leverkusen', 'latitude': 51.0459, 'longitude': 7.0192},
    {'name': 'Osnabrück', 'latitude': 52.2799, 'longitude': 8.0472},
    {'name': 'Solingen', 'latitude': 51.1652, 'longitude': 7.0671},
    {'name': 'Heidelberg', 'latitude': 49.3988, 'longitude': 8.6724},
    {'name': 'Herne', 'latitude': 51.5369, 'longitude': 7.2009},
    {'name': 'Neuss', 'latitude': 51.2042, 'longitude': 6.6879},
]

# Method to retrieve annual sunshine hours based on an address
def get_annual_sunshine_hours(address):
    def get_coordinates(address):
        geolocator = Nominatim(user_agent="city_finder")
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError("Address not found.")
    
    def find_nearest_city(address_coords, cities):
        min_distance = float('inf')
        nearest_city = None
        for city in cities:
            city_coords = (city['latitude'], city['longitude'])
            distance = geodesic(address_coords, city_coords).kilometers
            if distance < min_distance:
                min_distance = distance
                nearest_city = city['name']
        return nearest_city
    
    try:
        address_coords = get_coordinates(address)
        nearest_city = find_nearest_city(address_coords, major_cities)
        
        # Get the annual sunshine hours for the nearest city
        sunshine_hours = df_sunshine[df_sunshine['Place'] == nearest_city]['Hours'].values[0]
        return sunshine_hours
    except ValueError as e:
        print(e)
        return None
    

# address = "Parkstraße 22, 50169 Kerpen"
# annual_sunshine_hours = get_annual_sunshine_hours(address)
# print("Annual Sunshine Hours:", annual_sunshine_hours)