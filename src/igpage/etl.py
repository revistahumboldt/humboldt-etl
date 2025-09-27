import traceback
from igpage.extract import get_ig_page_next_day_data, get_igpage_raw_data
from igpage.init_fb_api import _initialize_facebook_api
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
        # 1. Extracting. 
        print("\n1. Data extract for Instagram page data.")
        ig_raw_page_data = get_ig_page_next_day_data(page_id, project_id, dataset_id, table_id, 1, service_account_key_path)
        #ig_raw_page_data = get_igpage_raw_data(page_id, {'since':'2025-09-01','until':'2025-09-01'})
        print(f"Extracted {len(ig_raw_page_data)} raw posts.")
        print(ig_raw_page_data)

        # 2. Transforming
        print("\n2. Data transformation...")
        igpage_transformed_data = transform_igpage_data(ig_raw_page_data, page_id)
        print(f"Transformation applied on {len(ig_raw_page_data)} items.")
        print(igpage_transformed_data)

        if not ig_raw_page_data:
            print("No transformed data to load. Closing the pipeline.")
            return
    
        # 3. Loading in BigQuery
        print("\n3. Loading data into BigQuery.")
        load_data_to_bigquery(igpage_transformed_data,project_id, dataset_id, table_id, service_account_key_path)
        
        
        
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 



    
  

 