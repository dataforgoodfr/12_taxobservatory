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
import logging

# Local imports
from .utils.utils import filter_pages
from . import img_table_extraction, pagefilter, table_cleaning


class ReportProcessor:
    def __init__(self, config: dict) -> None:
        # Report filter
        self.page_filter = pagefilter.from_config(config["pagefilter"])

        # Table extraction from images
        img_table_extractors = config["table_extraction"]["img"]
        self.img_table_extractors = [
            img_table_extraction.from_config(name) for name in img_table_extractors
        ]

        # Table cleaning & reformatting
        table_cleaners = config["table_cleaning"]
        self.table_cleaners = [
            table_cleaning.from_config(name) for name in table_cleaners
        ]

    def process(self, pdf_filepath: str) -> dict:
        logging.info(f"Processing {pdf_filepath}")

        assets = {
            "pagefilter": {},
            "text_table_extractors": {},
            "img_table_extractors": {},
            "table_cleaners": {},
        }

        # Filtering the pages
        self.page_filter(pdf_filepath, assets)

        # Now that we identified the pages to be extracted, we extract them
        # Note, in a GUI, we could ask the user to the change the content of
        # assets["pagefilter"]["selected_pages"] before selecting the pages
        pdf_to_process = filter_pages(
            pdf_filepath,
            assets["pagefilter"]["selected_pages"],
        )

        # Process the selected pages to detect the tables and extract
        # their contents
        for img_table_extractor in self.img_table_extractors:
            img_table_extractor(pdf_to_process, assets)

        # Give the parsed content to the cleaner stage for getting organized data
        for table_cleaner in self.table_cleaners:
            table_cleaner(assets)

        return assets
