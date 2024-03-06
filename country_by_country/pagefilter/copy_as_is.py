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

# External imports
import pypdf


class CopyAsIs:
    """
    Dummy filter just copying the source pdf to a target
    temporary file
    """

    def __init__(self) -> None:
        pass

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        """
        Basically copies the source pdf at a temporary location.
        Writes assets:
            src_pdf: the original pdf filepath
            target_pdf: the temporary target pdf filepath
            selected_pages : list of selected pages
        """
        filename = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        shutil.copy(pdf_filepath, filename)

        reader = pypdf.PdfReader(pdf_filepath)
        n_pages = len(reader.pages)

        if assets is not None:
            assets["pagefilter"] = {
                "src_pdf": pdf_filepath,
                "target_pdf": filename,
                "selected_pages": list(range(n_pages)),
            }
