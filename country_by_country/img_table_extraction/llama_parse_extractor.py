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

# External imports
import pandas as pd
from llama_parse import LlamaParse
import os
from dotenv import load_dotenv
import nest_asyncio


class LlamaParseExtractor:
    def __init__(self, **kwargs: dict) -> None:
        """
        Builds a pdf page parser, looking for tables using
        the llama_parse library.
        The kwargs given to the constructor are directly propagated
        to the LlamaParse constructor.
        You are free to define any parameter LlamaParse recognizes
        """
        self.kwargs = kwargs

        # Load LLAMA_CLOUD_API_KEY from .env file
        load_dotenv()
        # llama-parse is async-first
        nest_asyncio.apply()

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        json_objs = LlamaParse(**self.kwargs).get_json_result(pdf_filepath)

        tables_list = []
        for page in json_objs[0]["pages"]:
            for item in page["items"]:
                if item['type'] == 'table':
                    df = pd.DataFrame(item["rows"][1:], columns=item["rows"][0])
                    tables_list.append(df)

        assets["img_table_extractors"]["llama_parse"] = {
            "ntables": len(tables_list),
            "tables": tables_list,
        }