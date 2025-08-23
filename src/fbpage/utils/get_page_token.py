from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
import os
from dotenv import load_dotenv
from typing import cast, Dict, Any


load_dotenv()

def get_page_token(page_id: str) -> str:
    page_access_token = ""
    try:
        page_obj = Page(page_id)
        
        # Cast para type dict
        page_info = cast(Dict[str, Any], page_obj.api_get(fields=['access_token']))
        page_access_token = page_info.get('access_token')
        
        page_access_token = page_info['access_token']
        
        if not page_access_token:
            raise ValueError("Failed to retrieve the page access token.")
        
        print("Page access token retrieved successfully.")
        
        return page_access_token
    
    except Exception as e:
        print("Error retrieving page access token.")
        print(f"Detalhes: {e}")
        return page_access_token
    
