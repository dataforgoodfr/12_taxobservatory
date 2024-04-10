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
import pathlib
import tempfile

import pandas as pd

# External imports
import pypdf


def keep_pages(pdf_filepath: str, selected_pages: list[int]) -> str:
    """
    Function to extract the selected pages from a source pdf
    It returns the path to the PDF created by keeping only the
    selected pages
    """
    reader = pypdf.PdfReader(pdf_filepath)
    writer = pypdf.PdfWriter()

    for pi in selected_pages:
        writer.add_page(reader.pages[pi])

    # We add the original pdf name without extension
    # in the prefix of the temporary file
    # in order to keep a trace of this name so that the next modules, from table
    # extraction can make use of this name.
    # For example, FromCSV makes use of this name to determine the name of the
    # CSV to load
    pdf_stem = pathlib.Path(pdf_filepath).stem
    filename = tempfile.NamedTemporaryFile(
        prefix=f"{pdf_stem}____",
        suffix=".pdf",
        delete=False,
    ).name
    print(f"filename {filename}")
    writer.write(filename)

    return filename


def gather_tables(
    assets: dict,
) -> dict:
    tables_by_name = {}
    for asset in assets["table_extractors"]:
        tables = asset["tables"]
        if len(tables) == 1:
            tables_by_name[asset["type"]] = tables[0]
        elif len(tables) > 1:
            for i in range(len(tables)):
                tables_by_name[asset["type"] + "_" + str(i)] = tables[i]

    return tables_by_name


def check_if_many(assets: dict) -> bool:
    for asset in assets["table_extractors"]:
        tables = asset["tables"]
        if len(tables) > 1:
            return True
    return False


def filled_table_extractors(assets: dict) -> list:
    tables_by_name = []
    print(assets)
    for asset in assets["table_extractors"]:
        tables = asset["tables"]
        if len(tables) > 0:
            tables_by_name.append(asset["type"])
    return tables_by_name


def gather_tables_with_merge(
    assets: dict,
    new_tables: pd.DataFrame,
    table_extractor: str,
) -> dict:
    tables_by_name = {}
    for asset in assets["table_extractors"]:
        if asset["type"] == table_extractor:
            tables_by_name[table_extractor] = new_tables
        else:
            tables = asset["tables"]
            if len(tables) == 1:
                tables_by_name[asset["type"]] = tables[0]
            elif len(tables) > 1:
                for i in range(len(tables)):
                    tables_by_name[asset["type"] + "_" + str(i)] = tables[i]

    return tables_by_name
