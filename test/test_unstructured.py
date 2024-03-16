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
import numpy as np

# Local imports
from country_by_country import img_table_extraction


def test_unstructured_yolox() -> None:
    config = {
        "type": "Unstructured",
        "params": {"pdf_image_dpi": 300, "hi_res_model_name": "yolox"},
    }
    table_extractor = img_table_extraction.from_config(config)

    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    assets = {"img_table_extractors": {}}
    table_extractor(src_path, assets)

    ntables = assets["img_table_extractors"]["unstructured"]["ntables"]
    tables = assets["img_table_extractors"]["unstructured"]["tables"]

    # To get the expected result :
    # python -m pytest -s
    # cbcr_table = tables[1]
    # column_idx = 3
    # print(cbcr_table[column_idx].tolist())

    # As of 03/2024, unstructured yolox detects 1 table
    assert ntables == 1

    # The detection of the table is perfect
    table = tables[0][0]

    assert table.shape == (12, 9)

    # for column_idx in range(9):
    #     print(f"expected_c{column_idx} = {table[\"columns[column_idx]\"].tolist()}")
    expected_columns = [
        "Tax jurisdiction",
        "Total sales (M€)",
        "EBT (M€)",
        "Corporate Income Tax accrued (M€)",
        "Corporate Income Tax paid on a cash basis (M€)",
        "Employees at the close of 2020",
        "Grants (M€)",
        "Footnote explaining effective rate due",
        "Footnote explaining effective rate paid",
    ]

    assert list(table.columns) == expected_columns
    expected_c0 = [
        "Spain",
        "Germany",
        "Mexico",
        "Australia",
        "Poland",
        "Saudi Arabia",
        "Portugal",
        "Brazil",
        "USA",
        "Canada",
        "Others",
        "Total",
    ]

    # assert table[] == expected_columns
    expected_c1 = [
        "2673",
        "12",
        "238",
        "881",
        "335",
        "329",
        "152",
        "44",
        "7)",
        "327",
        "1409",
        "6472",
    ]
    expected_c2 = [
        "367",
        "75",
        "54",
        "33",
        "19",
        "10",
        "9",
        "-8",
        "-4)",
        "-44",
        "35",
        "508",
    ]
    expected_c3 = [51, -8, 19, 13, 4, 6, 7, -16, -6, -1, 27, 97]
    expected_c4 = [-0.7, -1.0, 71.0, 0.0, 14.0, 6.6, 5.2, 0.2, 0.0, 1.0, 24.8, 44.5]
    expected_c5 = [20860, 428, 1978, 1704, 1523, 131, 2015, 390, 184, 1379, 7763, 38355]
    expected_c6 = [48.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 13.0, 0.0, 0.3, 6.4]
    expected_c7 = [1.0, 1.0, 5.8, 45.0, 4.0, 4.0, 7.0, 3.0, 7.0, 7.0, np.nan, np.nan]
    expected_c8 = [2.0, 2.0, 9.0, 10.0, 9.0, 4.0, 11.0, 2.0, 2.1, 2.0, np.nan, np.nan]
