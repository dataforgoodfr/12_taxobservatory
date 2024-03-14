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

import country_by_country.pagefilter as pagefilter


def test_copy_as_is():
    config = {"type": "CopyAsIs"}
    myfilter = pagefilter.from_config(config)

    assets = {}
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [0]


def test_filter_pages():
    config = {"type": "FromFilename"}
    myfilter = pagefilter.from_config(config)

    assets = {}
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [0]


def test_rf_classifier():
    config = {
        "type": "RFClassifier",
        "params": {"modelfile": "random_forest_model_low_false_positive.joblib"},
    }
    myfilter = pagefilter.from_config(config)

    assets = {}
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [0]
