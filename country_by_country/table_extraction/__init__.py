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

# Local imports
import logging
import sys

from .camelot_extractor import Camelot
from .from_csv import FromCSV
from .llama_parse_extractor import LlamaParseExtractor
from .unstructured import Unstructured
from .unstructured_api import UnstructuredAPI

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")


def from_config(config: dict) -> Camelot:
    extractor_type = config["type"]
    extractor_params = {}
    if "params" in config:
        extractor_params = config["params"]
    if extractor_type == "Camelot":
        return Camelot(**extractor_params)
    elif extractor_type == "FromCSV":
        return FromCSV(**extractor_params)
    elif extractor_type == "Unstructured":
        return Unstructured(**extractor_params)
    elif extractor_type == "UnstructuredAPI":
        return UnstructuredAPI(**extractor_params)
    elif extractor_type == "LlamaParse":
        return LlamaParseExtractor(**extractor_params)
    elif extractor_type == "ExtractTableAPI":
        # This is for legacy support
        # In order to be able to use ExtractTable
        # for benchmarking
        # Note: ExtractTable-py is not maintained anymore
        # This is the reason why this case is handled in a specific way
        from .extract_table_api import ExtractTableAPI

        return ExtractTableAPI(**extractor_params)
    else:
        logging.info(f"There are no extractors of the type : {extractor_type}")
