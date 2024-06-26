from pathlib import Path

import pages as pg
import streamlit as st
from streamlit.logger import get_logger
from streamlit_navigation_bar import st_navbar

import pandas as pd

LOGGER = get_logger(__name__)

if 'data_root_path' not in st.session_state:
    st.session_state['data_root_path'] = 'data/'

if 'dataset' not in st.session_state:
    st.session_state['dataset'] = pd.DataFrame()

def run() -> None:
    st.set_page_config(
        page_title="Company explorer",
        page_icon="👋",
        initial_sidebar_state="collapsed",  # "auto", "expanded", "collapsed"
        layout="wide",
    )

    pages = [
        "Home",
        "viz",
        "publication trends explorer",
        "intra-report data explorer",
        "methodology",
        "faq",
        "download data",
        "contact",
        "GitHub",
    ]

    this_path = Path(__file__).resolve()
    parent_dir = this_path.parent
    logo_path = parent_dir / "cubes.svg"
    urls = {"GitHub": "https://github.com/dataforgoodfr/12_taxobservatory.git"}
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
        logo_path=str(logo_path),
        urls=urls,
        styles=styles,
        adjust=False,
    )

    # Create a sidebar selection
    st.sidebar.radio(
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

    def load_dataset() -> pd.DataFrame:
        dataset_file = 'dataset_multi_years_cleaned_completed.tab'
        df = pd.read_csv(st.session_state.data_root_path + dataset_file, sep='\t')
        df['year'] = df['year'].astype(int)
        return df

    st.session_state['dataset'] = load_dataset()


if __name__ == "__main__":
    run()
