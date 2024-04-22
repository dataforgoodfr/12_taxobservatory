import streamlit as st
from utils import set_algorithm_name, get_pdf_iframe
from menu import display_pages_menu
from country_by_country.utils.constants import JURIDICTIONS, CURRENCIES
from Levenshtein import distance
import sys
import logging
import pandas as pd
import numpy as np
import re

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


st.set_page_config(layout="wide", page_title="Report metadata")
st.title("Country by Country Tax Reporting analysis : Metadata")
st.subheader(
    "This page will allow you to fill in metadata about the report : company name, headquarter, currency, unit, ...",
)
display_pages_menu()

if "pdf_after_page_validation" in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            get_pdf_iframe(st.session_state["pdf_after_page_validation"]),
            unsafe_allow_html=True,
        )
    with col2:
        with st.form("metadata_form"):
            company_name = st.text_input("Company name")
            year = st.text_input("Year")

            currencies = {
                (
                    CURRENCIES[currency]["AlphabeticCode"],
                    CURRENCIES[currency]["Currency"],
                )
                for currency in CURRENCIES
            }
            currencies = sorted(currencies, key=lambda x: x[0])
            currencies = [f"{currency[0]} - {currency[1]}" for currency in currencies]
            currency = st.selectbox("Currency", currencies)
            unit = st.selectbox(
                "Unit",
                ("thousands", "millions", "10 millions", "100 millions", "billions"),
            )
            headquarter = st.selectbox(
                "Headquarter location", list(JURIDICTIONS.keys())
            )
            submitted = st.form_submit_button(
                label="Submit",
            )
            if submitted:
                st.session_state["metadata"] = {
                    "company_name": company_name,
                    "year": year,
                    "currency": currency,
                    "unit": unit,
                    "headquarter": headquarter,
                }
                st.switch_page("pages/2_Merge_Tables.py")
