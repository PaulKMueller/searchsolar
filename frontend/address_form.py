import streamlit as st
from ..main import navigate_to
from ..backend import orchestrator

def address_form():
    st.title("Address-Formular")
    st.write("We can tell you within seconds how profitable solar panels is with your own roof!")

    postal_code = st.text_input("Postal Code")
    city = st.text_input("City")
    street = st.text_input("Street")
    house_number = st.text_input("House Number")

    # Submit button
    if st.button("Submit"):
        if postal_code and city and street and house_number:
            orchestrator(postal_code, city, street, house_number)
            navigate_to("show_result")
        else:
            st.warning("Please enter an address before submitting.")