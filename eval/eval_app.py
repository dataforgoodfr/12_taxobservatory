# MIT License
#
# Copyright (c) 2024 dataforgood
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Standard imports
import json
import pickle
import sys
from pathlib import Path

# External imports
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download
from streamlit import session_state as ss
from streamlit_option_menu import option_menu
from streamlit_pdf_viewer import pdf_viewer
from utils import append_count_to_duplicates, convert_to_str, reformat_str

from country_by_country import pagefilter


# Callbacks
def on_pdf_selected() -> None:
    ss["pdf_downloaded"] = hf_hub_download(
        repo_id="DataForGood/taxobservatory_data",
        filename=ss.pdf_selected,
        repo_type="dataset",
    )


def on_table_selected(key: str) -> None:
    selected = ss[key]
    ss.selected_idx = int(selected.split(" ", 1)[1])


def main(ref_data_file: str = None) -> None:
    # Initialization
    st.set_page_config(layout="wide")

    if "selected_idx" not in ss:
        ss.selected_idx = 0

    if "pdf_downloaded" not in ss:
        ss.pdf_downloaded = None

    if "ref_uploaded" not in ss:
        try:
            ss.ref_uploaded = pd.read_csv(ref_data_file)
        except Exception:
            st.warning(
                """REF data not found. Continue without or set the constant ref_data_file /
                to the full path of the data_step2_before-currency-unit.csv file.""",
            )
            ss.ref_uploaded = None

    # Display title
    st.title("Table extraction benchmark")

    # Display sidebar
    with st.sidebar:
        # Select pickle containing results
        uploaded_file = st.file_uploader(
            "Select a pickle file to load results",
            type="pkl",
            help="Run eval_table_extraction.py to generate a picke file.",
        )

        if uploaded_file:
            # Load pickle
            assets = pickle.load(uploaded_file)

            # List PDFs
            pdf_files = [Path(asset[0]).name for asset in assets]
            asset_dict = {}
            for asset in assets:
                asset_dict[Path(asset[0]).name] = asset[1]

            # Select PDF to load results
            pdf_file = st.selectbox(
                "Select a PDF file",
                asset_dict.keys(),
                on_change=on_pdf_selected,
                key="pdf_selected",
            )

    # Pull the extractions applied to the PDF
    if "pdf_file" in locals() and pdf_file:
        # Append REF data matching the PDF to our assets
        if ss.ref_uploaded is not None:
            company = pdf_file.split("_")[0]
            year = pdf_file.split("_")[1]
            cols = [2, *list(range(5, 10)), *list(range(15, 18))]
            ref_df = (
                ss.ref_uploaded.query(f'company=="{company}" and year=={year}')
                .iloc[:, cols]
                .reset_index(drop=True)
                .dropna(axis="columns", how="all")
            )
            asset_dict[pdf_file]["table_extractors"].append(
                {
                    "type": "REF",
                    "params": {"src_file": ref_data_file},
                    "tables": [ref_df],
                },
            )

        # Pull the extractions from the asssets
        extractions = [
            extractor["type"] for extractor in asset_dict[pdf_file]["table_extractors"]
        ]
        extractions = append_count_to_duplicates(extractions)
        extractions.append("PDF")

        # Select reference extraction for comparison (default to REF data)
        with st.sidebar:
            try:
                ref_idx = extractions.index("REF")
            except Exception:
                ref_idx = 0
            ref_extraction = st.selectbox(
                "Select ref extraction for comparison",
                extractions[:-1],
                index=ref_idx,
            )
            if ref_extraction is not None:
                ss.ref_extraction = ref_extraction

        # Display tabs (one per extraction + one to display PDF)
        tabs = st.tabs(extractions)

        for idx, tab in enumerate(tabs[:-1]):
            with tab:
                # Display parameters of the extraction
                st.write(
                    json.dumps(asset_dict[pdf_file]["table_extractors"][idx]["params"]),
                )

                # Pull tables from the extraction
                dfs = asset_dict[pdf_file]["table_extractors"][idx]["tables"]
                dfs = [df.map(convert_to_str).replace("nan", "") for df in dfs]
                dfs_str = ["Table " + str(i) for i in range(len(dfs))]

                # Select table to display
                selected = option_menu(
                    None,
                    dfs_str,
                    menu_icon=None,
                    icons=None,
                    manual_select=min(ss.selected_idx, len(dfs_str) - 1),
                    orientation="horizontal",
                    key="tab_" + str(idx),
                    on_change=on_table_selected,
                    styles={
                        "container": {
                            "padding": "0!important",
                            "margin": "0!important",
                            "background-color": "#ffffff",
                        },
                        "nav-item": {
                            "max-width": "100px",
                            "color": "black",
                            "font-size": "14px",
                        },
                        "icon": {"font-size": "0px"},
                    },
                )
                ss.selected_idx = dfs_str.index(selected)

                # Display table
                df = dfs[ss.selected_idx]

                # Check if values in table are in tables of reference extraction
                refvalues = []
                for dfref in asset_dict[pdf_file]["table_extractors"][
                    extractions.index(ref_extraction)
                ]["tables"]:
                    refvalues.extend(dfref.map(reformat_str).to_numpy().flatten())
                mask = df.map(reformat_str).isin(refvalues)

                # Apply font color (green vs red) based on above check
                def color_mask(val: bool) -> None:
                    return f'color: {"green" if val is True else "red"}'

                dfst = df.style.apply(
                    lambda c, mask=mask: mask[c.name].apply(color_mask)
                )

                # Display table with appropriate font color
                column_config = {}
                for col in df.columns:
                    column_config[col] = st.column_config.Column(width="small")

                st.dataframe(
                    dfst,
                    column_config=column_config,
                    use_container_width=False,
                    height=round(35.5 * (len(dfst.index) + 1)),
                )

        # Tab to display PDF
        with tabs[-1]:

            if not ss.pdf_downloaded:
                ss["pdf_downloaded"] = hf_hub_download(
                    repo_id="DataForGood/taxobservatory_data",
                    filename=ss.pdf_selected,
                    repo_type="dataset",
                )

            if ss.pdf_downloaded:
                # Get pages to render
                assets = {}
                pagefilter.FromFilename()(ss.pdf_downloaded, assets=assets)
                pages_to_render = [
                    page + 1 for page in assets["pagefilter"]["selected_pages"]
                ]

                # Render pages from PDF
                pdf_viewer(
                    input=ss.pdf_downloaded,
                    pages_to_render=pages_to_render,
                    width=1000,
                )


if __name__ == "__main__":

    if len(sys.argv) > 1:
        ref_data_file = sys.argv[1]
    else:
        ref_data_file = None

    main(ref_data_file)
