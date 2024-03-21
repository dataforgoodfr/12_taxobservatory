from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from streamlit_navigation_bar import st_navbar
import pages as pg
import os

LOGGER = get_logger(__name__)


def run():

    st.set_page_config(
        page_title="Company explorer",
        page_icon="👋",
        initial_sidebar_state="collapsed", # "auto", "expanded", "collapsed"
        layout="wide"
    )

    pages = [
        "Home", "viz", "publication trends explorer",
         "intra-report data explorer",  "methodology",
         "faq", "download data", "contact", "GitHub"
     ]
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(parent_dir, "cubes.svg")
    urls = {"GitHub": "https://github.com/pykoe/data4good-taxobservatory.git"}
    styles = {
        "nav": {
            "background-color": "rgb(25, 25, 25)",
        },
        "div": {
            "max-width": "65.25rem",
        },
        "span": {
            "color": "var(--text-color)",
            "border-radius": "0.5rem",
            "padding": "0.4375rem 0.625rem",
            "margin": "0 0.125rem",
        },
        "active": {
            "background-color": "rgba(151, 166, 195, 0.15)",
        },
        "hover": {
            "background-color": "rgba(151, 166, 195, 0.25)",
        },
    }

    page = st_navbar(
        pages,
        logo_path=logo_path,
        urls=urls,
        styles=styles,
        adjust=False,
    )

    # Create a sidebar selection
    selection = st.sidebar.radio(
        "Test page hiding",
        ["Show all pages", "Hide pages 1 and 2", "Hide Other apps Section"],
    )

    # Define a list of pages
    pages = ["Example One", "Example Two", "Other apps"]

    functions = {
        "Home": pg.show_home,
        "viz": pg.show_all_viz,
        "publication trends explorer": pg.show_publication,
        "intra-report data explorer": pg.show_company,
        "methodology": pg.show_methodology,
        "faq": pg.show_faq,
        "download data": pg.show_downlaod_data,
        "contact": pg.show_contact,
    }
    go_to = functions.get(page)
    if go_to:
        go_to()


if __name__ == "__main__":
    run()