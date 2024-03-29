import base64
from pathlib import Path
import pandas as pd
import re

import streamlit as st
from streamlit import session_state as ss
import pickle
import os
import streamlit_pills
from streamlit_option_menu import option_menu
from pandas import option_context
from streamlit_pdf_viewer import pdf_viewer
import json
from huggingface_hub import hf_hub_download
from country_by_country import pagefilter
from country_by_country.utils.utils import append_count_to_duplicates, reformat

# Callbacks
def on_pdf_selected():
    ss["pdf_downloaded"] = hf_hub_download(repo_id="DataForGood/taxobservatory_data", filename=ss.pdf_selected, repo_type="dataset")

def on_table_selected(key):
    selected = ss[key]
    ss.selected_idx = int(selected.split(" ",1)[1])

# Initialization
if 'selected_idx' not in ss:
    ss.selected_idx = 0

if 'pdf_downloaded' not in ss:
    ss.pdf_downloaded = None

# Display title
st.set_page_config(layout="wide")
st.title("Table extraction benchmark")


# Display sidebar
with st.sidebar:
    # Select pickle containing results 
    uploaded_file = st.file_uploader("Select a pickle file to load results")

    if uploaded_file:
        # Load pickle
        assets = pickle.load(uploaded_file)

        # List PDFs
        pdf_files = [os.path.basename(asset[0]) for asset in assets]
        asset_dict = {}
        for asset in assets:
            asset_dict[os.path.basename(asset[0])] = asset[1]

        # Select PDF to load results
        pdf_file = st.selectbox("Select a PDF file", asset_dict.keys(), on_change=on_pdf_selected, key="pdf_selected")


# Pull the extractions applied to the PDF
if "pdf_file" in locals():
    extractions = [extractor["type"] for extractor in asset_dict[pdf_file]["table_extractors"]]
    extractions = append_count_to_duplicates(extractions)
    extractions.append("PDF")

    # Select reference extraction for comparison
    with st.sidebar:
        ref_extraction = st.selectbox("Select ref extraction for comparison", extractions[:-1], index=0)
        if ref_extraction is not None:
            ss.ref_extraction = ref_extraction

    # Display tabs (one per extraction + one to display PDF)
    tabs = st.tabs(extractions)

    for idx, tab in enumerate(tabs[:-1]):
        with tab:
            # Display parameters of the extraction
            st.write(json.dumps(asset_dict[pdf_file]["table_extractors"][idx]["params"]))

            #P Pull tables from the extraction
            dfs = asset_dict[pdf_file]["table_extractors"][idx]["tables"]
            dfs_str = ["Table " + str(i) for i in range(len(dfs))]

            # Select table to display
            selected = option_menu(None, dfs_str, menu_icon=None, icons=None, manual_select=min(ss.selected_idx,len(dfs_str)-1), 
                orientation="horizontal", key="tab_" + str(idx), on_change=on_table_selected,
                styles={
                    "container": {"padding": "0!important", "margin": "0!important", "background-color": "#ffffff"},
                    "nav-item": {"max-width": "100px", "color": "black", "font-size": "14px"},
                    "icon": {"font-size": "0px"}}
            )
            ss.selected_idx = dfs_str.index(selected)
            
            # Display table
            df = dfs[ss.selected_idx]

            # Check if values in table are in tables of reference extraction
            refvalues = []
            for dfref in asset_dict[pdf_file]["table_extractors"][extractions.index(ref_extraction)]["tables"]:
                refvalues.extend(dfref.map(reformat).to_numpy().flatten())
            mask = df.map(reformat).isin(refvalues)

            # Apply font color (green vs red) based on above check
            def color_mask(val):
                return f'color: {"green" if val == True else "red"}'
            dfst = df.style.apply(lambda _: mask.map(color_mask), axis=None)

            # Display table with appropriate font color
            column_config = {}
            for col in df.columns:
                column_config[col] = st.column_config.Column(width="small")

            st.dataframe(dfst, 
                column_config=column_config,
                use_container_width=True,
                height=1000
            )
            
    # Last tab to display PDF
    with tabs[-1]:

        if not ss.pdf_downloaded:
            ss["pdf_downloaded"] = hf_hub_download(repo_id="DataForGood/taxobservatory_data", filename=ss.pdf_selected, repo_type="dataset")

        if ss.pdf_downloaded:
            # Get pages to render
            assets = {}
            pagefilter.FromFilename()(ss.pdf_downloaded, assets=assets)
            pages_to_render = [page+1 for page in assets["pagefilter"]["selected_pages"]]

            # Render pages from PDF
            pdf_viewer(input=ss.pdf_downloaded, pages_to_render=pages_to_render, width=1000)
