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

# Standard import
import pickle
import pkgutil
import tempfile

# External imports
import joblib
import numpy as np
import pypdf


class FeatureExtractor:
    """
    A class to extract the features of a page as required by the random forest
    classifier
    """

    def __init__(self, keywords: list[str], all_country_names: list[str]) -> None:
        """
        Arguments:
            keywords: the keywords to count from the page text content
            all_country_names: the country names/flags to count in the page content
        """
        self.all_country_names = all_country_names
        self.keywords = keywords

    def number_country_names(self, text: str) -> int:
        """
        Computes and returns the total number of occurence of any of the the
        country names
        """
        return sum([text.count(country) for country in self.all_country_names])

    def keyword(self, text: str, keyword: str) -> int:
        """
        Computes and returns the number of occurence of the specific keyword
        """
        return text.count(keyword)

    def __call__(self, text: str) -> np.array:
        """
        Extracts the feature vector from the text
        The features we extract are:
            - nb_country: the total number of country names in the page
            - keywords: how many times a string in the list of keywords is contained in the page

        A typical list of keywords is :
            ["tax","countr","country by country","country-by-country","report","cbc",\
            "revenu","transparen","ethic","incom","employ","benefi","asset","contrib",\
            "profit","accrued","jurisdiction","sales","ebt","paid","stated","accu","tangible",\
            "fte", "expense", "related","headcount","capital","turnover","retained","current",\
            "plant","work","intragroup","remuneration","debt","contribution","per country"]
        """
        features = [self.number_country_names(text)]
        features.extend([self.keyword(text, keyword_i) for keyword_i in self.keywords])
        return features


class RFClassifier:
    """
    RandomForest classifier of whether a page contains a CbCR table or not
    This randomforest decides from the text content of the page and is unable
    to detect a page where a CbCR table would be included as an image
    """

    def __init__(self, modelfile: str) -> None:
        # Access the model bundled in the package
        data = pkgutil.get_data(
            "country_by_country",
            f"models/{modelfile}",
        )
        keywords = pickle.loads(
            pkgutil.get_data("country_by_country", "models/random_forest_keywords.pkl"),
        ).split(",")

        all_country_names = pickle.loads(
            pkgutil.get_data(
                "country_by_country",
                "models/random_forest_country_names.pkl",
            ),
        )
        self.feature_extractor = FeatureExtractor(keywords, all_country_names)
        # Unpack the data in a temporary file that joblib can then load
        with tempfile.NamedTemporaryFile("wb", delete=False) as fp:
            fp.write(data)
            fp.close()
            self.clf = joblib.load(fp.name)

    def __call__(self, pdf_filepath: str, assets: dict) -> None:
        """
        Reads and processes a pdf from its filepath
        It writes the filtered pdf as a temporary pdf
        The filepath of this temporary pdf is returned

        Writes assets:
            src_pdf: the original pdf filepath
            target_pdf: the temporary target pdf filepath
            selected_pages : List of int
        """

        # Generate a temporary filename where to save the filtered pdf
        filename = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        reader = pypdf.PdfReader(pdf_filepath)
        writer = pypdf.PdfWriter()

        # Extract the features from all the pages
        page_features = []
        for p in reader.pages:
            content = p.extract_text().lower()
            page_features.append(self.feature_extractor(content))

        # features is now num_pages x num_features_per_page
        page_features = np.array(page_features)
        n_pages, n_features_per_page = page_features.shape

        # Concatenate the features of the previous page and the next page
        # the random forest expects
        # [features_page_{i-1}, features_page_{i}, features_pages_{i+1}]
        features = np.zeros((n_pages, 3 * n_features_per_page))
        features[1:, :n_features_per_page] = page_features[:-1]
        features[:, n_features_per_page:-n_features_per_page] = page_features
        features[:-1, -n_features_per_page:] = page_features[1:]

        # Performs the prediction
        predictions = self.clf.predict(features)

        # And now we keep only the pages that have been selected
        selected_pages = []
        for ip, (p, keep_p) in enumerate(zip(reader.pages, predictions, strict=True)):
            if keep_p:
                writer.add_page(p)
                selected_pages.append(ip)
        writer.write(filename)

        if assets is not None:
            assets["pagefilter"] = {
                "src_pdf": pdf_filepath,
                "target_pdf": filename,
                "selected_pages": selected_pages,
            }
