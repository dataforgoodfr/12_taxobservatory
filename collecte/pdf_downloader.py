from pathlib import Path

import pandas as pd
import requests

keywords = "tax country by country reporting GRI 207-4"
api_key = ""
cx = ""


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


def download_pdf(url: str, download_folder: str, company_name: str) -> str:
    # Create a sanitized version of the company name for the directory
    company_folder = Path(download_folder) / "".join(
        e for e in company_name if e.isalnum()
    )

    Path.mkdir(company_folder, parents=True, exist_ok=True)

    local_filename = Path(company_folder) / url.split("/")[-1]

    if not Path.exists(local_filename):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with Path.open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Downloaded: {local_filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e!s}")
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
        csv_path="collection/data/orbis_d4g_sample.csv",
        api_key=api_key,
        cse_id=cx,
        keywords=keywords,
        download_folder="collection/data/pdf_downloads",
    )
