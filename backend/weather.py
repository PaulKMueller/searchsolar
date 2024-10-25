# sunshine.py
import requests
from datetime import datetime, timedelta

API_KEY = "f421378da6b2ca61895a4055a554f186"

def get_unix_timestamps(days_back=30):
    today = datetime.now()
    return [(today - timedelta(days=i)).timestamp() for i in range(days_back)]

def fetch_weather_data(lat, lon, timestamp):
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        'lat': lat,
        'lon': lon,
        'dt': int(timestamp),
        'appid': API_KEY,
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    return response.json()

def calculate_sunshine_rain(lat, lon, days_back=30):
    timestamps = get_unix_timestamps(days_back)
    total_sunshine = 0
    total_rainfall = 0

    for timestamp in timestamps:
        data = fetch_weather_data(lat, lon, timestamp)
        daily_sunshine = sum(hourly.get('uvi', 0) for hourly in data.get('hourly', []))
        daily_rainfall = sum(hourly.get('rain', {}).get('1h', 0) for hourly in data.get('hourly', []))

        total_sunshine += daily_sunshine
        total_rainfall += daily_rainfall

    return {
        "total_sunshine": total_sunshine,
        "total_rainfall": total_rainfall
    }

# address = "Parkstraße 22, 50169 Kerpen"
# annual_sunshine_hours = get_annual_sunshine_hours(address)
# print("Annual Sunshine Hours:", annual_sunshine_hours)