import streamlit as st
from country_by_country.processor import ReportProcessor
from utils import get_pdf_iframe, set_state, generate_assets
from country_by_country.utils.utils import keep_pages
from pypdf import PdfReader
from menu import display_pages_menu, display_config

import sys
import copy
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

ALL_TABLE_EXTRACTORS = {
    extractor["type"]: extractor
    for extractor in st.session_state["initial_config"]["table_extraction"]
}


def set_validate() -> None:
    st.session_state["validate_selected_pages"] = True


def set_extractors() -> None:
    if st.session_state.get("extractor_keys") is None:
        return
    selected_extractors_dict = [
        ALL_TABLE_EXTRACTORS[key] for key in st.session_state["extractor_keys"]
    ]
    set_state(["config", "table_extraction"], selected_extractors_dict)
    st.session_state["proc"] = ReportProcessor(st.session_state["config"])
    generate_assets()


st.set_page_config(layout="wide", page_title="Pages selection")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Selected Pages")
st.subheader(
    "This page will allow you to select the pages containing your tables",
)
display_pages_menu()
with st.sidebar:
    display_config()

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

        # Set extractors
        current_table_extractors = [
            extractor["type"]
            for extractor in st.session_state["config"]["table_extraction"]
        ]
        extractor_keys = st.multiselect(
            "Extractors",
            key="extractor_keys",
            options=ALL_TABLE_EXTRACTORS.keys(),
            default=current_table_extractors,
            on_change=set_extractors,
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
        st.switch_page("pages/2_Metadata.py")
