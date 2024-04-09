import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from utils import set_algorithm_name, get_pdf_iframe

import sys
import logging
import pandas as pd
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def apply_filter(column_name: str, algorithm_name: str) -> None:

    if st.session_state[column_name + algorithm_name] is not None:
        st.session_state["filters_selected" + "_" + algorithm_name][
            column_name
        ] = st.session_state[column_name + algorithm_name]
        # update_gridoption_cellstyle(column_name, js_code, algorithm_name)
    else:
        del st.session_state["filters_selected" + "_" + algorithm_name][column_name]
        # remove_gridoption_cellstyle(column_name, algorithm_name)


def check_last_cell_sum(column):
    last_cell = column.iloc[-2]  # Get the last cell value
    result = [""] * (len(column.tolist()) - 2)

    try:
        column = column.astype(float)
        sum_except_last = column.iloc[
            :-2
        ].sum()  # Calculate the sum of all values except the last one
        result.append(
            "background-color: red"
            if float(last_cell) != sum_except_last
            else "background-color: green"
        )
        result.append("")
        return result
    except Exception:
        result.append("background-color: red")
        result.append("")
        return result


def column_sum(column):
    try:
        column = column.astype(float)
        return column.iloc[:-1].sum()
    except Exception:
        return None


def style_negative(v, props=""):
    try:
        return props if float(v) < 0 else None
    except Exception:
        return None


special_characters = "#&()[]@"


def style_symbol(v, props=""):
    try:
        return props if any(c in special_characters for c in v) else None
    except Exception:
        return None


st.set_page_config(layout="wide")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Tables")
st.subheader(
    "This page will allow you to clean the extracted tables",
)

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

    with col6:
        col7, col8, col9 = st.columns([1, 1, 1])
        with col7:
            total = st.checkbox(
                "Calculate the Total of each columns, excluding the last row"
            )
        with col8:
            negativ = st.checkbox(
                "Show the negative numbers, for each columns detected as a numerical type"
            )
        with col9:
            symbol = st.checkbox(
                "Show the cells that contain a special symbol : " + special_characters
            )

        if total or negativ or symbol:
            dataframe = edited_df
            new_row = edited_df.apply(column_sum, axis=0)
            new_row.iloc[0] = "Total Calculated"
            dataframe.loc[-1] = new_row.transpose()
            dataframe_styler = dataframe.style
            if total:
                dataframe_styler = dataframe_styler.apply(
                    check_last_cell_sum,
                    subset=pd.IndexSlice[:, dataframe.columns[1:]],
                    axis=0,
                )
            if negativ:
                numeric_columns = edited_df.select_dtypes(include=np.number).columns
                dataframe_styler = dataframe_styler.map(
                    style_negative,
                    props="color:red;",
                )
            if symbol:
                dataframe_styler = dataframe_styler.map(
                    style_symbol,
                    props="color:red;",
                )
            st.dataframe(dataframe_styler, use_container_width=True, height=1000)
        else:
            st.dataframe(edited_df, use_container_width=True, height=1000)
