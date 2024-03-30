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
import datetime
import glob
import io
import logging
import pickle
import sys
import tempfile
from pathlib import Path

import pdfkit
import yaml
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter

# Local imports
from country_by_country import processor


def add_page(asset: dict, table_idx: int, writer: object) -> None:
    # Create temporary file to store content of each page
    with tempfile.NamedTemporaryFile(
        suffix=".html",
        mode="w",
        encoding="utf-8",
        delete=False,
    ) as f:
        # Add any detected tables
        f.writelines('<meta charset="UTF-8">')
        html_header_start = f"<h3>{asset['type']} {asset['params']} - "
        if table_idx is None:
            f.writelines(html_header_start + "no table</h3>")
        else:
            f.writelines(
                html_header_start + f"table {table_idx+1}/{len(asset['tables'])}</h3>",
            )
            f.write(asset["tables"][table_idx].to_html(index=False))

    # Load file content into byte stream
    stream = io.BytesIO()
    stream.write(pdfkit.from_file(f.name, False))

    # Create page from byte stream
    writer.add_page(PdfReader(stream).pages[0])


def save_to_pdf(assets: dict, output_file: str) -> None:
    # Initialize PDF writer
    writer = PdfWriter()

    # Iterate through all the assets
    for asset in assets["table_extractors"]:
        if len(asset["tables"]) > 0:
            # If tables, create one table per page
            for table_idx, _df in enumerate(asset["tables"]):
                add_page(asset, table_idx, writer)
        else:
            # If no table, create page with header only
            add_page(asset, None, writer)

    # Write pages to PDF
    writer.write(output_file)


def run_extractions(
    config: dict,
    pdf_files: list[str],
    output_folder: Path,
) -> list[list[dict]]:
    # Initialize processor
    report_processor = processor.ReportProcessor(config)

    # Process each PDF file
    all_assets = []
    for pdf_file in pdf_files:
        print("\n\n\n")
        logging.info(f"Processing {pdf_file}")
        assets = report_processor.process(pdf_file)
        all_assets.append((Path(pdf_file).name, assets))

        # Save extracted tables in new PDF file
        output_file = output_folder / (Path(pdf_file).stem + "_parsed.pdf")
        save_to_pdf(assets, output_file)
        logging.info(f"Saved to {output_file}")

    # Return extracted tables for further processing
    return all_assets


NUMBER_OF_ARGS = 4

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    if len(sys.argv) != NUMBER_OF_ARGS:
        print(
            "Usage: python eval_table_extraction.py <config_file> <pdf_folder> <output_folder>",
        )
        sys.exit(-1)

    CONFIG_FILE = sys.argv[1]
    PDF_FOLDER = sys.argv[2]
    OUTPUT_FOLDER = Path(sys.argv[3])

    # PDF files to parse
    pdf_files = list(glob.glob(PDF_FOLDER + "*.pdf"))

    # Create output folder
    path = Path(OUTPUT_FOLDER)
    path.mkdir(parents=True, exist_ok=True)

    # Load config file
    with Path(CONFIG_FILE).open() as stream:
        try:
            config = yaml.safe_load(stream)
        except Exception as e:
            print(e)

    # Run extractions
    eval_assets = run_extractions(
        config=config,
        pdf_files=pdf_files,
        output_folder=OUTPUT_FOLDER,
    )

    # Save all assets to disk
    cur_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "eval/eval_" + str(cur_datetime) + ".pkl"

    with Path(filename).open("wb") as fh:
        pickle.dump(eval_assets, fh)
    logging.info(
        "Assets dumped in assets.pkl. You can read then using : \n"
        + f"pickle.load(open({filename}, 'rb'))",
    )
