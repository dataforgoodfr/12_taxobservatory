import unittest
from pathlib import PosixPath
from unittest.mock import MagicMock, mock_open, patch

from collecte import pdf_downloader


class TestCBCRScript(unittest.TestCase):
    def setUp(self) -> None:
        self.company_name = "TestCompany"
        self.keywords = "tax country by country reporting GRI 207-4"
        self.api_key = "test_api_key"
        self.cse_id = "test_cse_id"
        self.pdf_url = "https://example.com/report.pdf"

    @patch("collecte.pdf_downloader.requests.get")
    def test_cbcr_finder(self, mock_get: any) -> None:
        # Setup mock response for requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"link": self.pdf_url},
            ],
        }
        mock_get.return_value = mock_response

        # Call the function
        result = pdf_downloader.cbcr_finder(
            self.company_name,
            self.keywords,
            self.api_key,
            self.cse_id,
        )

        # Assert the result
        assert self.pdf_url in result
        mock_get.assert_called_once()

    @patch("collecte.pdf_downloader.requests.get")
    @patch("collecte.pdf_downloader.Path.exists")
    @patch("collecte.pdf_downloader.Path.open", new_callable=mock_open)
    def test_download_pdf(
        self,
        mock_file: any,
        mock_exists: any,
        mock_get: any,
    ) -> None:
        # Setup mocks
        mock_exists.return_value = False
        mock_response = MagicMock()
        mock_get.return_value = mock_response
        mock_response.iter_content.return_value = [b"test data"]

        # Expected filename
        expected_filename = "collecte/data/pdf_downloads/TestCompany/report.pdf"

        # Call the function
        result = pdf_downloader.download_pdf(
            self.pdf_url,
            "collecte/data/pdf_downloads",
            self.company_name,
        )

        # Assert the calls and result
        assert result == expected_filename
        mock_file.assert_called_once_with(PosixPath(expected_filename), "wb")
        mock_exists.assert_any_call(PosixPath(expected_filename))
        mock_get.assert_called_once_with(
            self.pdf_url,
            stream=True,
            timeout=10,
            headers=None,
        )


if __name__ == "__main__":
    unittest.main()
