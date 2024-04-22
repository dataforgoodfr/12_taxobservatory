import streamlit as st
from utils import set_algorithm_name, get_pdf_iframe, to_csv_file, update_df_csv_to_save
from menu import display_pages_menu
from country_by_country.utils.constants import JURIDICTIONS
from Levenshtein import distance
import sys
import logging
import pandas as pd
import numpy as np
import re

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def check_last_cell_sum(column):
    last_cell = column.iloc[-2]  # Get the last cell value
    result = [""] * (len(column.tolist()) - 2)
    try:
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
        return column.iloc[:-1].sum()
    except Exception:
        return None


def style_negative(v, props=""):
    try:
        return props if float(v) < 0 else None
    except Exception:
        return None


def convert_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    for column_name in dataframe.columns:
        try:
            dataframe[column_name] = dataframe[column_name].astype(float)
        except Exception:
            pass
    return dataframe


special_characters = "#&()[]@©"


def style_symbol(v, props=""):
    try:
        return props if any(c in special_characters for c in v) else None
    except Exception:
        return None


def style_specific_cells(dataframe: pd.DataFrame, index_list: list):

    color = "background-color: lightgreen"
    df1 = pd.DataFrame("", index=dataframe.index, columns=dataframe.columns)
    for index in index_list:
        df1.iloc[index, 0] = color
    return df1


def most_similar_string(input_string: str) -> str:
    def update_min(string, min_distance, most_similar, input_string=input_string):
        dist = distance(input_string, string)
        if dist < min_distance:
            return dist, string
        else:
            return min_distance, most_similar

    if input_string == None:
        return "None"
    min_distance = float("inf")
    most_similar = None
    for string in JURIDICTIONS.keys():
        # Compute the distance with the juridiction name
        min_distance, most_similar = update_min(string, min_distance, most_similar)
        # Compute the distance with the Alpha-2 code
        min_distance, most_similar = update_min(
            JURIDICTIONS[string]["Alpha-2 code"], min_distance, most_similar
        )
        # Compute the distance with the Alpha-3 code
        min_distance, most_similar = update_min(
            JURIDICTIONS[string]["Alpha-3 code"], min_distance, most_similar
        )
    return most_similar


def validate(data: pd.DataFrame) -> None:
    st.session_state.tables[st.session_state["algorithm_name"]] = data


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
            index=(
                list(st.session_state.tables.keys()).index(
                    st.session_state["algorithm_name"],
                )
                if "algorithm_name" in st.session_state
                else 0
            ),
            on_change=set_algorithm_name,
            args=("selectbox2",),
            key="selectbox2",
        )

        if "algorithm_name" in st.session_state:
            st.session_state["df_csv_to_save"] = to_csv_file(
                st.session_state.tables[st.session_state["algorithm_name"]]
            )
        st.download_button(
            label="📥 Download Current Table",
            data=(
                st.session_state["df_csv_to_save"]
                if "df_csv_to_save" in st.session_state
                else None
            ),
            disabled="df_csv_to_save" not in st.session_state,
            file_name=(
                f"{st.session_state['original_pdf_name']}.csv"
                if "original_pdf_name" in st.session_state
                else "table.csv"
            ),
        )

        st.session_state.tables[st.session_state["algorithm_name"]] = st.data_editor(
            st.session_state.tables[st.session_state["algorithm_name"]],
            num_rows="dynamic",
            on_change=update_df_csv_to_save,
            width=800,
            height=900,
        )

    col7, col8, col9 = st.columns([1, 1, 1])
    with col7:
        total = st.checkbox(
            "Calculate the Total of each columns, excluding the last row", value=True
        )
        country = st.checkbox("Activate the country filter", value=True)

    with col8:
        negativ = st.checkbox(
            "Show the negative numbers, for each columns detected as a numerical type"
        )
    with col9:
        symbol = st.checkbox(
            "Show the cells that contain a special symbol : " + special_characters,
            value=True,
        )
        remove_symbols = st.checkbox("Remove the special symbols")

    dataframe = st.session_state.tables[st.session_state["algorithm_name"]].copy()

    if country:
        dataframe.iloc[:-2, 0] = dataframe.iloc[:-2, 0].apply(
            lambda x: most_similar_string(x)
        )

    if remove_symbols:
        pattern = "\(.*?\)" + "|[" + re.escape(special_characters) + "]"
        for column in dataframe.columns:
            dataframe[column] = dataframe[column].apply(
                lambda x: re.sub(pattern, "", str(x))
            )
        dataframe = convert_dataframe(dataframe)

    if total:
        dataframe = convert_dataframe(dataframe)
        new_row = dataframe.apply(column_sum, axis=0)
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
        dataframe_styler = dataframe_styler.map(
            style_negative,
            props="color:red;",
        )
    if symbol:
        dataframe_styler = dataframe_styler.map(
            style_symbol,
            props="color:red;",
        )

    if country:
        index_list = []
        for index, (val1, val2) in enumerate(
            zip(
                dataframe.iloc[:-1, 0],
                st.session_state.tables[st.session_state["algorithm_name"]].iloc[
                    :-1, 0
                ],
            )
        ):
            if val1 != val2:
                index_list.append(index)
        dataframe_styler = dataframe_styler.apply(
            lambda x: style_specific_cells(x, index_list), axis=None
        )

    st.dataframe(dataframe_styler, use_container_width=True, height=1000)

    st.button(
        "Save the table above",
        on_click=validate,
        args=(dataframe_styler.data,),
    )
