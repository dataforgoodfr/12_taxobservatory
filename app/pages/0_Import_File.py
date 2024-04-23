import logging
import sys
import tempfile

import streamlit as st
import yaml
from menu import display_pages_menu
from pypdf import PdfReader
from utils import get_pdf_iframe, set_state

from country_by_country.processor import ReportProcessor

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

def set_extractors(value: list):
    set_state(["config", "table_extraction"], value)

st.set_page_config(layout="wide", page_title="Accueil - upload de PDF")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)
display_pages_menu()

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

with st.sidebar:

    st.markdown("# Configuration")

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

    st.markdown("## Pipeline configuration")
    loaded_config = st.file_uploader(
        "Upload a config if the default config doesn't suit you :",
    )

    with open("app/extract_config.yaml", "r") as f:
        default_config=f.read()


    if loaded_config is None:
        config = yaml.safe_load(default_config)        
    else:
        config = yaml.safe_load(loaded_config)
    
    if st.session_state.get("first_time", True):
        st.session_state["config"] = config

    st.write("Config:\n\n")
    page_filter_list = [pagefilter["type"] for pagefilter in config["pagefilter"]]
    st.radio("Page filter", page_filter_list)
    
    #Set extractors
    all_table_extractors = {extractor["type"]: extractor for extractor in config["table_extraction"]}
    current_table_extractors = [extractor['type'] for extractor in st.session_state['config']['table_extraction']]
    extractor_keys = st.multiselect("Extractors", options=all_table_extractors.keys(), default=current_table_extractors)
    set_extractors([all_table_extractors[key] for key in extractor_keys])
    
    yaml_str = yaml.dump(st.session_state["config"], default_flow_style=False, sort_keys=False, indent=2)
    # Ajouter des backticks triples pour créer un bloc de code markdown
    markdown_str = f"The configuration is : \n\n```\n{yaml_str}\n```"
    st.write(markdown_str)

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
            number_pages = len(PdfReader(st.session_state["working_file_pdf"]).pages)
            assets["pagefilter"]["selected_pages"] = list(range(number_pages))
        st.session_state["assets"] = assets
        st.switch_page("pages/1_Selected_Pages.py")

