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
import contextlib
import re

import pandas as pd


def append_count_to_duplicates(strings: list[str]) -> list[str]:
    """Append count to duplicate strings in array"""
    count_dict = {}
    for i, string in enumerate(strings):
        if string in count_dict:
            count_dict[string] += 1
            strings[i] = f"{string}_{count_dict[string]}"
        else:
            count_dict[string] = 0
    return strings


def convert_num_to_str(val: any) -> str:
    """Convert number to str and remove any trailing zeros for floats"""
    out = val
    with contextlib.suppress(Exception):
        out = str(float(out)).rstrip("0").rstrip(".")

    out = str(out)
    return out


def normalize_num_str(el: any) -> str:
    """Normalize numeric string:
    - Remove empty spaces
    - Add "negative" sign to str with enclosing parentheses
    - Check if is a number
    Test with: AXA_2021_CbCR_24-27.pdf / llama_parse / table 1
    """
    out = el
    with contextlib.suppress(Exception):
        out = re.sub(r"^\((.*?)\)$", r"-\1", str(out).replace(" ", ""))
        out = str(float(out)).rstrip("0").rstrip(".")

    out = out.replace(",", "")
    return out


def clean_headers(df: pd) -> None:
    """Transform multi-row headers to single-row and deduplicate
    - Multi-row & empty headers: ACS_2019_CbCR_3.pdf / unstructured / detectron2_onnx
    - Duplicated non-empty headers: AkerSolutions_2015_CbCR_16.pdf / llama_parse"""
    # Transform multi-rown headers to single-row
    if isinstance(df.columns, pd.MultiIndex):
        # Erase first any "Unnamed" headers originating from the html to df conversion
        clean_columns = []
        for col in df.columns:
            clean_columns.append(
                [item for item in col if "Unnamed" not in item],
            )

        df.columns = [": ".join(list(dict.fromkeys(col))) for col in clean_columns]

    # Deduplicate headers
    if df.columns.duplicated().sum() > 0:
        cols = pd.Series(df.columns)
        for dup in set(df.columns[df.columns.duplicated()]):
            prefix = f"{dup}_"
            if dup == "":
                prefix = "COL"
            cols[df.columns.get_loc(dup)] = [
                prefix + str(idx)
                for idx, _ in enumerate(slice_to_mask(df.columns.get_loc(dup)))
            ]
        df.columns = cols


def slice_to_mask(s: any) -> list:
    if isinstance(s, slice):
        start, stop, step = s.start, s.stop, s.step
        if step is None:
            step = 1
        return [i in range(start, stop, step) for i in range(s.stop)]
    return s
