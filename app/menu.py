import streamlit as st


def display_pages_menu() -> None:
    with st.sidebar:
        st.markdown("# Reset")
        st.markdown("Click the button below to reset the app")
        if st.button("Reset", type="primary"):
            st.session_state.clear()
            st.switch_page("index.py")

        st.markdown("# Pipeline steps")
        st.page_link("pages/0_Import_File.py", label="Upload PDF")
        st.page_link("pages/1_Selected_Pages.py", label="Pages selection")
        st.page_link("pages/2_Metadata.py", label="Metadata")
        st.page_link("pages/3_Merge_Tables.py", label="Merge tables")
        st.page_link("pages/4_Clean_Headers.py", label="Headers setup")
        st.page_link("pages/5_Clean_Tables.py", label="Tables customization")
