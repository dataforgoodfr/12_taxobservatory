import logging
import sys
import tempfile

import streamlit as st
import yaml
import copy
from menu import display_pages_menu, display_config
from pypdf import PdfReader
from utils import get_pdf_iframe, set_state, generate_assets

from country_by_country.processor import ReportProcessor

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def set_page_filter(value: dict):
    set_state(["config", "pagefilter"], value)


def initiate_configuration() -> None:
    st.session_state["config"] = copy.deepcopy(st.session_state["initial_config"])
    if isinstance(st.session_state["config"]["pagefilter"], list):
        st.session_state["config"]["pagefilter"] = st.session_state["initial_config"][
            "pagefilter"
        ][0]
    st.session_state["selected_page_filter_name"] = st.session_state["config"][
        "pagefilter"
    ]["type"]


def on_pdf_file_upload() -> None:
    # Change states related to the pdf file upload
    mytmpfile.write(st.session_state.original_pdf.read())
    st.session_state["working_file_pdf"] = mytmpfile
    st.session_state["original_pdf_name"] = st.session_state.original_pdf.name

    # Generate assets
    generate_assets()

    st.session_state["page_redirection"] = "pages/1_Selected_Pages.py"


def on_config_file_upload() -> None:
    st.session_state["initial_config"] = st.session_state["initial_uploaded_config"]
    initiate_configuration()


def on_change_page_filter(name_to_filter_dict: dict) -> None:
    st.session_state["selected_page_filter_name"] = st.session_state[
        "radio_button_filter_selection"
    ]  # this 'buffer' is needed because selectors wipe their key on reload
    set_page_filter(name_to_filter_dict[st.session_state["selected_page_filter_name"]])


# Check if a redirection was requested
# Workaround because st.switch_page is not allowed in a callback function
if st.session_state.get("page_redirection", False):
    page_to_redirect_to = st.session_state["page_redirection"]
    st.session_state["page_redirection"] = False
    st.switch_page(page_to_redirect_to)

st.set_page_config(layout="wide", page_title="Accueil - upload de PDF")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)
display_pages_menu()

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

# State initialization
if "first_time" not in st.session_state:
    logging.info("State initialization...")
    st.session_state["first_time"] = False

    logging.info("... loading default extract config")
    with open("app/extract_config.yaml", "r") as f:
        st.session_state["initial_config"] = yaml.safe_load(f.read())
    initiate_configuration()

    logging.info("... initializing processor")
    st.session_state["proc"] = ReportProcessor(st.session_state["config"])
    st.session_state["assets"] = {
        "pagefilter": {},
        "table_extractors": [],
    }


with st.sidebar:

    st.markdown("# PDF Upload")

    st.markdown("## PDF Report to process")
    original_pdf = st.file_uploader(
        "Upload a pdf document containing financial table : ",
        key="original_pdf",
        on_change=on_pdf_file_upload,
    )

    if "original_pdf_name" in st.session_state:
        st.markdown(
            "Already loaded file : " + st.session_state["original_pdf_name"],
        )

    st.markdown("# Configuration:\n")
    # Upload personalized config if required
    loaded_config = st.file_uploader(
        "Upload a config if the default config doesn't suit you :",
        key="initial_uploaded_config",
        on_change=initiate_configuration,
    )

    if loaded_config is not None:
        if not loaded_config.name.endswith(".yaml"):
            st.error("Please upload a yaml file")
            loaded_config = None

        try:
            loaded_config_dict = yaml.safe_load(loaded_config)
            if not (
                loaded_config_dict.get("pagefilter", False)
                and loaded_config_dict.get("table_extraction", False)
            ):
                st.error("Please upload a valid config file")
                loaded_config = None
        except yaml.YAMLError as e:
            st.error("Unable to load yaml file config")
            loaded_config = None

    # Extract config

    if bool(loaded_config):
        st.session_state["initial_config"] = loaded_config_dict
        st.session_state["config"] = copy.deepcopy(st.session_state["initial_config"])

    # Set page filter
    page_filter_name_to_config_mapping = {
        pagefilter["type"]: pagefilter
        for pagefilter in st.session_state["initial_config"]["pagefilter"]
    }
    page_filter_list = list(page_filter_name_to_config_mapping.keys())
    current_selected_page_filter_index = page_filter_list.index(
        st.session_state["selected_page_filter_name"]
    )
    selected_page_filter_name = st.radio(
        "Page filter",
        page_filter_list,
        index=current_selected_page_filter_index,
        on_change=on_change_page_filter,
        key="radio_button_filter_selection",
        args=(page_filter_name_to_config_mapping,),
    )

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
