from backend.find_geo import find_geo
from backend.weather import fetch_sunshine_data
import streamlit as st
from backend.orchestrator import get_potential_profits
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar for Address Input
st.sidebar.title("Address Input")
postal_code = st.sidebar.text_input("Postal Code", value="76137")
city = st.sidebar.text_input("City", value="Karlsruhe")
street = st.sidebar.text_input("Street", value="Morgenstraße")
house_number = st.sidebar.text_input("House Number", value="5")

# Sidebar for Timeframe Selection
timeframe = st.sidebar.selectbox(
    "Select Timeframe for Weather Data",
    ("Past Week", "Past Month", "Past Year")
)

# Map timeframe selection to days_back value
timeframe_map = {
    "Past Week": 7,
    "Past Month": 30,
    "Past Year": 365
}
days_back = timeframe_map[timeframe]

# Submit button
if st.sidebar.button("Submit"):
    if postal_code and city and street and house_number:
        # Fetch geolocation data
        geo = find_geo(postal_code, city, street, house_number)

        # Check if outline is available for latitude and longitude
        if geo['outline'] and len(geo['outline']) > 0:
            latitude = geo['outline'][0][0]
            longitude = geo['outline'][0][1]
            
            # Fetch sunshine data for the selected timeframe
            sunshine_data = fetch_sunshine_data(latitude, longitude, days_back)

            # Check if data is available
            if not sunshine_data.empty:
                # Visualization of sunshine duration over time
                st.title("Sunshine Duration Over Time")
                st.write(f"Showing sunshine duration for {timeframe}")

                # Plot the data
                plt.figure(figsize=(10, 5))
                plt.plot(sunshine_data["date"], sunshine_data["sunshine_hours"], label="Sunshine Hours")
                plt.xlabel("Date")
                plt.ylabel("Sunshine Duration (hours)")
                plt.title("Sunshine Duration Over Time")
                plt.legend()
                plt.grid()
                st.pyplot(plt)
            else:
                st.warning("No sunshine data available for the selected timeframe.")

            # Calculate potential profits based on location data
            potential_profits = get_potential_profits(postal_code, city, street, house_number)

            # Display results
            st.title("Here is your result:")
            st.write(f"Roof Outline: {geo['outline']}")
            st.write(f"Square Meters: {geo['squaremeters']}")
            st.write(f"Potential Profit (KPI): {potential_profits} €")

            # Display location on the map
            df = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})
            st.map(df)
        else:
            st.warning("Geolocation data could not be found. Please check the address.")
    else:
        st.warning("Please enter a complete address before submitting.")
else:
    # Display an empty map as a default
    st.map(pd.DataFrame({'latitude': [], 'longitude': []}))
