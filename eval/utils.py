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


def convert_to_str(val: any) -> str:
    """Convert input to str and remove any trailing zeros for floats"""
    with contextlib.suppress(Exception):
        return str(float(val)).rstrip("0").rstrip(".")
    return str(val)


def reformat_str(el: any) -> str:
    """Normalize input value:
    - If numerical, convert to string
    - If contains comma, remove comma
    - If enclosed in "()", convert to negative value
    Output string."""
    el = convert_to_str(el).replace(",", "")
    return re.sub(r"\((\d+)\)", r"-\1", el)
