import math
from backend.find_geo import find_geo
from backend.sunshine import get_annual_sunshine_hours
import streamlit as st
from backend.orchestrator import get_potential_profits
import pandas as pd
import pydeck as pdk
import numpy as np
from scipy.spatial import ConvexHull

def compute_outline(latitudes, longitudes):
    """
    Compute the outline (convex hull) of a set of latitude and longitude points.
    
    Args:
        latitudes (list): List of latitude values.
        longitudes (list): List of longitude values.
    
    Returns:
        outline (list): List of points (latitude, longitude) representing the boundary (convex hull) in sequence.
    """
    # Combine the latitudes and longitudes into an array of points
    points = np.column_stack((longitudes, latitudes))
    
    # Compute the convex hull
    hull = ConvexHull(points)
    
    # Extract the vertices of the convex hull in the correct sequence
    outline = [(points[vertex, 1], points[vertex, 0]) for vertex in hull.vertices]
    
    return outline


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
        latitude = geo_information["outline"][0][0]
        longitude = geo_information["outline"][0][1]

        # Compute the outline using the helper function
        latitudes = [x[0] for x in geo_information["outline"]]
        longitudes = [x[1] for x in geo_information["outline"]]
        outline = compute_outline(latitudes, longitudes)

        # Create DataFrames for points and outline paths
        df_points = pd.DataFrame({"latitude": latitudes, "longitude": longitudes})
        df_outline = pd.DataFrame({"latitude": [x[0] for x in outline], "longitude": [x[1] for x in outline]})

        # Prepare the outline as lines for plotting
        lines_data = []
        for i in range(len(df_outline) - 1):
            lines_data.append({
                'start': [df_outline['longitude'].iloc[i], df_outline['latitude'].iloc[i]],
                'end': [df_outline['longitude'].iloc[i + 1], df_outline['latitude'].iloc[i + 1]]
            })
        # Close the loop by connecting the last point to the first
        lines_data.append({
            'start': [df_outline['longitude'].iloc[-1], df_outline['latitude'].iloc[-1]],
            'end': [df_outline['longitude'].iloc[0], df_outline['latitude'].iloc[0]]
        })

        # Define a PyDeck layer for the scatter plot (points)
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_points,
            get_position='[longitude, latitude]',
            get_radius=1,          # Set radius of points
            get_fill_color=[0, 0, 255],  # Red color for points
            pickable=True,
            auto_highlight=True
        )

        # Define a PyDeck layer for the outline (lines connecting the points)
        line_layer = pdk.Layer(
            "LineLayer",
            data=lines_data,
            get_source_position="start",
            get_target_position="end",
            get_color=[0, 0, 255],  # Blue color for lines
            get_width=2,
            pickable=True
        )

        # Define the PyDeck chart with an initial view
        view_state = pdk.ViewState(
            latitude=latitudes[0],
            longitude=longitudes[0],
            zoom=18,
            pitch=0,
        )

        # Combine layers into a pydeck chart
        deck = pdk.Deck(
            # Satellite map style
            map_style="mapbox://styles/mapbox/light-v9",
            layers=[scatter_layer, line_layer],  # You can add more layers here
            initial_view_state=view_state,
            tooltip={"text": "{latitude}, {longitude}"}
        )

        # Show the chart in Streamlit
        st.pydeck_chart(deck)

        st.subheader("Your roof size 🏠:")
        st.write(str(round(geo_information["squaremeters"], 2)) + " m²")
        st.subheader("Estimated Sun Hours ☀️:")
        st.write(f"{str(sun_hours)} h/year")
        st.write(f"Potential Profit (KPI): {potential_profits} €")

    else:
        st.warning("Please enter a complete address before submitting.")
else:
    st.map()
