from menu import display_pages_menu
import streamlit as st
from utils import set_algorithm_name, get_pdf_iframe

import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

keep = "keep the extracted value"
remove = "remove this column"


def transpose_current_table():
    st.session_state.tables[
        st.session_state["algorithm_name"]
    ] = st.session_state.tables[st.session_state["algorithm_name"]].transpose()


def set_headers(algorithm_name: str) -> None:
    for header in st.session_state.tables[algorithm_name].columns.values.tolist():
        if st.session_state["widget" + str(header)] == remove:
            st.session_state.tables[algorithm_name].drop(columns=[header], inplace=True)
        if st.session_state["widget" + str(header)] == keep:
            pass
        else:
            st.session_state.tables[algorithm_name].rename(
                columns={header: st.session_state["widget" + str(header)]},
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

st.set_page_config(layout="wide")  # page_icon="📈"
st.title("Country by Country Tax Reporting analysis : Headers")
st.subheader(
    "This page will allow you to modify the headers and to remove columns",
)
display_pages_menu()

if "tables" not in st.session_state:
    st.markdown(
        "# !! Don't change the page while the algorithms are runing, else they will start again"
    )

if (
    st.session_state.get("validate_selected_pages", False)
    and "pdf_after_page_validation" in st.session_state
):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            get_pdf_iframe(st.session_state["pdf_after_page_validation"]),
            unsafe_allow_html=True,
        )
    with col2:
        index = (
            list(st.session_state.tables.keys()).index(
                st.session_state["algorithm_name"],
            )
            if "algorithm_name" in st.session_state
            else 0
        )

        st.session_state["algorithm_name"] = st.selectbox(
            "Choose the extracted table you want to see",
            list(st.session_state.tables.keys()),
            index=index,
            on_change=set_algorithm_name,
            args=("selectbox1",),
            key="selectbox1",
        )
        st.markdown(
            "Table shape :"
            + str(st.session_state.tables[st.session_state["algorithm_name"]].shape)
        )

        st.button("Transpose table", on_click=transpose_current_table)

        with st.form(key="my_form"):
            for header in st.session_state.tables[
                st.session_state["algorithm_name"]
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
                args=(st.session_state["algorithm_name"],),
            )

            if submitted:
                st.switch_page("pages/5_Clean_Tables.py")

    st.markdown("# Current extraction")
    st.markdown("The extracted table is displaye below")
    st.dataframe(
        st.session_state.tables[st.session_state["algorithm_name"]],
        width=900,
        height=900,
    )
