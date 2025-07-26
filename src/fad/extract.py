from dotenv import load_dotenv
from facebook_business.adobjects import adaccount
from facebook_business.api import FacebookRequestError, Cursor, FacebookRequest # Import Cursor e FacebookRequest
from utils.get_date import DateUtils
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
load_dotenv()

#extracts insigts for a given time range and ad account
def get_fb_raw_data(ad_account_id: str, 
                    time_range: dict,
                     service_account_key_path: Optional[str]=None) -> list:
    
    print(f"DEBUG: ad_account_id received in extract_ad_insights: '{ad_account_id}' (Type: {type(ad_account_id)})")
    ad_account = adaccount.AdAccount(ad_account_id)

    insights_data = []

    # Defining the fields we want to extract
    # https://developers.facebook.com/docs/marketing-api/insights/reference
    fields = [
    'ad_id',
    'campaign_name',
    'adset_name',
    'ad_name',
    'frequency',
    'spend',
    'reach',
    'impressions', 
    'objective',
    "optimization_goal",
    "clicks",
    "actions"
]
    
    # parameter dictionary
    params = {
        'time_increment': 1, # daily insights , 
        #'date_preset': date_preset, # 'yesterday', 'last_7_days', etc.
        'time_range': time_range, # Alternative to date_preset
        'level': 'ad', # level (account, campaign, adset, ad)
        'breakdowns': ['age', 'gender'],       
        'action_breakdowns': ['action_type']  
    }

    print(f"Extracting insights for the account {ad_account_id} with parameters: {params}")
    print(f"time_range: {params['time_range']}")
    try:
        # get_insights() returns an iterator, which handles pagination automatically
        # insights is a list of dictionaries
        
        insights_raw_response = ad_account.get_insights(fields=fields, params=params)
        print("Successful insights data.")
        insights_list = []

        if isinstance(insights_raw_response, Cursor):
            # If it's a Cursor, we iterate directly
            for insight in insights_raw_response:
                insights_list.append(insight)

        if isinstance(insights_raw_response, FacebookRequest):
            # If FacebookRequest, we need to execute it
            # and then iterate over the result. This is less common for get_insights.
            # However, FacebookRequest.execute() returns a FacebookResponse,
            # which can have an .iterate_edge() method or be a list of objects.
            response = insights_raw_response.execute()

            if isinstance(response, list):
                insights_list = response # If the answer is a list of objects
            
            if not isinstance(response, list): # If the answer is not a list of objects
                try:
                    for item in response: # Pode ser um FacebookResponse que é iterável
                        insights_list.append(item)
                except TypeError:
                    # If response is not iterable, we assume it's a single object
                    insights_list.append(response)
            
        insights_data = insights_list
        print(f"Insights extracted successfully: {len(insights_data)} records found.")
    
    except FacebookRequestError as e:
        print(f"Facebook API Error while extracting insights: {e.api_error_code} - {e.api_error_message}")
        print(f"API Error Type: {e.api_error_type}")
        raise

    except Exception as e:
        print(f"Error while extracting insights from Facebook: {e}")
        raise # Re-raise so that main.py can capture

    return insights_data


def get_next_day_data(ad_account_id: str, 
                        gcp_project_id:str, 
                        gcp_dataset_id:str, 
                        gcp_table_id:str,
                        service_account_key_path: Optional[str]=None
                     ) -> list:
    extract_has_data = False
    increment = 1
    while not extract_has_data:
        time_range = DateUtils.get_time_range(gcp_project_id, gcp_dataset_id, gcp_table_id, increment, service_account_key_path)
        print(f"Trying to get data for time_range: {time_range}") 

        raw_data = get_fb_raw_data(ad_account_id, time_range, service_account_key_path)
        if len(raw_data) == 0:
            increment += 1
            print(len(raw_data))
            print(f"No data found for increment {increment}. Trying next increment.")
        if len(raw_data) > 0:
            extract_has_data = True
            print(f"Data found for increment {increment}. Extracted {len(raw_data)} records.")
            increment = 1  # Reset increment for next extraction
            return list(raw_data)
        if increment > 50:
            print("\nNo data found multiple tries. Exiting extraction.")
            return []
    # Ensure a list is always returned, even if the loop does not execute
    return []
        
    