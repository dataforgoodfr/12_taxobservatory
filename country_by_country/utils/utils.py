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
import tempfile

# External imports
import pypdf


def filter_pages(pdf_filepath: str, selected_pages: list[int]) -> str:
    """
    Function to extract the selected pages from a source pdf
    It returns the path to the PDF created by keeping only the
    selected pages
    """
    reader = pypdf.PdfReader(pdf_filepath)
    writer = pypdf.PdfWriter()

    for pi in selected_pages:
        writer.add_page(reader.pages[pi])

    filename = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
    writer.write(filename)

    return filename

def gather_tables(assets): # TODO : find a better way than hard coding. fix inconsistancy of camelot extractor (should be in img_table_extractor)
    tables_by_name = {}
    if len(assets["text_table_extractors"]["camelot_stream"]["tables"]) != 0:
        tables_by_name["camelot_stream"] = assets["text_table_extractors"]["camelot_stream"]["tables"][0]
    
    if len(assets["text_table_extractors"]["camelot_lattice"]["tables"]) != 0:
        tables_by_name["camelot_lattice"] =  assets["text_table_extractors"]["camelot_lattice"]["tables"][0]

    if len(assets["img_table_extractors"]["unstructured"]["tables"]) != 0:
        tables_by_name["unstructured"] = assets["img_table_extractors"]["unstructured"]["tables"][0]
        
    return tables_by_name
