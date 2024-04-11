import logging
import pickle
import signal
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from time import time
from typing import Any

import pandas as pd
import requests
import yaml
from logger import FileLogger, StdoutLogger
from pypdf import PdfReader
from pypdf.errors import PdfStreamError
from tqdm import tqdm

# default logger printing to stdout ; if run as main, a file+stdout logger is used instead
logger = StdoutLogger()


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
        logger.logger.error(f"No results found for query '{search_query}'")

    return pdf_urls


def pdf_is_valid(filepath: str | Path) -> bool:
    with open(filepath, "rb") as f:
        try:
            pdf = PdfReader(f)
            info = pdf.metadata
            return bool(info)
        except PdfStreamError:
            return False


def download_pdf(
    url: str,
    download_folder: Path,
    company_name: str,
    fetch_timeout_s: int,
    check_pdf_integrity: bool,
) -> str:

    # Create a sanitized version of the company name for the directory
    company_folder = download_folder / "".join(e for e in company_name if e.isalnum())

    Path.mkdir(company_folder, parents=True, exist_ok=True)
    local_filename = Path(company_folder) / url.split("/")[-1]

    if not Path.exists(local_filename):

        try:
            t_start = time()
            with requests.get(url, stream=True, timeout=(3.05, 10)) as r:
                r.raise_for_status()

                with Path.open(local_filename, "wb") as f:
                    chunk_size = 8192

                    # In debug mode, display a download progress bar for every file download
                    if logging.root.level <= logging.INFO:
                        content_length = get_content_length(r)
                    else:
                        content_length = None
                    if content_length is not None:
                        n_chunks, rem = (
                            content_length // chunk_size,
                            content_length % chunk_size,
                        )
                        if rem != 0:
                            n_chunks += 1
                        pbar_content = tqdm(total=n_chunks)
                    else:
                        logger.logger.info(
                            "Could not fetch the content length in a timely manner, no progress"
                            "bar displayed",
                        )

                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        now = time()
                        if (
                            fetch_timeout_s is not None
                            and now - t_start > fetch_timeout_s
                        ):
                            logger.logger.error(
                                f"Failed to download '{local_filename}' before timeout "
                                f"({fetch_timeout_s} s)\n",
                            )
                            local_filename.unlink(missing_ok=True)
                            break
                        if content_length is not None:
                            pbar_content.update(1)

            if Path.exists(local_filename):
                logger.logger.info(f"Downloaded '{local_filename}'")
                if check_pdf_integrity and not pdf_is_valid(local_filename):
                    logger.logger.error(
                        f"PDF file '{local_filename}' seems broken and will be erased",
                    )
                    local_filename.unlink(missing_ok=True)

        except requests.RequestException as e:
            logger.logger.error(f"Failed to download {url}: {e!s}")
            local_filename.unlink(missing_ok=True)
    else:
        logger.logger.warning(
            f"File '{local_filename}' already exists, download ignored",
        )
    return str(local_filename)


def find_and_download_pdfs(
    csv_path: str,
    api_key: str,
    cse_id: str,
    keywords: str,
    download_folder: Path,
    fetch_timeout_s: int,
    check_pdf_integrity: bool,
    url_cache_filepath: Path | None = None,
) -> None:

    # Cache URLs queried with the Google API to avoid excessive costly queries when debugging
    if url_cache_filepath is None:
        url_cache_filepath = Path("pdf_url_cache.pkl")

    if url_cache_filepath.exists():
        with open(url_cache_filepath, "rb") as f:
            all_urls = pickle.load(f)
        logger.logger.warning(
            f"Loaded pdf URLs list from cache file' {url_cache_filepath}'",
        )
    else:
        df = pd.read_csv(csv_path)
        all_urls = []

        for company_name in df["name_normalized"].unique():
            pdf_urls = cbcr_finder(company_name, keywords, api_key, cse_id)
            for url in pdf_urls:
                all_urls.append((company_name, url))

        with open(url_cache_filepath, "wb") as f:
            pickle.dump(all_urls, f)
        logger.logger.warning(f"Cached pdf URLs list to file '{url_cache_filepath}'")

    downloaded_files = set()
    pbar = tqdm(total=len(all_urls))
    for company_name, url in all_urls:
        if url not in downloaded_files:
            download_pdf(
                url,
                download_folder,
                company_name,
                fetch_timeout_s,
                check_pdf_integrity,
            )
            downloaded_files.add(url)
        else:
            logger.logger.warning(f"URL '{url}' already downloaded, URL ignored")
        pbar.update(1)


def get_content_length(r: requests.models.Response) -> int | None:

    try:
        content_length = int(r.headers["content-length"])
    except KeyError:
        try:
            # TODO: check Windows compatibility
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
            content_length = len(r.content)
        except TimeoutError:
            content_length = None

    signal.alarm(0)
    return content_length


def timeout_handler(signum: Any, frame: Any) -> None:
    """Raises a TimeoutError upon calling."""
    raise TimeoutError


if __name__ == "__main__":

    parser = ArgumentParser(description="Run the PDF downloader")
    parser.add_argument(
        "src_filepath",
        type=str,
        help="The CSV file storing the company names to target",
    )
    parser.add_argument(
        "googleapi_filepath",
        type=str,
        help="The YAML-like file storing the Google JSON API credentials",
    )
    parser.add_argument(
        "--search_keywords",
        type=str,
        default="tax country by country reporting GRI 207-4",
        help="The keywords used for the URL search query",
    )
    parser.add_argument(
        "--dest_dirpath",
        type=str,
        default="collection/data/pdf_downloads",
        help="The directory where the downloaded PDFs are saved",
    )
    parser.add_argument(
        "--url_cache_filepath",
        type=str,
        default=None,
        help="The pickled file where fetched URLs are cached for reruns",
    )
    parser.add_argument(
        "--fetch_timeout_s",
        type=int,
        default=60,
        help="Timeout threshold (in s) to download a PDF",
    )
    parser.add_argument(
        "--keep_broken_pdf",
        action="store_true",
        default=False,
        help="Disable broken PDF filtering",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Set the logging level to DEBUG (default is WARNING)",
    )

    args = parser.parse_args()
    with open(args.googleapi_filepath) as f:
        googleapi_credentials = yaml.full_load(f)
        api_key, cx = googleapi_credentials["api_key"], googleapi_credentials["cse_id"]
    dest_dirpath = Path(args.dest_dirpath)
    url_cache_filepath = args.url_cache_filepath
    if url_cache_filepath is not None:
        url_cache_filepath = Path(url_cache_filepath)

    Path.mkdir(dest_dirpath, parents=True, exist_ok=True)
    logger = FileLogger(
        str(
            dest_dirpath
            / f"run_pdf_downloader_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log",
        ),
    )
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    find_and_download_pdfs(
        csv_path=args.src_filepath,
        api_key=api_key,
        cse_id=cx,
        keywords=args.search_keywords,
        download_folder=dest_dirpath,
        url_cache_filepath=url_cache_filepath,
        fetch_timeout_s=args.fetch_timeout_s,
        check_pdf_integrity=not args.keep_broken_pdf,
    )
