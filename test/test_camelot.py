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
from country_by_country import img_table_extraction

NTABLES_DETECTED_ACCIONA = 4


def test_camelot() -> None:
    flavor = "stream"
    config = {"type": "Camelot", "params": {"flavor": flavor}}
    table_extractor = img_table_extraction.from_config(config)

    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    asset = table_extractor(src_path)

    ntables = asset["ntables"]
    tables = asset["tables"]

    # As of 03/2024, camelot detects 4 tables
    assert ntables == NTABLES_DETECTED_ACCIONA

    # To get the expected result :
    # python -m pytest -s
    # >>> cbcr_table = tables[1]
    # >>> column_idx = 3
    # >>> print(cbcr_table[column_idx].tolist())

    expected_c0 = [
        "",
        "",
        "",
        "",
        "Spain",
        "Germany",
        "",
        "Mexico",
        "",
        "Australia",
        "Poland",
        "",
        "Saudi Arabia",
        "",
        "Portugal",
        "Brazil",
        "USA",
        "",
        "Canada",
        "Others",
        "Total",
        "",
    ]

    expected_c3 = [
        "Tax accrued (M€)",
        "",
        "",
        "",
        "51",
        "-8",
        "",
        "19",
        "",
        "13",
        "4",
        "",
        "6",
        "",
        "7",
        "-16",
        "-6",
        "",
        "-0.1",
        "27",
        "97",
        "",
    ]
    assert tables[1][0].tolist() == expected_c0
    assert tables[1][3].tolist() == expected_c3
