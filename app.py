import streamlit as st
import logging
import sys
import yaml
from country_by_country.processor import ReportProcessor
from country_by_country.utils.utils import filter_pages,gather_tables 

from pathlib import Path
import tempfile
import base64
from pathlib import Path
from pypdf import PdfReader

def get_pdf_iframe(pdf_to_process):
	base64_pdf = base64.b64encode(Path(pdf_to_process).read_bytes()).decode("utf-8")
	pdf_display = f"""
		<iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
	"""
	return pdf_display

st.set_page_config(layout="wide")
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
st.title("Country by Country Tax Reporting analysis")
st.subheader("This app will help you extract a table containing financial information from a pdf")

with st.sidebar:
	pdf = st.file_uploader("Upload a pdf document")
	config = st.file_uploader("Upload a config") 

mytmpfile = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
page_selected = None
first_part = True

placeholder = st.empty()
if pdf is not None and config is not None and first_part is not False:
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
	proc.page_filter(mytmpfile.name, assets) # TODO : rename to avoid confusion with filter_pages

	logging.info(f"Assets : {assets}")
    
	pdf_before_page_validation = filter_pages(  #TODO : should return the tmp file object, in order to close it + create utils
		mytmpfile.name,
		assets["pagefilter"]["selected_pages"],
    )

	assets["pagefilter"]["selected_pages"].append("None")

	logging.info(f"Assets : {assets}")

	with placeholder.container():
		page_selected = st.selectbox(
			'Which page of the following pdf contains the table you want to extract ?',
			assets["pagefilter"]["selected_pages"],
			index=None,
			placeholder="Select a page number")

		st.markdown(get_pdf_iframe(pdf_before_page_validation), unsafe_allow_html=True)

		if page_selected == "None":
			number_pages = len(pdfreader.pages)
			page_selected = show_pdf_selector(mytmpfile.name, range(0, number_pages))
		
		assets["pagefilter"]["selected_pages"] = [page_selected]
		first_part = False
	

if page_selected is not None and page_selected != "None":
	placeholder.empty()
	
	pdf_after_page_validation = filter_pages(  
		pdf_before_page_validation,
		assets["pagefilter"]["selected_pages"],
    )

	for img_table_extractor in proc.img_table_extractors:
		img_table_extractor(pdf_after_page_validation, assets)

	tables_extracted_by_name = gather_tables(assets)

	logging.info(f"Table extracted : {tables_extracted_by_name}")

	with placeholder.container(): 
		col1, col2 = st.columns(2)
		with col1:
			st.markdown(get_pdf_iframe(pdf_after_page_validation), unsafe_allow_html=True)
		
		with col2:
			algorithm_name = st.selectbox(
				'Choose the extracted table you to see',
				list(tables_extracted_by_name.keys()))	
			st.dataframe(tables_extracted_by_name[algorithm_name])


	mytmpfile.close()