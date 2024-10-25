import math
from backend.find_geo import find_geo
from backend.sunshine import get_annual_sunshine_hours
from backend.weather import fetch_sunshine_data
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from backend.finance import get_energy_for_hours, get_financial_kpis
from datetime import date, datetime, timedelta 
import plotly.graph_objects as go  

import plotly.express as px

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

# Sidebar for Timeframe Selection
timeframe = st.sidebar.selectbox(
        "Select Timeframe for Weather Data",
        ("Past Year", "Past Month", "Past Week"),
    )

    # Map timeframe selection to days_back value
timeframe_map = {
        "Past Week": 7,
        "Past Month": 30,
        "Past Year": 365
    }

# Submit button
if st.sidebar.button("Submit"):
    if postal_code and city and street and house_number:

        st.title("Here is your result:")

        geo_information = find_geo(postal_code, city, street, house_number)
        sun_hours = get_annual_sunshine_hours(
            f"{street} {house_number} {postal_code} {city}"
        )
        roof_area = geo_information["squaremeters"]

        days_back = timeframe_map[timeframe]

        st.write(f"**Your roof size 🏠:** {str(round(geo_information["squaremeters"], 2))} m²")
        st.write(f"**Estimated Sun Hours ☀️**: {str(sun_hours)} h/year")

        energy_output = get_energy_for_hours(roof_area, sun_hours)
        st.write(f"**Energy output:** {round(energy_output/1000, 2)} MWh/year")

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
        geo = find_geo(postal_code, city, street, house_number)
        sun_hours = get_annual_sunshine_hours(f"{street} {house_number} {postal_code} {city}") 
        financial_kpis = get_financial_kpis(geo['squaremeters'], sun_hours)

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

        sunshine_data = fetch_sunshine_data(latitude, longitude, days_back)

        # Visualization of sunshine duration over time
        st.title("Sunshine Duration Over Time")

        # Step 1: Convert the 'date' column to datetime (if not already in datetime)
        sunshine_data['date'] = pd.to_datetime(sunshine_data['date'])

        # Step 2: Group by the day and sum the 'sunshine_hours'
        sunshine_data = sunshine_data.groupby(sunshine_data['date'].dt.date)['sunshine_hours'].sum().reset_index()
        # Sample down if data for year has been selected
        if len(sunshine_data) >= 300:
            sunshine_data = sunshine_data.iloc[::int(len(sunshine_data) / 20)]
        sunshine_data.columns = ['date', 'sunshine_hours']
        plotly_plot = px.bar(sunshine_data, x="date", y="sunshine_hours")
        st.plotly_chart(plotly_plot)

         # Calculate financial KPIs based on roof area and sunlight hours
        roof_area = geo['squaremeters']
        avg_sunlight_hours = sunshine_data['sunshine_hours'].mean() * 365  # convert to avg annual sunlight hours
        financial_kpis = get_financial_kpis(roof_area, avg_sunlight_hours)

        # Extract KPI values
        annual_savings = financial_kpis['annual_savings']
        break_even_date = financial_kpis['break_even_date']
        roi = financial_kpis['roi']

        # Display Financial KPIs
        st.subheader("Financial Summary")
        st.write(f"Annual Savings: {annual_savings:.2f} €")
        st.write(f"Break-Even Date: {break_even_date}")
        st.write(f"Return on Investment: {round(roi, 2)} %")

        # Ensure break_even_date is in datetime format for compatibility
        break_even_date = datetime.combine(break_even_date, datetime.min.time())

        # Calculate cumulative savings
        cumulative_savings = []
        dates = pd.date_range(start=date.today(), periods=25, freq='Y')
        for i, dt in enumerate(dates):
            cumulative_savings.append(annual_savings * i)

        # Find the closest date in the `dates` range for the break-even date
        closest_date = min(dates, key=lambda x: abs(x.to_pydatetime() - break_even_date))

        # Create plot
        fig = go.Figure()

        # Plot cumulative savings
        fig.add_trace(go.Scatter(
            x=dates,
            y=cumulative_savings,
            mode='lines+markers',
            name='Cumulative Savings',
            line=dict(color='blue')
        ))

        # Add break-even point
        fig.add_trace(go.Scatter(
            x=[closest_date],
            y=[annual_savings * dates.get_loc(closest_date)],  # Cumulative savings at closest date
            mode='markers+text',
            name='Break-Even Point',
            text=['Break-Even'],
            textposition='top center',
            marker=dict(size=10, color='red', symbol='circle')
        ))

        # Update layout
        fig.update_layout(
            title="Cumulative Savings Over Time with Break-Even Point",
            xaxis_title="Year",
            yaxis_title="Cumulative Savings (€)"
        )

        # Display the cumulative savings plot
        st.plotly_chart(fig)
    else:
        st.warning("Please enter a complete address before submitting.")
else:
    # Display an empty map as a default
    st.map(pd.DataFrame({'latitude': [], 'longitude': []}))
