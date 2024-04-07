import logging
import sys
import tempfile

import streamlit as st
import yaml
from utils import get_pdf_iframe

from country_by_country.processor import ReportProcessor
from country_by_country.utils.utils import keep_pages

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

st.set_page_config(layout="wide")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

with st.sidebar:
    pdf = st.file_uploader("Upload a pdf document containing financial table : ")

    if pdf is not None:
        mytmpfile.write(pdf.read())
        st.session_state["original_pdf"] = mytmpfile
    if "original_pdf" in st.session_state:
        st.markdown("Already loaded file : " + st.session_state["original_pdf"].name)

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

if "original_pdf" in st.session_state:
    # Once a pdf has been uploaded, it will be stored as
    # the "original_pdf" key in the session state.
    # Hence, the following code will only be executed if a pdf has been uploaded.

    # Display the uploaded pdf
    st.markdown(
        get_pdf_iframe(st.session_state["original_pdf"].name),
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
            st.session_state["original_pdf"].name,
            assets,
        )

        logging.info(f"Assets : {assets}")

        if len(assets["pagefilter"]["selected_pages"]) == 0:
            # No page has been automatically selected by the page filter
            # Hence, we display the full pdf, letting the user select the pages
            st.session_state["pdf_before_page_validation"] = st.session_state[
                "original_pdf"
            ].name
        else:
            # Otherwise, we keep only the pages selected by the page filter
            st.session_state["pdf_before_page_validation"] = keep_pages(
                st.session_state["original_pdf"].name,
                assets["pagefilter"]["selected_pages"],
            )
            assets["pagefilter"]["selected_pages"] = []
        st.session_state["assets"] = assets
        st.switch_page("pages/1_Selected_Pages.py")
