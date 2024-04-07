import base64
import logging
import sys
import tempfile
from pathlib import Path

import streamlit as st
import yaml
from pypdf import PdfReader
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

from country_by_country.processor import ReportProcessor
from country_by_country.utils.utils import gather_tables, keep_pages, displayed_pages


def get_pdf_iframe(pdf_to_process: str, title:str | None = None, metadata: dict | None = None) -> str:
    base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
    title_tag = f"<b>{title}</b><br>" if title else ""
    metadata_tag = ""
    if metadata:
        for k, v in metadata.items():
            metadata_tag += f"{k}: {v}<br>"        
    pdf_display = f"""
    {title_tag}
    {metadata_tag}
    <iframe src="data:application/pdf;base64,{base64_pdf}
    " width="100%" height="1000px" type="application/pdf"></iframe>
    """
    return pdf_display


def apply_filter(column_name: str, algorithm_name: str) -> None:

    if st.session_state[column_name + algorithm_name] == "is_negative":
        js_code = JsCode(
            """
            function(params) {
                if (params.value > 0) {
                    return {backgroundColor: '#abf7b1'}
                } else {
                    return {backgroundColor: '#fcccbb'}
                }
            }
            """,
        )

    if st.session_state[column_name + algorithm_name] == "is_number":
        js_code = JsCode(
            """
            function(params) {
                if (/[^a-zA-Z0-9]/.test(params.value))
                {
                    return {backgroundColor: '#fcccbb'}
                }
                else
                {
                    return {backgroundColor: '#abf7b1'}
                }
            };
            """,
        )

    if st.session_state[column_name + algorithm_name] is not None:
        st.session_state["filters_selected" + "_" + algorithm_name][
            column_name
        ] = st.session_state[column_name + algorithm_name]
        update_gridoption_cellstyle(column_name, js_code, algorithm_name)
    else:
        del st.session_state["filters_selected" + "_" + algorithm_name][column_name]
        remove_gridoption_cellstyle(column_name, algorithm_name)


def update_gridoption_cellstyle(
    header_name: str,
    js_code: str,
    algorithm_name: str,
) -> None:
    # Find the index of the column definition corresponding to the headerName
    for i, column_def in enumerate(
        st.session_state["grid_options" + "_" + algorithm_name]["columnDefs"],
    ):
        if column_def["headerName"] == header_name:
            # Update the cellStyle for the found column definition
            st.session_state["grid_options" + "_" + algorithm_name]["columnDefs"][i][
                "cellStyle"
            ] = js_code
            break


def remove_gridoption_cellstyle(header_name: str, algorithm_name: str) -> None:
    # Find the column definition corresponding to the headerName
    for column_def in st.session_state["grid_options" + "_" + algorithm_name][
        "columnDefs"
    ]:
        if column_def["headerName"] == header_name:
            # Check if cellStyle exists, and remove it if it does
            if "cellStyle" in column_def:
                del column_def["cellStyle"]
            break


def set_validate(validate: str) -> None:
    st.session_state[validate] = True


keep = "keep the extracted value"
remove = "remove this column"


def set_headers(algorithm_name: str) -> None:
    for header in st.session_state.tables[algorithm_name].columns.values.tolist():
        if st.session_state["widget" + header] == remove:
            st.session_state.tables[algorithm_name].drop(columns=[header], inplace=True)
        if st.session_state["widget" + header] == keep:
            pass
        else:
            st.session_state.tables[algorithm_name].rename(
                columns={header: st.session_state["widget" + header]},
                inplace=True,
            )


header_list = [
    keep,
    "jurisdiction",
    "profit_before_tax",
    "tax_accrued",
    "tax_paid",
    "employees",
    "unrelated_revenues",
    "related_revenues",
    "stated_capital",
    "accumulated_earnings",
    "tangible_assets",
    "total_revenues",
    remove,
]


def set_algorithm_name(my_key: str) -> None:
    st.session_state["algorithm_name"] = st.session_state[my_key]


st.set_page_config(layout="wide")
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
st.title("Country by Country Tax Reporting analysis")
st.subheader(
    "This app will help you extract a table containing financial information from a pdf",
)

with st.sidebar:
    original_pdf = st.file_uploader("Upload a pdf document containing financial table : ")
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
        config = yaml.safe_load(yaml_config)
    else:
        config = yaml.safe_load(loaded_config)
    yaml_str = yaml.dump(config, default_flow_style=False, indent=2)
    # Ajouter des backticks triples pour créer un bloc de code markdown
    markdown_str = f"The configuration is : \n\n```\n{yaml_str}\n```"
    st.write(markdown_str)

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
placeholder = st.empty()
selected_pages_index = []

