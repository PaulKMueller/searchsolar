import streamlit as st
from frontend.address_form import address_form
from frontend.result import result

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'address_form'

# Control which page to display
if st.session_state['page'] == 'address_form':
    address_form()
elif st.session_state['page'] == 'result':
    result()
