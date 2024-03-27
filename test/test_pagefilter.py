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
import pypdf

# Local imports
from country_by_country import pagefilter
from country_by_country.utils.utils import keep_pages


def test_copy_as_is() -> None:
    config = {"type": "CopyAsIs"}
    myfilter = pagefilter.from_config(config)

    assets = {}
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [0]

    assets = {}
    src_path = "./test/data/Allianz_2017_CbCR_7.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == list(range(11))


def test_from_filemane() -> None:
    config = {"type": "FromFilename"}
    myfilter = pagefilter.from_config(config)

    assets = {}
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [0]

    assets = {}
    src_path = "./test/data/Allianz_2017_CbCR_7.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [6]


def test_rf_classifier() -> None:
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

    assets = {}
    src_path = "./test/data/Allianz_2017_CbCR_7.pdf"
    myfilter(src_path, assets)
    assert assets["pagefilter"]["src_pdf"] == src_path
    assert assets["pagefilter"]["selected_pages"] == [6, 7]


def test_keep_pages() -> None:
    src_path = "./test/data/Acciona_2020_CbCR_1.pdf"
    selected_pages = [0]
    out_pdf = keep_pages(src_path, selected_pages)

    # This test does not work even if we just copy
    # all the pages from the source pdf

    reader = pypdf.PdfReader(out_pdf)
    assert len(reader.pages) == len(selected_pages)
