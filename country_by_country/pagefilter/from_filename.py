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
import shutil
import tempfile
from pathlib import Path

# External imports
import pypdf

NUM_PAGE_FIELDS = 2


class FromFilename:
    """
    Filtering from filename. This filter expects the filename
    of the pdf contains either the page or a page range of interest
    explicitely given in the filename as :

        /dir/containing/the/filename_of_the_report_#1.pdf
        /dif/containing/the/filename_of_the_report_#1-#2.pdf

    where #1 is a single page
          #1-#2 is a page range
    """

    def __init__(self) -> None:
        pass

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        """
        Reads and processes a pdf from its filepath
        It writes the filtered pdf as a temporary pdf
        The filepath of this temporary pdf is returned

        Writes assets:
            src_pdf: the original pdf filepath
            target_pdf: the temporary target pdf filepath
            selected_pages : list of selected pages
        """

        filename = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        # Get the page or page range from the filename
        src_filename = Path(pdf_filepath).name

        # We remove the extension, split on "_" and keep the last field
        pagefield = src_filename[:-4].split("_")[-1]
        selected_pages = []

        if pagefield.isnumeric():
            selected_pages = [int(pagefield) - 1]
        else:
            pagefields = pagefield.split("-")
            if (
                len(pagefields) == NUM_PAGE_FIELDS
                and pagefields[0].isnumeric()
                and pagefields[1].isnumeric()
            ):
                selected_pages = list(range(int(pagefields[0]) - 1, int(pagefields[1])))

        # Extract the selected pages
        if len(selected_pages) == 0:
            # If we keep all the page, just copy the pdf
            shutil.copy(pdf_filepath, filename)
        else:
            reader = pypdf.PdfReader(pdf_filepath)
            writer = pypdf.PdfWriter()

            for pi in selected_pages:
                writer.add_page(reader.pages[pi])
            writer.write(filename)

        if assets is not None:
            assets["pagefilter"] = {
                "src_pdf": pdf_filepath,
                "target_pdf": filename,
                "selected_pages": selected_pages,
            }
