import base64
from pathlib import Path
from io import BytesIO
import gzip

import streamlit as st


def get_pdf_iframe(pdf_to_process: str) -> str:
    base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}
    " width="800px" height="1000px" type="application/pdf"></iframe>
    """
    return pdf_display


def set_algorithm_name(my_key: str) -> None:
    st.session_state["algorithm_name"] = st.session_state[my_key]


def to_csv_file(df):
    output = BytesIO()
    with gzip.open(output, "wt") as f:
        df.to_csv(f, index=False)
    processed_data = output.getvalue()
    return processed_data


def update_df_csv_to_save() -> None:
    st.session_state["df_csv_to_save"] = to_csv_file(
        st.session_state.tables[st.session_state["algorithm_name"]]
    )
