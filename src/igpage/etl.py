import traceback
from igpage.extract import get_ig_page_next_day_data
from fbpage.init_fb_api import _initialize_facebook_api
from fbpage.utils.get_page_token import get_page_token
from fbpage.extract import get_fb_posts_data

from igpage.transform import transform_igpage_data
from igpage.load import load_data_to_bigquery
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

def run_etl(project_id: str,
            dataset_id: str, 
            table_id: str,
            page_id:str,
            meta_app_id:str,
            meta_app_secret: str,
            meta_access_token: str,
            service_account_key_path: Optional[str]=None
):

    try:
        _initialize_facebook_api(meta_app_id, meta_app_secret, meta_access_token)
    except ValueError as ve:
        print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
        exit(1) 

    try:
        # 0. Initialize app for page access 
        page_token = get_page_token(page_id)
        _initialize_facebook_api(meta_app_id, meta_app_secret, page_token)

        # 1. Extracting. 
        print("\n1. Data extract for facebook posts...")
        fb_rw_posts_data = get_fb_posts_data(page_id, project_id, dataset_id, table_id, 1, service_account_key_path)
        print(f"Extracted {len(fb_rw_posts_data)} raw posts.")
  
        # 2. Transforming
        print("\n2. Data transformation...")
        fbpage_transformed_data = ""
        print(f"Transformation applied on {len(fbpage_transformed_data)} items.")

        if not fbpage_transformed_data:
            print("No transformed data to load. Closing the pipeline.")
            return
    
        # 3. Loading in BigQuery
        print("\n3. Loading data into BigQuery...")
        #load_data_to_bigquery(fbpage_transformed_data,gcp_project_id, bq_dataset_id, bq_table_id, service_account_key_path)
   
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 



    
  

 