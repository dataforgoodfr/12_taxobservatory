import streamlit as st
import pandas as pd
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

from country_by_country.utils.utils import (
    gather_tables,
    check_if_many,
    filled_table_extractors,
    gather_tables_with_merge,
)
from menu import display_pages_menu
from dotenv import load_dotenv


def merge_table(table_extractor: str) -> None:
    first_df_columns = pd.Series([])
    table_list = []
    for key, table in st.session_state["tables"].items():
        if table_extractor in key:
            if first_df_columns.empty:
                first_df_columns = table.columns
            # Replace column names for all DataFrames in the list
            table.columns = first_df_columns
            table_list.append(table)

    st.session_state["new_tables"] = pd.concat(
        table_list, ignore_index=True, sort=False
    )


def save_merge(table_extractor: str) -> None:
    tables_extracted_by_name = gather_tables_with_merge(
        st.session_state["assets"],
        st.session_state["new_tables"],
        table_extractor,
    )
    st.session_state["tables"] = tables_extracted_by_name
    st.session_state["algorithm_name"] = table_extractor


def remove_table(key: str) -> None:
    del st.session_state["tables"][key]
    if (
        "algorithm_name" in st.session_state
        and st.session_state["algorithm_name"] == key
    ):
        del st.session_state["algorithm_name"]


st.set_page_config(layout="wide", page_title="Merge Tables")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Headers")
st.subheader(
    "This page will allow you to modify the headers and to remove columns",
)
display_pages_menu()
load_dotenv()


if "tables" not in st.session_state:
    st.markdown(
        "# !! Don't change the page while the algorithms are runing, else they will start again"
    )


if (
    st.session_state.get("validate_selected_pages", False)
    and "pdf_after_page_validation" in st.session_state
):
    if "tables" not in st.session_state:
        for table_extractor in st.session_state["proc"].table_extractors:
            new_asset = table_extractor(st.session_state["pdf_after_page_validation"])
            st.session_state["assets"]["table_extractors"].append(new_asset)
        tables_extracted_by_name = gather_tables(st.session_state["assets"])
        logging.info(f"Table extracted : {tables_extracted_by_name}")

        st.session_state["tables"] = tables_extracted_by_name

    if not check_if_many(st.session_state["assets"]):
        st.markdown("# !! Nothing to merge")

        if "first_time_merge" not in st.session_state:
            st.session_state["first_time_merge"] = False
            st.switch_page("pages/4_Clean_Headers.py")

    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        table_extractor = st.selectbox(
            "Choose an algorithm :",
            filled_table_extractors(st.session_state["assets"]),
            args=("selectbox2",),
            key="selectbox2",
        )

        if table_extractor is not None:
            for key, table in st.session_state["tables"].items():
                if table_extractor in key:
                    with st.container(border=True):
                        st.markdown("Table shape :" + str(table.shape))
                        st.markdown("Table name : " + key)
                        st.dataframe(
                            table,
                        )
                        st.button(
                            "Remove this table",
                            type="primary",
                            on_click=remove_table,
                            args=(key,),
                            key=key,
                        )

    with col2:
        st.markdown(
            "You won't be able to merge if the number of columns is not the same for each tables !!"
        )
        merged = st.button(
            "Merge",
            type="primary",
            on_click=merge_table,
            args=(table_extractor,),
        )
        validated = st.button(
            "Sauver le merge",
            on_click=save_merge,
            args=(table_extractor,),
        )
        if validated:
            st.switch_page("pages/4_Clean_Headers.py")

    with col3:
        if merged is True:
            edited_df = st.dataframe(
                st.session_state["new_tables"],
            )
