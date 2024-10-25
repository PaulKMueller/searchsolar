import streamlit as st

def get_location_data(result_data):
    st.title("Here is your result")
    st.write("Enter your address, and we’ll tell you how much you could earn with solar panels!")
    # Check if we have results from session state
    geo, sun_hours, kpi = result_data

    st.write(f"Location: {geo['latitude']}, {geo['longitude']}")
    st.write(f"Square Meters: {geo['squaremeters']}")
    st.write(f"Estimated Sun Hours: {sun_hours} hours")
    st.write(f"Potential Profit (KPI): {kpi} €")


