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
import os
import shutil
import tempfile

# External imports
import PyPDF2


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

    def __init__(self):
        pass

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        """
        Reads and processes a pdf from its filepath
        It writes the filtered pdf as a temporary pdf
        The filepath of this temporary pdf is returned

        Writes assets:
            src_pdf: the original pdf filepath
            target_pdf: the temporary target pdf filepath
            page_range : tuple or None
        """

        filename = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        # Get the page or page range from the filename
        src_filename = os.path.basename(pdf_filepath)

        # We remove the extension, split on "_" and keep the last field
        pagefield = src_filename[:-4].split("_")[-1]
        if pagefield.isnumeric():
            page_range = (int(pagefield) - 1, int(pagefield))
        else:
            pagefields = pagefield.split("-")
            if (
                len(pagefields) == 2
                and pagefields[0].isnumeric()
                and pagefields[1].isnumeric()
            ):
                page_range = (int(pagefields[0]) - 1, int(pagefields[1]))
            else:
                page_range = None

        # Extract the selected pages
        if page_range is None:
            # If we keep all the page, just copy the pdf
            shutil.copy(pdf_filepath, filename)
        else:
            reader = PyPDF2.PdfReader(pdf_filepath)
            writer = PyPDF2.PdfWriter()
            start_page = page_range[0]
            end_page = page_range[1]
            pages = reader.pages[start_page:end_page]
            for p in pages:
                writer.add_page(p)
            writer.write(filename)

        if assets is not None:
            assets["pagefilter"] = {
                "src_pdf": pdf_filepath,
                "target_pdf": filename,
                "page_range": page_range,
            }
