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
import collections
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


def normalize_num_str(el: any, check_abs: bool = True) -> str:
    """Normalize numeric string to prepare for comparison:
    - Remove any empty spaces
    - Replace enclosing parentheses with "negative" sign
    - Check if is a number
    - Round number to avoid equality comparison round-off error
    - Optionnally convert to absolute value
    Test with: AXA_2021_CbCR_24-27.pdf / llama_parse / table 1"""
    out = el
    with contextlib.suppress(Exception):
        out = re.sub(r"^\((.*?)\)$", r"-\1", str(out).replace(" ", "").replace(",", ""))
        out = str(round(float(out), 2)).rstrip("0").rstrip(".")

    if check_abs is True:
        out = out.lstrip("-")

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


def compute_recall_matrix(assets: dict, ref_data: pd, check_abs: bool) -> pd:
    # Initialize recall dataframe
    extractions = append_count_to_duplicates(
        [
            extractor["type"]
            for extractor in assets[next(iter(assets))]["table_extractors"]
        ],
    )
    df_recall = pd.DataFrame(columns=extractions)

    # Loop over the PDF files in assets
    for pdf_file in assets:

        # Get REF data corresponding to PDF file
        company = pdf_file.split("_")[0]
        year = pdf_file.split("_")[1]
        cols = [2, *list(range(5, 10)), *list(range(15, 18))]
        df_ref = (
            ref_data.query(f'company=="{company}" and year=={year}')
            .iloc[:, cols]
            .reset_index(drop=True)
            .dropna(axis="columns", how="all")
        )
        ref_values = (
            df_ref.iloc[0:, 1:]
            .map(normalize_num_str, check_abs=check_abs)
            .to_numpy()
            .flatten()
        )
        ref_counter = collections.Counter(ref_values)

        # Compute recall for each extraction
        new_row = {}
        for idx, asset in enumerate(assets[pdf_file]["table_extractors"]):
            cur_values = []
            for df in asset["tables"]:
                cur_values.extend(
                    df.map(normalize_num_str, check_abs=check_abs).to_numpy().flatten(),
                )
            cur_counter = collections.Counter(cur_values)
            cnt = 0
            for ref_val in ref_counter:
                if ref_val != "nan":  # Aegon_2020_CbCR_13.pdf
                    cnt += min(cur_counter[ref_val], ref_counter[ref_val])
            new_row[extractions[idx]] = round(
                100 * cnt / sum(x != "nan" for x in ref_values),
            )

        # Update recall dataframe
        df_recall.loc[len(df_recall)] = new_row
        df_recall.rename(index={len(df_recall) - 1: pdf_file}, inplace=True)

    df_recall.sort_index(inplace=True)
    return df_recall
