import os

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint

load_dotenv()


def get_llm(max_tokens=1024, temperature=0.0, verbose=True):
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACE_ALEXIS_API_TOKEN")
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-v0.1",  # "mistralai/Mistral-7B-Instruct-v0.2"
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        # max_tokens=128,
        # temperature=0.5,
    )
    return llm
