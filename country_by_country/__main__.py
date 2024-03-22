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
import pickle
import sys
from pathlib import Path

import yaml

# Local imports
from country_by_country import processor

NUM_CLI_ARGS = 3


def process_report(config: dict, pdf_filepath: str) -> None:
    proc = processor.ReportProcessor(config)
    return proc.process(pdf_filepath)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    if len(sys.argv) != NUM_CLI_ARGS:
        logging.error("Usage : python -m country_by_country config.yaml report.pdf")
        sys.exit(-1)

    logging.info(f"Loading {sys.argv[1]}")
    with Path(sys.argv[1]).open() as fh:
        config = yaml.safe_load(fh)

    assets = process_report(config, sys.argv[2])

    # Save all the assets to disk
    with Path("assets.pkl").open("wb") as fh:
        pickle.dump(assets, fh)
    logging.info(
        "Assets dumped in assets.pkl. You can read then using : \n"
        + "pickle.load(open('assets.pkl', 'rb'))",
    )
