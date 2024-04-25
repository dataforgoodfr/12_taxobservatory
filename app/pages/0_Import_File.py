import logging
import sys
import tempfile

import streamlit as st
import yaml
from menu import display_pages_menu, display_config
from pypdf import PdfReader
from utils import get_pdf_iframe, set_state

from country_by_country.processor import ReportProcessor

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def set_page_filter(value: dict):
    set_state(["config", "pagefilter"], value)


st.set_page_config(layout="wide", page_title="Accueil - upload de PDF")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)
display_pages_menu()

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

with st.sidebar:

    st.markdown("# PDF Upload")

    st.markdown("## PDF Report to process")
    original_pdf = st.file_uploader(
        "Upload a pdf document containing financial table : ",
    )

    if original_pdf is not None:
        mytmpfile.write(original_pdf.read())
        st.session_state["working_file_pdf"] = mytmpfile
        st.session_state["original_pdf_name"] = original_pdf.name

    if "original_pdf_name" in st.session_state:
        st.markdown(
            "Already loaded file : " + st.session_state["original_pdf_name"],
        )

    st.markdown("# Configuration:\n")
    # Upload personalized config if required
    loaded_config = st.file_uploader(
        "Upload a config if the default config doesn't suit you :",
    )

    # Default extract config
    with open("app/extract_config.yaml", "r") as f:
        default_config = f.read()

    if bool(loaded_config):
        st.session_state["initial_config"] = yaml.safe_load(loaded_config)
    else:
        st.session_state["initial_config"] = yaml.safe_load(default_config)

    if st.session_state.get("first_time", True):
        st.session_state["config"] = st.session_state["initial_config"]

    # Set page filter
    page_filter_radio_dict = {
        pagefilter["type"]: pagefilter for pagefilter in st.session_state["initial_config"]["pagefilter"]
    }
    selected_page_filter = st.radio("Page filter", page_filter_radio_dict.keys())
    set_page_filter(page_filter_radio_dict[selected_page_filter])

    display_config()

    
            

if "working_file_pdf" in st.session_state:
    # Once a pdf has been uploaded, it will be stored as
    # the "original_pdf" key in the session state.
    # Hence, the following code will only be executed if a pdf has been uploaded.

    # Display the uploaded pdf
    st.markdown(
        get_pdf_iframe(st.session_state["working_file_pdf"].name),
        unsafe_allow_html=True,
    )

    if "first_time" not in st.session_state:
        st.session_state["first_time"] = False
        logging.info("Loading config and pdf")
        st.session_state["proc"] = ReportProcessor(st.session_state["config"])

        logging.info("Config and pdf loaded")

        assets = {
            "pagefilter": {},
            "table_extractors": [],
        }

        # Filtering the pages
        st.session_state["proc"].page_filter(
            st.session_state["working_file_pdf"].name,
            assets,
        )

        logging.info(f"Assets : {assets}")

        if len(assets["pagefilter"]["selected_pages"]) == 0:
            # No page has been automatically selected by the page filter
            # Hence, we display the full pdf, letting the user select the pages
            pdfreader = PdfReader(st.session_state["working_file_pdf"])
            number_pages = len(
                PdfReader(st.session_state["working_file_pdf"]).pages
            )
            assets["pagefilter"]["selected_pages"] = list(range(number_pages))
        st.session_state["assets"] = assets
        st.switch_page("pages/1_Selected_Pages.py")
