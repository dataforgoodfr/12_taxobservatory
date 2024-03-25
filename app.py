import base64
import logging
import sys
import tempfile
from pathlib import Path

import streamlit as st
import yaml
from pypdf import PdfReader
from st_aggrid import AgGrid, JsCode

from country_by_country.processor import ReportProcessor
from country_by_country.utils.utils import gather_tables, keep_pages


def get_pdf_iframe(pdf_to_process: str) -> str:
    base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}
    " width="800px" height="1000px" type="application/pdf"></iframe>
    """
    return pdf_display


def apply_filter(column_name: str) -> None:

    if st.session_state.column_name == "is_negative":
        js_code = JsCode(
            """
            function(params) {
                if (params.value > 0) {
                    return {backgroundColor: 'green'}
                } else {
                    return {backgroundColor: 'red'}
                }
            }
            """,
        )

    if st.session_state.column_name == "is_number":
        js_code = JsCode(
            """
            function(params) {
                if (typeof params.value === 'number') {
                    return {backgroundColor: 'green'}
                } else {
                    return {backgroundColor: 'red'}
                }
            }
            """,
        )

    if st.session_state.column_name is not None:
        st.session_state.filters_selected[column_name] = st.session_state.column_name
        add_gridoption(js_code, column_name)
    else:
        del st.session_state.filters_selected[column_name]
        remove_gridoption(column_name)


def add_gridoption(js_code: str, column_name: str) -> None:
    new_column_def = {"headerName": column_name, "cellStyle": js_code}
    # add a new element to columnDefs
    st.session_state.gridOptions["columnDefs"].append(new_column_def)


def remove_gridoption(column_name: str) -> None:
    for column_def in st.session_state.gridOptions["columnDefs"]:
        # check if the column8name exist
        if column_def["headerName"] == column_name:
            # remove the element
            st.session_state.gridOptions["columnDefs"].remove(column_def)
            break


st.set_page_config(layout="wide")
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)

with st.sidebar:
    pdf = st.file_uploader("Upload a pdf document")
    config = st.file_uploader("Upload a config")

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
page_selected = None
first_part = True

placeholder = st.empty()
if pdf is not None and config is not None and first_part is not False:
    mytmpfile.write(pdf.read())
    pdfreader = PdfReader(mytmpfile.name)

    config_checked = yaml.safe_load(config)

    logging.info("Loading config and pdf")
    proc = ReportProcessor(config_checked)

    logging.info("Config and pdf loaded")

    logging.info(f"Processing {mytmpfile.name}")

    assets = {
        "pagefilter": {},
        "text_table_extractors": {},
        "img_table_extractors": {},
    }

    # Filtering the pages
    proc.page_filter(
        mytmpfile.name,
        assets,
    )

    logging.info(f"Assets : {assets}")

    pdf_before_page_validation = keep_pages(
        mytmpfile.name,
        assets["pagefilter"]["selected_pages"],
    )
    mytmpfile.close()

    assets["pagefilter"]["selected_pages"].append("None")

    logging.info(f"Assets : {assets}")

    with placeholder.container():
        page_selected = st.selectbox(
            "Which page of the following pdf contains the table you want to extract ?",
            assets["pagefilter"]["selected_pages"],
            index=None,
            placeholder="Select a page number",
        )

        st.markdown(get_pdf_iframe(pdf_before_page_validation), unsafe_allow_html=True)

        if page_selected == "None":
            number_pages = len(pdfreader.pages)
            page_selected = st.selectbox(
                "Which page of the following pdf contains the table you want to extract ?",
                assets["pagefilter"]["selected_pages"],
                index=None,
                placeholder="Select a page number",
            )

            st.markdown(
                get_pdf_iframe(pdf_before_page_validation),
                unsafe_allow_html=True,
            )

        first_part = False

if page_selected is not None and page_selected != "None":
    placeholder.empty()
    st.session_state.filters_selected = {}
    st.session_state.gridOptions = {
        "columnDefs": [],
    }
    logging.info(f"Page selected : {page_selected}")

    assets["pagefilter"]["selected_pages"] = [page_selected]
    pdf_after_page_validation = keep_pages(
        pdf_before_page_validation,
        assets["pagefilter"]["selected_pages"],
    )

    if "tables" not in st.session_state:
        for img_table_extractor in proc.img_table_extractors:
            img_table_extractor(pdf_after_page_validation, assets)
        tables_extracted_by_name = gather_tables(assets)
        logging.info(f"Table extracted : {tables_extracted_by_name}")

        st.session_state["tables"] = tables_extracted_by_name

    with placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                get_pdf_iframe(pdf_after_page_validation),
                unsafe_allow_html=True,
            )

        with col2:
            algorithm_name = st.selectbox(
                "Choose the extracted table you to see",
                list(st.session_state.tables.keys()),
            )
            edited_df = st.data_editor(
                st.session_state.tables[algorithm_name],
                num_rows="dynamic",
            )
            st.session_state.tables[algorithm_name] = edited_df

    st.markdown("""---""")
    col3, col4 = st.columns(2)
    filter_list = ["is_number", "is_negative"]
    with col3:
        for column_name in list(edited_df.columns.values):
            st.selectbox(
                "Do you want to apply a filter to the column " + column_name,
                filter_list,
                index=None,
                placeholder="Select a filter",
                on_change=apply_filter,
                key=column_name,
                args=(column_name),
            )

    logging.info(f"Grid Options : {st.session_state.gridOptions}")
    logging.info(f"Filters selected : {st.session_state.filters_selected}")

    with col4:
        if st.session_state.filters_selected is False:
            AgGrid(edited_df, editable=True, reload_data=True)
        else:
            AgGrid(
                edited_df,
                editable=True,
                reload_data=True,
                gridOptions=st.session_state.gridOptions,
                allow_unsafe_jscode=True,
            )
