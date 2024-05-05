import base64
import logging
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader
import streamlit as st


def get_pdf_iframe(pdf_to_process: str) -> str:
    base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}
    " width="100%" height="1000px" type="application/pdf"></iframe>
    """
    return pdf_display


def set_algorithm_name(my_key: str) -> None:
    st.session_state["algorithm_name"] = st.session_state[my_key]


@st.cache_data
def to_csv_file(df: pd.DataFrame) -> bytes:
    # Populate the columns with the metadata, if available
    # They may not be available if the user skipped the metadata page
    # by not clicking on Submit
    if "metadata" in st.session_state:
        df = df.assign(company=st.session_state["metadata"]["company_name"])
        df = df.assign(sector=st.session_state["metadata"]["sector"])
        df = df.assign(year=st.session_state["metadata"]["year"])
        df = df.assign(currency=st.session_state["metadata"]["currency"])
        df = df.assign(unit=st.session_state["metadata"]["unit"])
        df = df.assign(headquarter=st.session_state["metadata"]["headquarter"])
    else:
        df = df.assign(company="")
        df = df.assign(sector="")
        df = df.assign(year="")
        df = df.assign(currency="")
        df = df.assign(unit="")
        df = df.assign(headquarter="")

    return df.to_csv(index=False).encode("utf-8")

def set_state(key: Any, value: Any) -> None:
    """
    Sets the session_state[key] to value.
    key can be a list to reach nested values.
    Ex: ["key1", "key2"] to reach session_state["key1"]["key2"] value.
    """
    if isinstance(key, list):
        key_list = key
        nested_key_string = "session_state"
        nested_value = st.session_state
        for k in key_list[:-1]:
            try:
                nested_key_string += f"['{k}']"
                nested_value = nested_value[k]
            except KeyError as e:
                raise KeyError(f"{nested_key_string} does not exist") from e
        nested_value[key_list[-1]] = value
    else:
        st.session_state[key] = value

def generate_assets() -> None:
    assets = {
        "pagefilter": {},
        "table_extractors": [],
    }

    # Filtering the pages
    st.session_state["proc"].page_filter(
        st.session_state["working_file_pdf"].name,
        assets,
    )

    logging.info(f"Assets : {assets}")

    if len(assets["pagefilter"]["selected_pages"]) == 0:
        # No page has been automatically selected by the page filter
        # Hence, we display the full pdf, letting the user select the pages
        number_pages = len(PdfReader(st.session_state["working_file_pdf"]).pages)
        assets["pagefilter"]["selected_pages"] = list(range(number_pages))
    st.session_state["assets"] = assets