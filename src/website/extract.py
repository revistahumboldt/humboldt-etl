import requests
import os
import json
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from typing import List, Dict, Any, Optional
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import os
from dotenv import load_dotenv
load_dotenv()
from .utils.get_mapp_token import get_mapp_token
from .utils.config_analysis import config_analysis
from utils.get_date import DateUtils
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
MAPP_DATASET_ID = os.getenv("MAPP_DATASET_ID","")
MAPP_TABLE_ID = os.getenv("MAPP_TABLE_ID","")

def get_webiste_page_data(project_id: str,
        dataset_id: str,
        table_id: str,
        delta_days: int = 1,
        service_account_key_path: Optional[str] = None):
    try:

        # Step 1: Get the authentication token
        token = get_mapp_token()

        # Step 2: Get the time range according to the last data in BigQuery
        time_range = DateUtils.get_bq_based_time_range(project_id, dataset_id,table_id, delta_days,service_account_key_path)

        print("Fetching mapp data for time range: ", time_range)
        
        # Step 3: Prepare and send the request to the Mapp API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        #update date in config analysis object
        config_analysis['queryObject']['predefinedContainer']['filters'][0]['value1'] = time_range['since']
        config_analysis['queryObject']['predefinedContainer']['filters'][0]['value2'] = time_range['until']

        print(config_analysis['queryObject']['predefinedContainer']['filters'][0])

        mapp_config = config_analysis
     
        
        result_url = None
        while not result_url:
            print("Waiting for the data to be ready...")
            response = requests.post(
                os.getenv("MAPP_CONFIG_ANALYSIS_URL", ""),
                json=mapp_config,
                headers=headers
            )
            response.raise_for_status()
            
            result_url = response.json().get("resultUrl")

        print("Data is ready. Fetching results...")
        result = requests.get(result_url, headers=headers)
        result.raise_for_status()
        
        rows = result.json()["rows"]

        return rows
        
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err.response.status_code}")
        print(f"Error data: {err.response.text}")
        raise
    except requests.exceptions.RequestException as err:
        print(f"Error on request: {err}")
        raise
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        raise