if original_pdf is not None and config is not None:
    mytmpfile.write(original_pdf.read())
    pdfreader = PdfReader(mytmpfile.name)

    logging.info("Loading config and pdf")
    proc = ReportProcessor(config)

    logging.info("Config and pdf loaded")

    logging.info(f"Processing {mytmpfile.name}")

    assets = {
        "pagefilter": {},
        "table_extractors": [],
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

    logging.info(f"Assets : {assets}")

    with placeholder.container():
        col1, col2 = st.columns([1, 1])
        displayed_processed_pages = displayed_pages(assets["pagefilter"]["selected_pages"])
        with col1:
            st.markdown(
                get_pdf_iframe(pdf_before_page_validation, title=original_pdf.name, metadata={"Pages with tax data detected": displayed_processed_pages}),
                unsafe_allow_html=True,
            )

        with col2, st.form(key="selected_pages_form"):
            number_pages = (
                len(PdfReader(pdf_before_page_validation).pages) + 1
            )  # Make the index start to 1
            selected_pages_index = st.multiselect(
                "Which page of the following pdf contains the table you want to extract ?",
                list(range(1, number_pages)),
                placeholder="Select a page number",
            )
            submitted = st.form_submit_button(
                label="Validate your selected pages",
                on_click=set_validate,
                args=("validate_selected_pages",),
            )

        if selected_pages_index == ["None"]:  # TODO : check this behavior
            number_pages = len(pdfreader.pages)
            selected_pages_index = st.multiselect(
                "Which page of the following pdf contains the table you want to extract ?",
                [int(d) for d in number_pages],
                placeholder="Select a page number",
            )

            st.markdown(
                get_pdf_iframe(pdf_before_page_validation, title=original_pdf.name),
                unsafe_allow_html=True,
            )

        displayed_selected_pages = [assets["pagefilter"]["selected_pages"][i] for i in selected_pages_index]
        assets["pagefilter"]["selected_pages"] = selected_pages_index
        logging.info(f"Page selected : {selected_pages_index}")

        pdf_after_page_validation = keep_pages(
            pdf_before_page_validation,
            [item - 1 for item in assets["pagefilter"]["selected_pages"]],
        )


if (
    "validate_selected_pages" in st.session_state
    and st.session_state["validate_selected_pages"] is True
    and original_pdf is not None
):
    placeholder.empty()

    if "tables" not in st.session_state:
        for table_extractor in proc.table_extractors:
            new_asset = table_extractor(pdf_after_page_validation)
            assets["table_extractors"].append(new_asset)
        tables_extracted_by_name = gather_tables(assets)
        logging.info(f"Table extracted : {tables_extracted_by_name}")

        st.session_state["tables"] = tables_extracted_by_name

    with placeholder.container():
        col1, col2 = st.columns(2)
        pdf_iframe_after_page_validation = get_pdf_iframe(pdf_after_page_validation, title=original_pdf.name, metadata={"Selected pages": displayed_selected_pages})
        with col1:
            st.markdown(
                pdf_iframe_after_page_validation,
                unsafe_allow_html=True,
            )
        with col2:
            algorithm_name_tmp = st.selectbox(
                "Choose the extracted table you want to see",
                list(st.session_state.tables.keys()),
                on_change=set_algorithm_name,
                args=("selectbox1",),
                key="selectbox1",
            )

            algorithm_name = (
                st.session_state["algorithm_name"]
                if "algorithm_name" in st.session_state
                else algorithm_name_tmp
            )

            with st.form(key="my_form"):
                for header in st.session_state.tables[
                    algorithm_name
                ].columns.values.tolist():
                    st.selectbox(
                        "Choose the value of the following extracted header : "
                        + str(header),
                        header_list,
                        key="widget" + str(header),
                    )
                submitted = st.form_submit_button(
                    label="Submit",
                    on_click=set_headers,
                    args=(algorithm_name,),
                )
                if submitted:
                    set_validate("validate_headers")

if (
    "validate_headers" in st.session_state
    and st.session_state["validate_headers"] is True
    and original_pdf is not None
):
    placeholder.empty()

    with placeholder.container():
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                pdf_iframe_after_page_validation,
                unsafe_allow_html=True,
            )

        with col4:
            st.selectbox(
                "Choose the extracted table you want to see",
                list(st.session_state.tables.keys()),
                index=list(st.session_state.tables.keys()).index(
                    st.session_state["algorithm_name"],
                ),
                on_change=set_algorithm_name,
                args=("selectbox2",),
                key="selectbox2",
            )
            # if (
            #    "aggrid_" + algorithm_name in st.session_state
            #    and st.session_state["aggrid_" + algorithm_name] is not None
            # ):
            #    st.session_state.tables[algorithm_name] = pd.DataFrame(

            edited_df = st.data_editor(
                st.session_state.tables[algorithm_name],
                num_rows="dynamic",
                width=800,
                height=900,
            )

        if "filters_selected" + "_" + algorithm_name not in st.session_state:
            st.session_state["filters_selected" + "_" + algorithm_name] = {}
            gd = GridOptionsBuilder.from_dataframe(edited_df)
            gd.configure_default_column(editable=True)
            st.session_state["grid_options" + "_" + algorithm_name] = gd.build()

        col5, col6 = st.columns([1, 3])
        filter_list = ["is_number", "is_negative"]
        logging.info(f"Algorithm_name : {algorithm_name}")
        with col5:
            for column_name in list(edited_df.columns.values):
                if (
                    column_name
                    in st.session_state["filters_selected" + "_" + algorithm_name]
                ):
                    index = filter_list.index(
                        st.session_state["filters_selected" + "_" + algorithm_name][
                            column_name
                        ],
                    )
                else:
                    index = None
                st.selectbox(
                    "Do you want to apply a filter to the column " + column_name,
                    filter_list,
                    index=index,
                    placeholder="Select a filter",
                    on_change=apply_filter,
                    key=column_name + algorithm_name,
                    args=(column_name, algorithm_name),
                )
        logging.info(
            f"""Grid Options : {st.session_state["grid_options" + "_" + algorithm_name]}""",
        )
        with col6:
            AgGrid(
                edited_df,
                gridOptions=st.session_state["grid_options" + "_" + algorithm_name],
                allow_unsafe_jscode=True,
            )
            # There is an open bug here :
            # https://github.com/PablocFonseca/streamlit-aggrid/issues/234
            # currently we cannot use the key and the reload_data option together
