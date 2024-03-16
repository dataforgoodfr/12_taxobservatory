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
    table_extractor, report_fh, pdf_filepath: pathlib.Path, tables: List[pd.DataFrame]
) -> None:
    logging.info(
        f"\nProcessing {pdf_filepath.name}, with {len(tables)} ground truth tables"
    )

    extracted_assets = {
        "text_table_extractors": {},
        "img_table_extractors": {},
    }
    table_extractor(pdf_filepath, extracted_assets)
    extracted_tables = extracted_assets["img_table_extractors"]["unstructured"][
        "tables"
    ]

    print(
        f"===> Extracted {len(extracted_tables)} tables, expected {len(tables)} tables"
    )

    # Fill in the HTML report
    # with the tables to parse and the parsed tables
    report_fh.write('<div class="tab">')
    # Fill in the parsed tables
    report_fh.write(
        f"Parsed {len(extracted_tables)} tables, expected {len(tables)} tables"
    )
    report_fh.write("<h1>Parsed tables</h1>")
    for df in extracted_tables:
        df = df[0]  # For some reasons, this is a list ?
        report_fh.write(df.to_html())

    # Separator
    report_fh.write("<h1>Ground truth</h1>")
    # Fill in the tables to parse
    for df_gt in tables:
        report_fh.write(df_gt.to_html())

    report_fh.write("</div>")


def evaluate_table_extraction(datadir: pathlib.Path) -> None:
    logging.info(f"Evaluation with the data in {datadir}")

    labels_dir = datadir / "labels"
    pdf_dir = datadir / "PDFs"

    config = {
        "type": "Unstructured",
        "params": {"pdf_image_dpi": 300, "hi_res_model_name": "yolox"},
    }
    table_extractor = img_table_extraction.from_config(config)

    fh = open("report.html", "w")
    fh.write(
        """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
  """
    )

    write_style(fh)
    fh.write(
        """
  </style>
</head>
<body>"""
    )

    fh.write(f"Config : \n {config} \n")

    fh.write(
        """
<div class="tabs">
            """
    )

    first = True
    for idx, pdf_filepath in enumerate(pdf_dir.glob("*.pdf")):
        prefix = pdf_filepath.stem
        # We check if there are any CSV associated
        # with this stem
        # and sort them by increasing table index
        csvs = sorted(list(labels_dir.glob(f"{prefix}*.csv")))

        if len(csvs) == 0:
            logging.info(f"Skipping {pdf_filepath.name}, there are no labels")
            continue

        fh.write(
            f"""
<input type="radio" name="tabs" id="tab{idx}" checked={"checked" if first else ""}>
<label for="tab{idx}">{prefix}</label>
        """
        )

        logging.debug(f"For the pdf {pdf_filepath}, I found the CSVs {csvs}")
        tables = [pd.read_csv(csv_filepath) for csv_filepath in csvs]
        evaluate_single_report(table_extractor, fh, pdf_filepath, tables)
        first = False

    fh.write(
        """
</div>
</body>
</html>
            """
    )


def write_style(fh):
    fh.write(
        """
/**
 * Tabs
 */
.tabs {
	display: flex;
	flex-wrap: wrap; // make sure it wraps
}
.tabs label {
	order: 1; // Put the labels first
	display: block;
	padding: 1rem 2rem;
	margin-right: 0.2rem;
	cursor: pointer;
  background: #90CAF9;
  font-weight: bold;
  transition: background ease 0.2s;
}
.tabs .tab {
  order: 99; // Put the tabs last
  flex-grow: 1;
	width: 100%;
	display: none;
  padding: 1rem;
  background: #fff;
}
.tabs input[type="radio"] {
	display: none;
}
.tabs input[type="radio"]:checked + label {
	background: #fff;
}
.tabs input[type="radio"]:checked + label + .tab {
	display: block;
}

@media (max-width: 45em) {
  .tabs .tab,
  .tabs label {
    order: initial;
  }
  .tabs label {
    width: 100%;
    margin-right: 0;
    margin-top: 0.2rem;
  }
}

/**
 * Generic Styling
*/
body {
  background: #eee;
  min-height: 100vh;
	box-sizing: border-box;
	padding-top: 10vh;
  font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
  font-weight: 300;
  line-height: 1.5;
  max-width: 100%;
  margin: 0 auto;
  font-size: 112%;
}

/**
 * Tables
 */


.dataframe {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

.dataframe td, .dataframe th {
  border: 1px solid #ddd;
  padding: 8px;
}

.dataframe tr:nth-child(even){background-color: #f2f2f2;}

.dataframe tr:hover {background-color: #ddd;}

.dataframe th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #044A6D;
  color: white;
}
            """
    )


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <data_dir>")
        sys.exit(-1)

    evaluate_table_extraction(pathlib.Path(sys.argv[1]))
