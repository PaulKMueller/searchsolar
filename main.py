from backend.find_geo import find_geo
from backend.sunshine import get_annual_sunshine_hours
import streamlit as st
from backend.finance import get_financial_kpis

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
        sun_hours = get_annual_sunshine_hours(f"{street} {house_number} {postal_code} {city}") 
        financial_kpis = get_financial_kpis(geo['squaremeters'], sun_hours)

        st.title("Here is your result")
        st.write("Enter your address, and we’ll tell you how much you could earn with solar panels!")

        st.write(f"Roof Outline: {geo['outline']}")
        st.write(f"Square Meters: {geo['squaremeters']}")
        st.write(f"Estimated Sun Hours: {sun_hours} hours")
        st.write(f"Annual savings: {financial_kpis['annual_savings']} €")
        st.write(f"Break even after: {financial_kpis['break_even_after']} years")
        st.write(f"Return of investment: {financial_kpis['roi']} %")
    else:
        st.warning("Please enter a complete address before submitting.")