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
import os
import uuid
from io import StringIO

import pandas as pd
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError


class UnstructuredAPI:
    def __init__(self, **kwargs: dict) -> dict:
        """
        Builds a pdf page parser, looking for tables using
        the unstructured.io api.
        The kwargs given to the constructor are directly propagated
        to the partition_pdf function.
        You are free to define any parameter partition_pdf recognizes
        """
        self.kwargs = kwargs
        self.type = "unstructured_api"

    def __call__(self, pdf_filepath: str) -> dict:
        logging.info("\nKicking off extraction stage...")
        logging.info(f"Extraction type: {self.type}, with params: {self.kwargs}")

        s = UnstructuredClient(api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"))

        with open(pdf_filepath, "rb") as f:
            # Note that this currently only supports a single file
            files = shared.Files(
                content=f.read(),
                file_name=pdf_filepath,
            )

        req = shared.PartitionParameters(
            files=files,
            strategy="hi_res",
            pdf_infer_table_structure="True",
            **self.kwargs,
        )

        try:
            resp = s.general.partition(req)

            tables_list = [
                pd.read_html(StringIO(el["metadata"]["text_as_html"]))[0]
                for el in resp.elements
                if el["type"] == "Table"
            ]

            # Create asset
            new_asset = {
                "id": uuid.uuid4(),
                "type": "unstructured_api",
                "params": self.kwargs,
                "tables": tables_list,
            }

            return new_asset

        except SDKError as e:
            print(e)
