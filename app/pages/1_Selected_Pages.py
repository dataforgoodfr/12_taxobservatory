import streamlit as st
from utils import get_pdf_iframe, set_validate
from country_by_country.utils.utils import keep_pages
from pypdf import PdfReader

import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

st.set_page_config(layout="wide")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Selected Pages")
st.subheader(
    "This page will allow you to select the pages containing your tables",
)

if "original_pdf" in st.session_state:

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            get_pdf_iframe(st.session_state["pdf_before_page_validation"]),
            unsafe_allow_html=True,
        )

    with col2, st.form(key="selected_pages_form"):
        pdfreader = PdfReader(st.session_state["original_pdf"])
        number_pages = (
            len(PdfReader(st.session_state["pdf_before_page_validation"]).pages) + 1
        )  # Make the index start to 1
        st.session_state["assets"]["pagefilter"]["selected_pages"] = st.multiselect(
            "Which page of the following pdf contains the table you want to extract ?",
            list(range(1, number_pages)),
            placeholder="Select a page number",
            default=(
                st.session_state["assets"]["pagefilter"]["selected_pages"]
                if "assets" in st.session_state
                else None
            ),
        )
        # TODO : add a new button in order to use original pdf if the table was not found
        submitted = st.form_submit_button(
            label="Validate your selected pages",
            on_click=set_validate,
            args=("validate_selected_pages",),
        )

    st.session_state["pdf_after_page_validation"] = keep_pages(
        st.session_state["pdf_before_page_validation"],
        [
            item - 1
            for item in st.session_state["assets"]["pagefilter"]["selected_pages"]
        ],
    )

    if (
        len(st.session_state["assets"]["pagefilter"]["selected_pages"]) != 0
        and "first_time_selected" not in st.session_state
    ):
        st.session_state["first_time_selected"] = False
        st.switch_page("pages/2_Headers.py")
