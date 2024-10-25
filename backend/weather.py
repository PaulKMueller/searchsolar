import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta

# Initialize caching and retry mechanisms
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_date_range(days_back):
    """Calculate the start and end dates based on the number of days back from today."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date

def fetch_sunshine_data(lat, lon, days_back):
    """Fetch sunshine duration data for a given location and period."""
    start_date, end_date = get_date_range(days_back)
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": ["sunshine_duration"],
        "timezone": "auto"
    }
    
    # Make API call to fetch sunshine data
    responses = openmeteo.weather_api(url, params=params)
    
    # Check if data was returned
    if not responses:
        print("No data returned for sunshine_duration.")
        return pd.DataFrame()

    response = responses[0]
    hourly = response.Hourly()

    # Retrieve sunshine duration values
    try:
        sunshine_duration = hourly.Variables(0).ValuesAsNumpy()  # Sunshine duration in seconds
    except IndexError:
        print("Error: Could not retrieve sunshine duration data.")
        return pd.DataFrame()

    # Construct DataFrame with hourly timestamps and sunshine duration data
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "sunshine_duration": sunshine_duration
    }

    # Create DataFrame for hourly sunshine duration data
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    
    # Convert sunshine duration from seconds to hours for easier interpretation
    hourly_dataframe["sunshine_hours"] = hourly_dataframe["sunshine_duration"] / 3600

    return hourly_dataframe