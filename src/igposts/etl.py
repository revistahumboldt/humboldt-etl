import traceback
from igposts.extract import get_ig_posts_next_day_data, get_raw_igposts
from igposts.init_fb_api import _initialize_facebook_api
from igposts.transform import transform_igposts_data
from igposts.load import load_data_to_bigquery
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

def run_etl(gcp_project_id: str,
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
        # 1. Extracting
        print("\n2. Data extraction for ig posts...")
        
        #raw_ig_posts_data = get_raw_igposts(page_id, {'since':'2023-05-20','until':'2023-05-25'})
        raw_ig_posts_data = get_ig_posts_next_day_data(page_id, gcp_project_id, dataset_id, table_id, 30,service_account_key_path)
     
        print(f"Extraction retrieved {len(raw_ig_posts_data)} items.")
        #print(raw_ig_posts_data)        
        
        # 2. Transforming
        print("\n2. Data transformation for ig posts...")
        igposts_transformed_data = transform_igposts_data(raw_ig_posts_data, page_id)
        print(f"Transformation applied on {len(igposts_transformed_data)} items.")
        #print(igposts_transformed_data)

        if not igposts_transformed_data:
            print("No transformed data to load. Closing the pipeline.")
            return
        
        print(f"Sample transformed data: {igposts_transformed_data[0]}")
        print(f"Total transformed data: {len(igposts_transformed_data)}")
        
        # 3. Loading in BigQuery
        print("\n3. Loading  ig posts data into BigQuery...")
        print("dataset", dataset_id)
        load_data_to_bigquery(igposts_transformed_data,gcp_project_id, dataset_id, table_id, service_account_key_path)
        
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 



    
  

 