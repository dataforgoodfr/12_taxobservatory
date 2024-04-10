import streamlit as st
from utils import get_pdf_iframe
from country_by_country.utils.utils import keep_pages
from pypdf import PdfReader

import sys
import copy
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def set_validate() -> None:
    st.session_state["validate_selected_pages"] = True


st.set_page_config(layout="wide")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Selected Pages")
st.subheader(
    "This page will allow you to select the pages containing your tables",
)

if "working_file_pdf" in st.session_state:

    col1, col2 = st.columns([1, 1])

    with col2:
        # Display the page selector on the right column
        pdfreader = PdfReader(st.session_state["working_file_pdf"])
        number_pages = len(PdfReader(st.session_state["working_file_pdf"]).pages)
        logging.info("got the assets : " + str(st.session_state["assets"]))
        selected_pages = st.multiselect(
            "Which page of the following pdf contains the table you want to extract ? Defaults pages are the pages extracted by the decision tree algorithm",
            list(range(1, number_pages + 1)),
            placeholder="Select a page number",
            default=[
                i + 1
                for i in st.session_state["assets"]["pagefilter"]["selected_pages"]
            ],
            disabled=True if "validate_selected_pages" in st.session_state else False,
        )
        submitted = st.button(
            label="Validate your selected pages",
            on_click=set_validate,
        )

    selected_pages = sorted(selected_pages)
    logging.info("Filtering the pdf with pages : " + str(selected_pages))
    st.session_state["pdf_before_page_validation"] = keep_pages(
        st.session_state["working_file_pdf"].name,
        [i - 1 for i in selected_pages],
    )

    with col1:
        # Display the filtered pdf on the left column
        st.markdown(
            get_pdf_iframe(st.session_state["pdf_before_page_validation"]),
            unsafe_allow_html=True,
        )

    if submitted:
        # Once the submission button is clicked, we commit the selected pages
        # The next pages will work with the pdf_after_page_validation
        st.session_state["assets"]["pagefilter"]["selected_pages"] = [
            i - 1 for i in selected_pages
        ]
        st.session_state["pdf_after_page_validation"] = keep_pages(
            st.session_state["working_file_pdf"].name,
            [i - 1 for i in selected_pages],
        )
        st.switch_page("pages/2_Merge_Tables.py")
