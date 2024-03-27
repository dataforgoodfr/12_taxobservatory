# MIT License
#
# Copyright (c) 2024 dataforgood
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# External imports
import logging
import yaml
from pypdf import PdfReader, PdfWriter
import tempfile
import pdfkit
import io
from dotenv import load_dotenv
from typing import List
from pathlib import Path

# Local imports
from country_by_country import processor

PDF_FILES = [
    "Acciona_2020_CbCR_1.pdf",
    "Acerinox_2020_CbCR_1.pdf",
    "ACS_2021_CbCR_2-3.pdf",
    "ENI_2018_CbCR_12-13.pdf",
]

INPUT_FOLDER = "../example_set/inputs/"
OUTPUT_FOLDER = "../example_set/extractions/"
CONFIG_FILE = "./configs/eval_table_extraction.yaml"


def add_page(asset: dict, table_idx: int, writer):
    # Create temporary file to store content of each page
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        # Add header
        f.writelines('<meta charset="UTF-8">')
       
        # Add any detected tables
        if table_idx==None:
            f.writelines(f"<h3>{asset['type']} {asset['params']} - no table</h3>")
        else:
            f.writelines(f"<h3>{asset['type']} {asset['params']} - table {table_idx+1}/{len(asset['tables'])}</h3>")
            f.write(asset['tables'][table_idx].to_html(index=False))
    
    # Load file content into byte stream
    stream = io.BytesIO()
    stream.write(pdfkit.from_file(f.name, False))
    
    # Create page from byte stream
    writer.add_page(PdfReader(stream).pages[0])


def save_to_pdf(assets: dict, output_file: str) -> str:
    # Initialize PDF writer
    writer = PdfWriter()

    # Iterate through all the assets
    for asset in assets["table_extractors"]:
        if len(asset["tables"]) > 0:
            # If tables, create one table per page
            for table_idx, df in enumerate(asset["tables"]):
                add_page(asset, table_idx, writer)
        else:
            # If no table, create page with header only
            add_page(asset, None, writer)

    # Write pages to PDF
    writer.write(output_file)


def run_extractions(config: dict, pdf_files: List[str], output_folder: str) -> List[List[dict]]:
    # Initialize processor
    report_processor = processor.ReportProcessor(config)

    # Process each PDF file
    all_assets = []
    for pdf_file in pdf_files:
        assets = report_processor.process(pdf_file)
        all_assets.append(assets)

        # Save extracted tables in new PDF file
        output_file = output_folder + Path(pdf_file).stem + "_parsed.pdf"
        save_to_pdf(assets, output_file)

    # Return extracted tables for further processing
    return all_assets


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    # PDF files to parse
    pdf_files=[INPUT_FOLDER + pdf_file for pdf_file in PDF_FILES]

    # Create output folder
    path = Path(OUTPUT_FOLDER)
    path.mkdir(parents=True, exist_ok=True)

    # Load config file
    with open(CONFIG_FILE) as stream:
        try:
            config = yaml.safe_load(stream)
        except Exception as e:
            print(e)

    # Run extractions
    assets = run_extractions(
        config=config,
        pdf_files=pdf_files,
        output_folder=OUTPUT_FOLDER
    )
