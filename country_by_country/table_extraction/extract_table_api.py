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
import uuid

# External imports
try:
    from ExtractTable import ExtractTable
except ImportError as e:

    class ExtractTableModuleException(Exception):
        def __init__(self) -> None:
            super().__init__("You must install ExtractTable : pip install ExtractTable")

    raise ExtractTableModuleException() from e


class ExtractTableAPI:
    def __init__(self) -> None:
        api_key = os.getenv("EXTRACT_TABLE_API_KEY")
        self.extract_table = ExtractTable(api_key)

    def __call__(self, pdf_filepath: str) -> None:
        """
        Writes assets:
            ntables: the number of detected tables
            tables: a list of pandas dataframe of the parsed tables
        """
        tables_list = self.extract_table.process_file(
            filepath=pdf_filepath,
            pages="all",
            output_format="df",
        )

        # Create asset
        new_asset = {
            "id": uuid.uuid4(),
            "type": "ExtractTableAPI",
            "tables": tables_list,
        }

        return new_asset
