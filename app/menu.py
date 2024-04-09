import streamlit as st


def display_pages_menu() -> None:
    st.sidebar.page_link("index.py", label="Home - upload PDF")
    st.sidebar.page_link("pages/1_Selected_Pages.py", label="Pages selection")
    st.sidebar.page_link("pages/2_Headers.py", label="Headers setup")
    st.sidebar.page_link("pages/3_Tables.py", label="Tables customization")
