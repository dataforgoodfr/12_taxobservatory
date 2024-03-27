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

# External imports
import pandas as pd
from pandas.testing import assert_frame_equal

# Local imports
from country_by_country import table_extraction


def test_unstructured_yolox() -> None:
    config = {
        "type": "Unstructured",
        "params": {"pdf_image_dpi": 300, "hi_res_model_name": "yolox"},
    }
    table_extractor = table_extraction.from_config(config)

    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    asset = table_extractor(src_path)

    tables = asset["tables"]

    # As of 03/2024, unstructured yolox detects 1 table
    assert len(tables) == 1

    # The detection of the table is perfect
    table = tables[0]

    # To get the expected result :
    # python -m pytest -s
    # >> table.to_csv("/tmp/table.csv", index=False)

    expected_table = pd.read_csv(
        "./test/data/unstructured_yolox_Acciona_2020_CbCR_1.csv",
    )

    assert_frame_equal(table, expected_table)
