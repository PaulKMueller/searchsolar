import streamlit as st
from backend.orchestrator import orchestrate

def address_form():
    st.title("Address Form")
    st.write("We can tell you how profitable solar panels are with your roof!")

    postal_code = st.text_input("Postal Code")
    city = st.text_input("City")
    street = st.text_input("Street")
    house_number = st.text_input("House Number")

    # Submit button
    if st.button("Submit"):
        if postal_code and city and street and house_number:
            result_data = orchestrate(postal_code, city, street, house_number)
            st.session_state['result_data'] = result_data  # Store result in session state
            st.session_state['page'] = 'result'  # Set page to result
        else:
            st.warning("Please enter a complete address before submitting.")