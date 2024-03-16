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

"""
In this script, we evaluate the quality of the automatic information
extraction from the reports. We expect a data directory to be organized as :

    data_dir/
        labels/
            prefix1.csv
            prefix2_1.csv
            prefix2_2.csv
        PDFs/
            prefix1.pdf
            prefix2.pdf

The numbered suffix of the ground truth CSV is the table number.
"""

# Standard imports
import logging
import pathlib
import sys
from typing import List

# External imports
import pandas as pd

# Local imports
import country_by_country.img_table_extraction as img_table_extraction


def evaluate_single_report(
    pdf_filepath: pathlib.Path, tables: List[pd.DataFrame]
) -> None:
    logging.info(
        f"\nProcessing {pdf_filepath.name}, with {len(tables)} ground truth tables"
    )

    table_extractor = img_table_extraction.from_config(
        {
            "type": "Unstructured",
            "params": {"pdf_image_dpi": 300, "hi_res_model_name": "yolox"},
        }
    )

    extracted_assets = {
        "text_table_extractors": {},
        "img_table_extractors": {},
    }
    table_extractor(pdf_filepath, extracted_assets)
    extracted_tables = extracted_assets["img_table_extractors"]["unstructured"][
        "tables"
    ]

    print(f"===> Extracted {len(extracted_tables)}, expected {len(tables)}")


def evaluate_table_extraction(datadir: pathlib.Path) -> None:
    logging.info(f"Evaluation with the data in {datadir}")

    labels_dir = datadir / "labels"
    pdf_dir = datadir / "PDFs"

    for pdf_filepath in pdf_dir.glob("*.pdf"):
        prefix = pdf_filepath.stem
        # We check if there are any CSV associated
        # with this stem
        # and sort them by increasing table index
        csvs = sorted(list(labels_dir.glob(f"{prefix}*.csv")))

        if len(csvs) == 0:
            logging.info(f"Skipping {pdf_filepath.name}, there are no labels")
            continue

        logging.debug(f"For the pdf {pdf_filepath}, I found the CSVs {csvs}")
        tables = [pd.read_csv(csv_filepath) for csv_filepath in csvs]
        evaluate_single_report(pdf_filepath, tables)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <data_dir>")
        sys.exit(-1)

    evaluate_table_extraction(pathlib.Path(sys.argv[1]))
