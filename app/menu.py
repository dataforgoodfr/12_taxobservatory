import streamlit as st


def display_pages_menu() -> None:

    with st.sidebar:
        if "original_pdf_name" in st.session_state:
            st.markdown(
                f"Currently processing : {st.session_state['original_pdf_name']}",
            )
    st.sidebar.page_link("pages/0_Import_File.py", label="Upload PDF")
    st.sidebar.page_link("pages/1_Selected_Pages.py", label="Pages selection")
    st.sidebar.page_link("pages/2_Merge_Tables.py", label="Merge tables")
    st.sidebar.page_link("pages/3_Clean_Headers.py", label="Headers setup")
    st.sidebar.page_link("pages/4_Clean_Tables.py", label="Tables customization")
