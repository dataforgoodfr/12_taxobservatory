import base64
from pathlib import Path

import pandas as pd
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
    # Populate the columns with the metadata
    df = df.assign(company=st.session_state["metadata"]["company_name"])
    df = df.assign(year=st.session_state["metadata"]["year"])
    df = df.assign(currency=st.session_state["metadata"]["currency"])
    df = df.assign(unit=st.session_state["metadata"]["unit"])
    df = df.assign(headquarter=st.session_state["metadata"]["headquarter"])
    return df.to_csv(index=False).encode("utf-8")


def update_df_csv_to_save() -> None:
    st.session_state["df_csv_to_save"] = to_csv_file(
        st.session_state.tables[st.session_state["algorithm_name"]],
    )
