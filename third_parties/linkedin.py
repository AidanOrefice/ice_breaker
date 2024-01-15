import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}

    if not True:
        response = requests.get(
            "https://gist.githubusercontent.com/AidanOrefice/8ac51364956513d5ec801e47438c2570/raw/72d538e6e80f6a31c4fc1fcac00460d3c21a8d97/aidan-orefice.json"
        )
    else:
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", " ", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    
    #data["profile_pic_url"] = "https://www.linkedin.com/in/aidan-orefice"

    return data
