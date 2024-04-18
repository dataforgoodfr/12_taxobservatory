import logging
import pickle
import signal
from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from time import time

import pandas as pd
import requests
import yaml
from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError


import tqdm
from tqdm import tqdm

from urllib.parse import urlparse

from .logger import FileLogger, StdoutLogger

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
        "dateRestrict": "y2", #restrict search to the specified number of past years
        "fileType": "pdf",  # Search only for PDF files
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


def download_pdf(
    url: str,
    download_folder: Path,
    company_name: str,
    fetch_timeout_s: int,
    check_pdf_integrity: bool,
) -> None | Exception:

    # Extract the hostname from the URL
    parsed_url = urlparse(url)
    website_name = parsed_url.hostname.split(".")[-2]  # Extract the second-level domain name

    # Create a sanitized version of the company name for the directory
    company_folder = download_folder / website_name

    Path.mkdir(company_folder, parents=True, exist_ok=True)
    local_filename = Path(company_folder) / url.split("/")[-1]
    exception_status = None

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
                            exception_status = TimeoutError
                            break
                        if content_length is not None:
                            pbar_content.update(1)

            if Path.exists(local_filename):
                logger.logger.info(f"Downloaded '{local_filename}'")
                if check_pdf_integrity:
                    current_pdf_is_valid, exception_status = pdf_is_valid(
                        local_filename,
                    )
                    if not current_pdf_is_valid:
                        logger.logger.error(
                            f"PDF file '{local_filename}' seems broken and will be discarded",
                        )
                        local_filename.unlink(missing_ok=True)

        except requests.RequestException as e:
            logger.logger.exception(f"Failed to download {url}")
            local_filename.unlink(missing_ok=True)
            exception_status = type(e)
    else:
        logger.logger.warning(
            f"File '{local_filename}' already exists, download ignored",
        )

    return exception_status


def find_and_download_pdfs(
    csv_path: Path,
    api_key: str,
    cse_id: str,
    keywords: str,
    download_folder: Path,
    fetch_timeout_s: int,
    check_pdf_integrity: bool,
    url_cache_filepath: Path | None = None,
) -> None:

    all_urls, df_no_url = fetch_pdf_urls(
        csv_path,
        api_key,
        cse_id,
        keywords,
        url_cache_filepath,
    )

    downloaded_files = set()
    failed_downloads = []
    pbar_download = tqdm(total=len(all_urls))
    for company_name, url in all_urls:
        if url not in downloaded_files:
            exception_status = download_pdf(
                url,
                download_folder,
                company_name,
                fetch_timeout_s,
                check_pdf_integrity,
            )
            downloaded_files.add(url)
            if exception_status is not None:
                failed_downloads.append((company_name, url, exception_status))
        else:
            logger.logger.warning(f"URL '{url}' already downloaded, URL ignored")
        pbar_download.update(1)

    df_failed_downloads = pd.DataFrame(
        failed_downloads,
        columns=["company_name", "url", "exception"],
    )
    df_fail = pd.concat((df_no_url, df_failed_downloads))
    missing_data_filepath = download_folder / "missing_data.csv"
    if missing_data_filepath.exists():
        df_fail = pd.concat(
            (df_fail, pd.read_csv(missing_data_filepath)),
        ).drop_duplicates(["company_name", "url"])
    df_fail = df_fail.sort_values(["company_name", "url"])
    df_fail.index = range(len(df_fail))
    df_fail.to_csv(missing_data_filepath, index=False)


def fetch_pdf_urls(
    csv_path: Path,
    api_key: str,
    cse_id: str,
    keywords: str,
    url_cache_filepath: Path | None,
) -> (list[tuple[str, str]], pd.DataFrame):

    df_company = pd.read_csv(csv_path)
    company_names = set(df_company["name_normalized"].unique())

    query = Query(company_names, keywords)

    # Cache URLs queried with the Google API to avoid excessive costly queries when debugging
    if url_cache_filepath is None:
        url_cache_filepath = Path("pdf_url_cache.pkl")

    if url_cache_filepath.exists():
        with url_cache_filepath.open("rb") as f:
            cache_query, all_urls = pickle.load(f)

    if url_cache_filepath.exists() and cache_query == query:
        logger.logger.warning(
            f"Loaded pdf URLs list from cache file' {url_cache_filepath}'",
        )

    else:
        if url_cache_filepath.exists() and cache_query != query:

            for (param_name, param_query), param_cache in zip(
                asdict(query).items(),
                asdict(cache_query).values(),
                strict=True,
            ):
                if param_query != param_cache:
                    logger.logger.warning(
                        f"User input query value for '{param_name}' differs from cache query "
                        f"value: '{param_query}' != '{param_cache}'",
                    )
            logger.logger.warning(
                f"A new campaign of queries is launched, results will be cached to "
                f"'{url_cache_filepath}'",
            )

        all_urls = []
        n_queries = len(query.company_names)
        logger.logger.warning(f"Starting a query campaign ({n_queries} queries)..")
        pbar_query = tqdm(total=n_queries)

        for company_name in query.company_names:
            pdf_urls = cbcr_finder(company_name, query.keywords, api_key, cse_id)
            for url in pdf_urls:
                all_urls.append((company_name, url))
            pbar_query.update(1)

        with url_cache_filepath.open("wb") as f:
            pickle.dump((query, all_urls), f)
        logger.logger.warning(f"Cached pdf URLs list to file '{url_cache_filepath}'")

    company_names_no_url = company_names.difference({result[0] for result in all_urls})
    df_no_url = pd.DataFrame(company_names_no_url, columns=["company_name"])
    df_no_url["url"] = "No URL found"
    df_no_url["exception"] = None

    return all_urls, df_no_url


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


@dataclass
class Query:
    company_names: set[str]
    keywords: str


def pdf_is_valid(filepath: Path) -> (bool, None | PdfReadError | PdfStreamError):
    with filepath.open("rb") as f:
        try:
            pdf = PdfReader(f)
            info = pdf.metadata
            is_valid = bool(info)
            exception_status = None
        except (PdfReadError, PdfStreamError) as e:
            is_valid = False
            exception_status = type(e)
        return is_valid, exception_status


def timeout_handler(signum: any, frame: any) -> None:  # noqa: ARG001
    """Raises a TimeoutError upon calling."""
    raise TimeoutError


if __name__ == "__main__":

    parser = ArgumentParser(description="Run the PDF downloader")
    parser.add_argument(
        "src_filepath",
        type=Path,
        help="The CSV file storing the company names to target",
    )
    parser.add_argument(
        "googleapi_filepath",
        type=Path,
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
        type=Path,
        default=Path("collection/data/pdf_downloads"),
        help="The directory where the downloaded PDFs are saved",
    )
    parser.add_argument(
        "--url_cache_filepath",
        type=Path,
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
    with args.googleapi_filepath.open("r") as f:
        googleapi_credentials = yaml.full_load(f)
        api_key, cx = googleapi_credentials["api_key"], googleapi_credentials["cse_id"]

    Path.mkdir(args.dest_dirpath, parents=True, exist_ok=True)
    logger = FileLogger(
        str(
            args.dest_dirpath
            / f"run_pdf_downloader_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log",
        ),
    )
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    find_and_download_pdfs(
        csv_path=args.src_filepath,
        api_key=api_key,
        cse_id=cx,
        keywords=args.search_keywords,
        download_folder=args.dest_dirpath,
        url_cache_filepath=args.url_cache_filepath,
        fetch_timeout_s=args.fetch_timeout_s,
        check_pdf_integrity=not args.keep_broken_pdf,
    )
