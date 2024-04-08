import logging
import sys
import tempfile

import streamlit as st
import yaml
from pypdf import PdfReader
from utils import get_pdf_iframe
from menu import display_pages_menu

from country_by_country.processor import ReportProcessor

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

st.set_page_config(layout="wide", page_title="Accueil - upload de PDF")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)
display_pages_menu()

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

with st.sidebar:
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

    loaded_config = st.file_uploader(
        "Upload a config if the default config doesn't suit you :",
    )

    yaml_config = """
pagefilter:
  type: RFClassifier
  params:
    modelfile: random_forest_model_low_false_positive.joblib

table_extraction:
  - type: Camelot
    params:
      flavor: stream
  - type: Camelot
    params:
      flavor: lattice
  - type: Unstructured
    params:
      hi_res_model_name: "yolox"
      pdf_image_dpi: 300
    """

    if loaded_config is None:
        st.session_state["config"] = yaml.safe_load(yaml_config)
    else:
        st.session_state["config"] = yaml.safe_load(loaded_config)
    yaml_str = yaml.dump(st.session_state["config"], default_flow_style=False, indent=2)
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
