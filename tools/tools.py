import os
import requests
from dotenv import load_dotenv
from langchain.serpapi import SerpAPIWrapper

load_dotenv()


def get_profile_url(text: str) -> str:
    """Searches for LinkedIn Profile Page"""
    search = SerpAPIWrapper()
    res = search.run(f"{text}")
    return res
