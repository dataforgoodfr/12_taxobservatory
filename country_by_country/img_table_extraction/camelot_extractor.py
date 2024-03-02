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

# External imports
import camelot


class Camelot:
    def __init__(self, flavor: str) -> None:
        self.flavor = flavor

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        """
        Writes assets:
            ntables: the number of detected tables
            tables: a list of pandas dataframe of the parsed tables
        """
        tables = camelot.read_pdf(pdf_filepath, flavor=self.flavor)

        # Write the parsed tables into the assets
        tables_list = [t.df for t in tables]
        key_assets = f"camelot_{self.flavor}"
        if key_assets in assets["text_table_extractors"]:
            logging.warning(
                f">> The key {key_assets} already exists in the assets dictionary. I will overwrite its content",
            )

        assets["text_table_extractors"][key_assets] = {
            "ntables": len(tables_list),
            "tables": tables_list,
        }
