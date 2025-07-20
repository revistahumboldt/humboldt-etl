from dotenv import load_dotenv
from facebook_business.adobjects import adaccount, campaign, adset, ad, adcreative, adsinsights
from utils.get_bq_last_date import get_bq_last_date
from facebook_business.api import FacebookAdsApi, FacebookRequestError, Cursor, FacebookRequest # Importe Cursor e FacebookRequest
import os
from dotenv import load_dotenv
load_dotenv()

GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")


def extract_ad_insights(ad_account_id: str) -> list:
  
    ad_account = adaccount.AdAccount(ad_account_id)
    if not ad_account:
        raise ValueError(f"Ad account with ID {ad_account_id} not found.")   
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
        'time_increment': 1, # daily insights 
        #'date_preset': date_preset, # 'yesterday', 'last_7_days', etc.
        'time_range': get_bq_last_date(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH), # Alternative to date_preset
        'level': 'ad', # level (account, campaign, adset, ad)
        'breakdowns': ['age', 'gender'],       
        'action_breakdowns': ['action_type']  
    }

    print(f"Extracting insights for the account {ad_account_id} for the period {get_bq_last_date(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH)}...")
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
            # Se é um FacebookRequest, iteramos diretamente
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
    
    except FacebookRequestError as e:
        print(f"Facebook API Error while extracting insights: {e.api_error_code} - {e.api_error_message}")
        print(f"API Error Type: {e.api_error_type}")
        raise

    except Exception as e:
        print(f"Error while extracting insights from Facebook: {e}")
        raise # Re-raise so that main.py can capture

    return insights_data

