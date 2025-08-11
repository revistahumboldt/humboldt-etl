import traceback
from igpage.extract import get_ig_page_next_day_data
from igpage.init_fb_api import _initialize_facebook_api
from igpage.transform import transform_igpage_data
from igpage.load import load_data_to_bigquery
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

def run_etl(gcp_project_id: str,
            bq_dataset_id: str, 
            bq_table_id: str,
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
        #IMPORTANT: the until date is excluded of the results, so that just the data for since will come
        ig_page_raw_data = get_ig_page_next_day_data(page_id,gcp_project_id,bq_dataset_id,bq_table_id, 1, service_account_key_path)
  
        # 2. Transforming
        print("\n2. Data transformation...")
        igpage_transformed_data = transform_igpage_data(ig_page_raw_data, page_id)
        print(f"Transformation applied on {len(igpage_transformed_data)} items.")

        if not igpage_transformed_data:
            print("No transformed data to load. Closing the pipeline.")
            return
    
        # 3. Loading in BigQuery
        print("\n3. Loading data into BigQuery...")
        load_data_to_bigquery(igpage_transformed_data,gcp_project_id, bq_dataset_id, bq_table_id, service_account_key_path)
   
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 



    
  

 