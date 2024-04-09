import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from utils import set_algorithm_name, get_pdf_iframe
from menu import display_pages_menu

import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


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


st.set_page_config(layout="wide", page_title="Tables customization")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Tables")
st.subheader(
    "This page will allow you to clean the extracted tables",
)
display_pages_menu()

if (
    st.session_state.get("validate_selected_pages", False)
    and "pdf_after_page_validation" in st.session_state
):
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            get_pdf_iframe(st.session_state["pdf_after_page_validation"]),
            unsafe_allow_html=True,
        )

    with col4:
        st.session_state["algorithm_name"] = st.selectbox(
            "Choose the extracted table you want to see",
            list(st.session_state.tables.keys()),
            index=list(st.session_state.tables.keys()).index(
                st.session_state["algorithm_name"],
            )
            if "algorithm_name" in st.session_state
            else 0,
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
            st.session_state.tables[st.session_state["algorithm_name"]],
            num_rows="dynamic",
            width=800,
            height=900,
        )

    if (
        "filters_selected" + "_" + st.session_state["algorithm_name"]
        not in st.session_state
    ):
        st.session_state[
            "filters_selected" + "_" + st.session_state["algorithm_name"]
        ] = {}
        gd = GridOptionsBuilder.from_dataframe(edited_df)
        gd.configure_default_column(editable=True)
        st.session_state[
            "grid_options" + "_" + st.session_state["algorithm_name"]
        ] = gd.build()

    col5, col6 = st.columns([1, 3])
    filter_list = ["is_number", "is_negative"]
    with col5:
        for column_name in list(edited_df.columns.values):
            if (
                column_name
                in st.session_state[
                    "filters_selected" + "_" + st.session_state["algorithm_name"]
                ]
            ):
                index = filter_list.index(
                    st.session_state[
                        "filters_selected" + "_" + st.session_state["algorithm_name"]
                    ][column_name],
                )
            else:
                index = None
            st.selectbox(
                "Do you want to apply a filter to the column " + column_name,
                filter_list,
                index=index,
                placeholder="Select a filter",
                on_change=apply_filter,
                key=column_name + st.session_state["algorithm_name"],
                args=(column_name, st.session_state["algorithm_name"]),
            )
    logging.info(
        f"""Grid Options : {st.session_state["grid_options" + "_" + st.session_state["algorithm_name"]]}""",
    )
    with col6:
        AgGrid(
            edited_df,
            gridOptions=st.session_state[
                "grid_options" + "_" + st.session_state["algorithm_name"]
            ],
            allow_unsafe_jscode=True,
        )
        # There is an open bug here :
        # https://github.com/PablocFonseca/streamlit-aggrid/issues/234
        # currently we cannot use the key and the reload_data option together
