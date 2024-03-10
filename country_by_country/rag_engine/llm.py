import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub

load_dotenv()

def get_llm(max_tokens=1024, temperature=0.0, verbose=True):
    huggingfacehub_api_token = os.getenv("HUGGINGFACE_API_TOKEN")
    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-alpha",
        model_kwargs={"temperature": 0.1, "max_new_tokens": 200},
        huggingfacehub_api_token=huggingfacehub_api_token
    )
    return llm
