import math
from backend.find_geo import find_geo
from backend.sunshine import get_annual_sunshine_hours
import streamlit as st
from backend.orchestrator import get_potential_profits
import pandas as pd
import pydeck as pdk
import numpy as np


st.sidebar.title("Address Input")

postal_code = st.sidebar.text_input("Postal Code", value="76137")
city = st.sidebar.text_input("City", value="Karlsruhe")
street = st.sidebar.text_input("Street", value="Morgenstraße")
house_number = st.sidebar.text_input("House Number", value="5")

# Submit button
if st.sidebar.button("Submit"):
    if postal_code and city and street and house_number:
        geo_information = find_geo(postal_code, city, street, house_number)
        potential_profits = get_potential_profits(
            postal_code, city, street, house_number
        )
        sun_hours = get_annual_sunshine_hours(
            f"{street} {house_number} {postal_code} {city}"
        )

        st.title("Here is your result:")
        st.subheader("Your roof size 🏠:")
        st.write(str(round(geo_information["squaremeters"], 2)) + " m²")
        st.subheader("Estimated Sun Hours ☀️:")
        st.write(f"{str(sun_hours)} h/year")
        st.write(f"Potential Profit (KPI): {potential_profits} €")
        latitude = geo_information["outline"][0][0]
        longitude = geo_information["outline"][0][1]

        latitudes = [x[0] for x in geo_information["outline"]]
        longitudes = [x[1] for x in geo_information["outline"]]

        df = pd.DataFrame({"latitude": latitudes, "longitude": longitudes})
        st.map(df, size=1, zoom=18)

        chart_data = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=["lat", "lon"],
        )
    else:
        st.warning("Please enter a complete address before submitting.")
else:
    st.map()
