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
import base64
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
from utils import (
    append_count_to_duplicates,
    clean_headers,
    convert_to_str,
    reformat_str,
)

from country_by_country import pagefilter
from country_by_country.utils.utils import keep_pages


def download_pdf() -> None:
    pdf_file = ss.pdf_selected.replace("'", "_")
    try:
        ss.pdf_downloaded = hf_hub_download(
            repo_id="DataForGood/taxobservatory_data",
            filename=f"pdf/{pdf_file}",
            repo_type="dataset",
        )
    except Exception:
        st.error("Couldn't download PDF: " + pdf_file)


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
        except Exception as e:
            msg = "REF data file not specified." if ref_data_file is None else e
            st.warning(
                f"REF data file not loaded. Continue without or fix the below error.\n\n{msg}",
            )
            ss.ref_uploaded = None

    # Display title
    st.title(
        "Table extraction benchmark",
        help="""Drag and drop a pickle file containg evaluation results, select a PDF to see
        the corresponding extracted tables and start comparing. Cells in the tables are
        colored **:green[in green]** if they are present in the tables of the reference
        extraction, and **:red[red]** otherwise. Note that the color only indicates if one
        extracted value is present in the reference extraction, not if that value is at the
        right location in the table. Change the reference extraction via the select box in the
        left sidebar.""",
    )

    # Display sidebar
    pdf_file = None
    with st.sidebar:
        # Select pickle containing results
        uploaded_file = st.file_uploader(
            "Select a pickle file to load evaluations results",
            type="pkl",
            help="""Run _eval_table_extraction.py_ to generate a picke file containing
            extracted tables for multiple PDFs""",
        )

        if uploaded_file:
            # Load pickle
            assets = pickle.load(uploaded_file)

            # List PDFs and their extracted assets
            asset_dict = {Path(asset[0]).name: asset[1] for asset in assets}

            # Select PDF to load results
            pdf_file = st.selectbox(
                "Select a PDF file",
                sorted(asset_dict.keys()),
                on_change=download_pdf,
                key="pdf_selected",
                help="""The corresponding extracted tables will be displayed (both REF and
                extractions from the picke file)""",
            )

    # Display tabs containing PDF and extracted tables
    if pdf_file is not None:
        process_pdf(pdf_file, asset_dict)


def append_ref_data(pdf_file: str, asset_dict: dict) -> None:
    company = pdf_file.split("_")[0]
    year = pdf_file.split("_")[1]
    cols = [2, *list(range(5, 10)), *list(range(15, 18))]
    ref_df = (
        ss.ref_uploaded.query(f'company=="{company}" and year=={year}')
        .iloc[:, cols]
        .reset_index(drop=True)
        .dropna(axis="columns", how="all")
    )
    asset_dict[pdf_file]["table_extractors"].insert(
        0,
        {
            "type": "REF",
            "params": {"src_file": ref_data_file},
            "tables": [ref_df],
        },
    )


def select_table(key: str) -> None:
    selected = ss[key]
    ss.selected_idx = int(selected.split(" ", 1)[1])


def process_pdf(pdf_file: str, asset_dict: dict) -> None:
    # Append REF data to extractions in assets
    if ss.ref_uploaded is not None:
        append_ref_data(pdf_file, asset_dict)

    # List all the extraction names including REF
    extractions = append_count_to_duplicates(
        [extractor["type"] for extractor in asset_dict[pdf_file]["table_extractors"]],
    )

    # Select reference extraction for comparison (default to REF data)
    with st.sidebar:
        try:
            ref_idx = extractions.index("REF")
        except Exception:
            ref_idx = 0
        ref_extraction = st.selectbox(
            "Select reference extraction for comparison",
            extractions,
            index=ref_idx,
        )
        if ref_extraction is not None:
            ss.ref_extraction = ref_extraction

    # Display tabs (one to display PDF + one per extraction)
    tabs = st.tabs(["PDF", *extractions])

    # Tab to display PDF
    with tabs[0]:
        if not ss.pdf_downloaded:
            download_pdf()

        if ss.pdf_downloaded:
            # Get pages to render
            assets = {}
            pagefilter.FromFilename()(ss.pdf_downloaded, assets=assets)
            pages_to_render = list(assets["pagefilter"]["selected_pages"])

            # Filter pages from PDF
            pdf_fitered = keep_pages(ss.pdf_downloaded, pages_to_render)

            # Get content of pages
            with Path(pdf_fitered).open("rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")

            # Embed content in HTML
            pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}"
            width="800" height="1000" type="application/pdf"></iframe>"""

            # Display content
            st.markdown(pdf_display, unsafe_allow_html=True)

    # Tabs to display extractions
    for idx, tab in enumerate(tabs[1:]):
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
            if len(dfs_str) == 0:
                st.info("No table extracted.")
            else:
                selected = option_menu(
                    None,
                    dfs_str,
                    menu_icon=None,
                    icons=None,
                    manual_select=min(ss.selected_idx, len(dfs_str) - 1),
                    orientation="horizontal",
                    key="tab_" + str(idx),
                    on_change=select_table,
                    styles={
                        "container": {
                            "padding": "0!important",
                            "margin": "0!important",
                            "background-color": "#EFF2F6",
                        },
                        "nav-item": {
                            "max-width": "100px",
                            "color": "black",
                            "font-size": "14px",
                        },
                        "icon": {"font-size": "0px"},
                    },
                )
                selected_idx = dfs_str.index(selected) if selected in dfs_str else 0

                # Pull selected table
                df = dfs[selected_idx]

                # Clean headers to prevent any st.dataframe error
                clean_headers(df)

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
                    lambda c, mask=mask: mask[c.name].apply(color_mask),
                )

                # Display table with appropriate font color
                column_config = {}
                for col in df.columns:
                    column_config[col] = st.column_config.Column(width="small")

                try:
                    st.dataframe(
                        dfst,
                        column_config=column_config,
                        use_container_width=False,
                        height=round(35.5 * (len(dfst.index) + 1)),
                    )
                except Exception as error:
                    st.error(error)


if __name__ == "__main__":

    ref_data_file = sys.argv[1] if len(sys.argv) > 1 else None

    main(ref_data_file)
