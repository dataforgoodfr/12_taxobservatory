import base64
from pathlib import Path

import streamlit as st


def get_pdf_iframe(pdf_to_process: str) -> str:
    base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}
    " width="800px" height="1000px" type="application/pdf"></iframe>
    """
    return pdf_display


def set_validate(validate: str) -> None:
    st.session_state[validate] = True
