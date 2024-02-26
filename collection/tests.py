def download_pdf(url, directory="pdf_downloads"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        filename = url.split("/")[-1]
        filepath = os.path.join(directory, filename)

        os.makedirs(directory, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {str(e)}")


def find_and_download_pdfs(search_query):
    for url in search(search_query, sleep_interval=5, num_results=50):
        if url.lower().endswith(".pdf"):
            download_pdf(url)
        else:
            try:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                pdf_links = soup.find_all("a", href=re.compile(r"\.pdf$"))
                for link in pdf_links:
                    pdf_url = link.get("href")
                    if pdf_url.startswith("http"):
                        download_pdf(pdf_url)
                    else:
                        # Handling relative URLs
                        from urllib.parse import urljoin

                        download_pdf(urljoin(url, pdf_url))
            except requests.RequestException as e:
                print(f"Failed to process {url}: {str(e)}")


# Example search queries
search_queries = "site:https://www.allianz.com/ country by country reporting pdf"
