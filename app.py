import streamlit as st
import logging
import sys
import yaml
from country_by_country.processor import ReportProcessor
from country_by_country.pagefilter.filter_pages import filter_pages

from pathlib import Path
import tempfile
import base64
from pathlib import Path
from pypdf import PdfReader

def show_pdf_selector(pdf_to_process, list_pages):
	base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
	pdf_display = f"""
		<iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
	"""

	page_selected = st.selectbox(
		'Which page of the following pdf contains the table you want to extract ?',
		list_pages,
		placeholder="Select a page number")

	st.markdown(pdf_display, unsafe_allow_html=True)
	return page_selected




logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
st.title("Country by Country Tax Reporting analysis")
st.subheader("This app will help you extract a table containing financial information from a pdf")

with st.sidebar:
	pdf = st.file_uploader("Upload a pdf document")
	config = st.file_uploader("Upload a config") #give the possibility to have a default config

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)



if pdf is not None and config is not None:
	mytmpfile.write(pdf.read())
	pdfreader = PdfReader(mytmpfile.name)

	config_checked = yaml.safe_load(config)

	logging.info(f"Loading config and pdf")
	proc = ReportProcessor(config_checked)

	logging.info(f"Config and pdf loaded")

	logging.info(f"Processing {mytmpfile.name}")

	assets = {
		"pagefilter": {},
		"text_table_extractors": {},
		"img_table_extractors": {},
	}

	# Filtering the pages
	proc.page_filter(mytmpfile.name, assets)

	logging.info(f"Assets : {assets}")
    
	pdf_to_process = filter_pages(  #TODO : should return the tmp file object, in order to close it + create utils
		mytmpfile.name,
		assets["pagefilter"]["selected_pages"],
    )

	assets["pagefilter"]["selected_pages"].append("None")
	page_selected = show_pdf_selector(pdf_to_process, assets)

	if page_selected == "None":
		number_pgages = len(pdfreader.pages)
		page_selected = show_pdf_selector(mytmpfile.name, range(0, number_pgages-1))

	mytmpfile.close()