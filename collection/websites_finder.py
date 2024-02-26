import requests
import pandas as pd
from loguru import logger as lg


api_key = "AIzaSyC4y5w028I3-LOVLEzDV6fOWV3EsstmdKk"
cx = "e3e7d6d29161d4932"


def find_company_website(company_name, api_key, cse_id):
    search_query = f"{company_name} official website"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": search_query,
    }
    response = requests.get(url, params=params)
    result = response.json()

    # Attempt to extract the first search result URL
    try:
        website_url = result["items"][0]["link"]
        lg.success(f"Found website for {company_name}: {website_url}")
        return website_url

    except Exception as e:
        lg.error(f"Error finding website for {company_name}: {e}")
        return "Website not found"


def process_companies(csv_file_path, api_key, cse_id):
    companies_df = pd.read_csv(csv_file_path)
    website_urls = []

    for index, row in companies_df.iterrows():
        company_name = row["global company"]
        website_url = find_company_website(company_name, api_key, cse_id)
        website_urls.append(website_url)

    companies_df["website_url"] = website_urls
    companies_df.to_csv(csv_file_path, index=False)


process_companies("collection/data/forbes2000.csv", api_key, cx)
