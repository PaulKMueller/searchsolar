from backend.find_geo import find_geo
from backend.sunshine import get_annual_sunshine_hours
import streamlit as st
from backend.orchestrator import get_potential_profits
import pandas as pd


st.sidebar.title("Address Input")

postal_code = st.sidebar.text_input("Postal Code", value="76137")
city = st.sidebar.text_input("City", value="Karlsruhe")
street = st.sidebar.text_input("Street", value="Morgenstraße")
house_number = st.sidebar.text_input("House Number", value="5")

# Submit button
if st.sidebar.button("Submit"):
    if postal_code and city and street and house_number:
        geo = find_geo(postal_code, city, street, house_number)
        potential_profits = get_potential_profits(postal_code, city, street, house_number)
        sun_hours = get_annual_sunshine_hours(f"{street} {house_number} {postal_code} {city}") 

        st.title("Here is your result:")
        st.write(f"Roof Outline: {geo['outline']}")
        st.write(f"Square Meters: {geo['squaremeters']}")
        st.write(f"Estimated Sun Hours: {sun_hours} hours")
        st.write(f"Potential Profit (KPI): {potential_profits} €")
        latitude = geo['outline'][0][0]
        longitude = geo['outline'][0][1]

        df = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})
        st.map(df)
    else:
        st.warning("Please enter a complete address before submitting.")
else:
    st.map()