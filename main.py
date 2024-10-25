import streamlit as st
from frontend.address_form import address_form
from frontend.result import result

if "page" not in st.session_state:
    st.session_state.page = "address_form"

def navigate_to(page):
    st.session_state.page = page

if st.session_state.page == "address_form":
    address_form()
elif st.session_state.page == "show_result":
    result()
