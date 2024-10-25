import streamlit as st

def result():
    st.title("Here is your result")
    st.write("Enter your address, and we’ll tell you how much you could earn with solar panels!")

    # Check if we have results from session state
    if 'result_data' in st.session_state:
        geo, sun_hours, kpi = st.session_state['result_data']

        st.write(f"Location: {geo['latitude']}, {geo['longitude']}")
        st.write(f"Square Meters: {geo['squaremeters']}")
        st.write(f"Estimated Sun Hours: {sun_hours} hours")
        st.write(f"Potential Profit (KPI): {kpi} €")
    else:
        st.warning("No results available. Please enter your address on the previous page.")


