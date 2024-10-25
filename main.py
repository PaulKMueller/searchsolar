from backend.find_geo import find_geo
from backend.weather import calculate_sunshine_rain
from backend.orchestrator import get_potential_profits
import streamlit as st

st.title("Address Form")
st.write("We can tell you how profitable solar panels are with your roof!")

# Address input fields
postal_code = st.text_input("Postal Code")
city = st.text_input("City")
street = st.text_input("Street")
house_number = st.text_input("House Number")

# Submit button
if st.button("Submit"):
    if postal_code and city and street and house_number:
        # Fetch geolocation data
        geo = find_geo(postal_code, city, street, house_number)

        # Check if geolocation data is valid
        if geo['latitude'] and geo['longitude']:
            # Calculate sunshine and rainfall
            weather_data = calculate_sunshine_rain(geo['latitude'], geo['longitude'])
            sun_hours = weather_data["total_sunshine"]
            rainfall = weather_data["total_rainfall"]

            # Calculate potential profits based on location data
            potential_profits = get_potential_profits(postal_code, city, street, house_number)

            # Display results
            st.title("Here is your result")
            st.write("Enter your address, and we’ll tell you how much you could earn with solar panels!")

            st.write(f"Roof Outline: {geo['outline']}")
            st.write(f"Square Meters: {geo['squaremeters']}")
            st.write(f"Estimated Sun Hours (Last Month): {sun_hours} hours")
            st.write(f"Total Rainfall (Last Month): {rainfall} mm")
            st.write(f"Potential Profit (KPI): {potential_profits} €")
        else:
            st.warning("Could not locate the address. Please check and try again.")
    else:
        st.warning("Please enter a complete address before submitting.")
