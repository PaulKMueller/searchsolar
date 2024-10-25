from backend.find_geo import find_geo
from backend.sunshine import get_sunhours
import streamlit as st
from result import get_location_data
from backend.orchestrator import get_potential_profits

st.title("Address Form")
st.write("We can tell you how profitable solar panels are with your roof!")

postal_code = st.text_input("Postal Code")
city = st.text_input("City")
street = st.text_input("Street")
house_number = st.text_input("House Number")

# Submit button
if st.button("Submit"):
    if postal_code and city and street and house_number:
        geo = find_geo(postal_code, city, street, house_number)
        potential_profits = get_potential_profits(postal_code, city, street, house_number)
        sun_hours = get_sunhours(geo['latitude'], geo['longitude']) 

        st.title("Here is your result")
        st.write("Enter your address, and we’ll tell you how much you could earn with solar panels!")

        st.write(f"Location: {geo['latitude']}, {geo['longitude']}")
        st.write(f"Square Meters: {geo['squaremeters']}")
        st.write(f"Estimated Sun Hours: {sun_hours} hours")
        st.write(f"Potential Profit (KPI): {potential_profits} €")
    else:
        st.warning("Please enter a complete address before submitting.")