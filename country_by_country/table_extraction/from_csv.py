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

# Standard imports
import glob
import uuid
from pathlib import Path

# External imports
import pandas as pd


class FromCSV:
    def __init__(self, csv_directory: str) -> None:
        self.csv_directory = csv_directory

    def __call__(self, pdf_filepath: str) -> dict:
        """
        Returns asset that contain:

        """
        # Build the path to the csv of the tables
        # we expect the csv to be defined as
        # - given a report /path/to/my_report.pdf
        # Tables are searched for as
        # - csv_directory/my_report_1.csv, csv_directory/my_report_2.csv,
        # csv_directory/my_report_2.csv, ...
        tables_list = []
        report_basename = Path(pdf_filepath).stem.split("____")[0]

        tables_files = glob.glob(f"{self.csv_directory}/{report_basename}*.csv")
        tables_list = [pd.read_csv(f) for f in tables_files]

        # Create asset
        new_asset = {
            "id": uuid.uuid4(),
            "type": "from_csv",
            "params": {"csv_directory": self.csv_directory},
            "tables": tables_list,
        }

        return new_asset
