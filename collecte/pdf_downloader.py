import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

keywords = "tax country by country reporting GRI 207-4"
api_key = os.getenv("GOOGLE_API_KEY")
cx = os.getenv("GOOGLE_CX")
if api_key is None or cx is None:
    raise KeyError(  # noqa: TRY003
        "Please set GOOGLE_API_KEY and GOOGLE_CX environment variables.",
    )

# Define a header designed to mimic a request from a web browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    ),
}


def cbcr_finder(
    company_name: str,
    keywords: str,
    api_key: str,
    cse_id: str,
) -> list[str]:
    search_query = f"{company_name} {keywords}"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": search_query,
    }
    response = requests.get(url, params=params)
    result = response.json()

    pdf_urls = []
    if "items" in result:
        items = result["items"]
        for item in items:
            link = item["link"]
            if link.endswith(".pdf"):
                pdf_urls.append(link)
    else:
        print("No results found.")

    return pdf_urls


def _download_pdf(
    url: str,
    local_filename: Path,
    headers: dict[str, str] | None = None,
) -> None:
    """
    Downloads a PDF file from a specified URL and saves it to a local file.

    This function attempts to download a file from the provided URL and save it
    to the specified local path. If the initial download attempt without headers times out,
    the function retries the download using a predefined HTTP headers designed to
    mimic a web browser request.

    Parameters:
        url (str): The URL from which to download the PDF file.
        local_filename (Path): The local path (including filename) where the PDF will be saved.
        headers (dict, optional): A dictionary of HTTP headers to send with the request.
            If None, the function initially tries without headers, and on timeout, retries with
            default browser-like headers.
    """
    try:
        with requests.get(url, stream=True, timeout=10, headers=headers) as r:
            r.raise_for_status()
            with local_filename.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except requests.exceptions.Timeout:
        if headers is None:  # Check if headers were not used in the initial request
            print("Initial request timed out. Retrying with headers...")
            return _download_pdf(url, local_filename, HEADERS)
        print("The request timed out with headers.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e!s}")


def download_pdf(url: str, download_folder: str, company_name: str) -> str:
    # Create a sanitized version of the company name for the directory
    company_folder = Path(download_folder) / "".join(
        e for e in company_name if e.isalnum()
    )

    Path.mkdir(company_folder, parents=True, exist_ok=True)

    local_filename = Path(company_folder) / url.split("/")[-1]

    if not Path.exists(local_filename):
        _download_pdf(url, local_filename)
    else:
        print(f"Already exists: {local_filename}")
    return str(local_filename)


def find_and_download_pdfs(
    csv_path: str,
    api_key: str,
    cse_id: str,
    keywords: str,
    download_folder: str,
) -> None:
    df = pd.read_csv(csv_path)
    downloaded_files = set()

    for company_name in df["name_normalized"].unique():
        pdf_urls = cbcr_finder(company_name, keywords, api_key, cse_id)
        for url in pdf_urls:
            if url not in downloaded_files:
                download_pdf(url, download_folder, company_name)
                downloaded_files.add(url)


if __name__ == "__main__":
    find_and_download_pdfs(
        csv_path="collecte/data/orbis_d4g_sample.csv",
        api_key=api_key,
        cse_id=cx,
        keywords=keywords,
        download_folder="collecte/data/pdf_downloads",
    )
