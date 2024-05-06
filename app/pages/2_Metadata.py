import streamlit as st
from utils import set_algorithm_name, get_pdf_iframe
from menu import display_pages_menu
from country_by_country.utils.constants import (
    JURIDICTIONS,
    CURRENCIES,
    SECTORS,
    COMPANIES,
)
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
            if "metadata" in st.session_state:
                company_name = st.session_state["metadata"]["company_name"]
                sector = st.session_state["metadata"]["sector"]
                year = st.session_state["metadata"]["year"]
                currency = st.session_state["metadata"]["currency"]
                unit = st.session_state["metadata"]["unit"]
                headquarter = st.session_state["metadata"]["headquarter"]
                decimal_separator = st.session_state["metadata"]["separator"]
            else:
                company_name = None
                sector = None
                year = ""
                currency = None
                unit = None
                headquarter = ""
                decimal_separator = ","

            separator_list = [",", "."]
            decimal_separator = st.selectbox(
                "Decimal separator",
                separator_list,
                index=separator_list.index(decimal_separator),
            )

            companies = list(COMPANIES.keys())
            company_name = st.selectbox(
                "Company name",
                companies,
                index=companies.index(company_name) if company_name else 0,
            )

            sector = st.selectbox(
                "Sector", SECTORS, index=SECTORS.index(sector) if sector else 0
            )

            year = st.text_input("Year", value=year)

            currencies = {
                (
                    CURRENCIES[currency]["AlphabeticCode"],
                    CURRENCIES[currency]["Currency"],
                )
                for currency in CURRENCIES
            }
            currencies = sorted(currencies, key=lambda x: x[0])
            currencies = [f"{currency[0]} - {currency[1]}" for currency in currencies]
            currency = st.selectbox(
                "Currency",
                currencies,
                index=currencies.index(currency)
                if currency
                else currencies.index("EUR - Euro"),
            )

            units = [
                "units",
                "thousands",
                "millions",
                "10 millions",
                "100 millions",
                "billions",
            ]
            unit = st.selectbox("Unit", units, index=units.index(unit) if unit else 0)

            headquarters = list(JURIDICTIONS.keys())
            headquarter = st.selectbox(
                "Headquarter location",
                headquarters,
                index=headquarters.index(headquarter) if headquarter else 0,
            )

            submitted = st.form_submit_button(
                label="Submit",
            )
            if submitted:
                st.session_state["metadata"] = {
                    "separator": decimal_separator,
                    "company_name": company_name,
                    "sector": sector,
                    "year": year,
                    "currency": currency,
                    "unit": unit,
                    "headquarter": headquarter,
                }
                st.switch_page("pages/3_Merge_Tables.py")
