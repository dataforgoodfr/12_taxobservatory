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
import uuid

# External imports
from transformers import pipeline


class HFCleaner:
    def __init__(self, model_name: str, **kwargs: dict) -> None:
        """
        Builds a table cleaner, by extracting clean data from tables
        extracted during table extraction stage.
        The kwargs given to the constructor are directly propagated
        to the LLMCleaner constructor.
        You are free to define any parameter LLMCleaner recognizes.

        Arguments:
            - model_name: the name of the model to load with pipeline
        """
        logging.info("Loading the LLM ")
        self.pipe = pipeline("text-generation", model=model_name)
        logging.info("LLM loaded")

    def __call__(self, asset: dict) -> dict:
        """
        Extracts clean data from tables using a language model with huggingface
        """
        tables = asset["tables"]

        logging.info(f"Pulling {len(tables)} tables from extraction stage")

        # Convert tables to html to add to LLM prompt
        md_tables = [table.to_markdown() for table in tables]

        # ---------- CHAIN 1/2 - Pull countries from each table ----------
        logging.info("Starting chain 1/2: extracting country names from tables")

        prompt = (
            "Extract an exhaustive list of countries from the following tables in markdown : \n"
            + "\n".join(md_tables)
        )
        output = self.pipe(prompt, max_length=100)
        print(output)

        # Create asset
        new_asset = {
            "id": uuid.uuid4(),
            "type": self.type,
            "params": self.kwargs,
            "table": None,
        }

        return new_asset
