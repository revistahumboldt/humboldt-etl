import traceback
from website.extract import get_webiste_page_data
from website.transform import transform_website_data
from website.load import load_data_to_bigquery
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

def run_etl(gcp_project_id: str,
            bq_dataset_id: str, 
            bq_table_id: str,
            service_account_key_path: Optional[str]=None
):
    try:
        # 1. Extracting
        print("\n2. Data extraction for website data...")
        raw_mapp_data = get_webiste_page_data(gcp_project_id, bq_dataset_id, bq_table_id, 1,service_account_key_path)
        print(f"Extraction returned {len(raw_mapp_data)} rows of data.")
        
        """
        for row in raw_mapp_data: 
            print(row[5])
        """

        # 2. Transforming
        print("\n2. Data transformation for website data...")
        website_transformed_data = transform_website_data(raw_mapp_data)
        print(f"Transformation applied on {len(website_transformed_data)} items.")

        if not website_transformed_data:
            print("No transformed data to load. Closing the pipeline.")
            return
        
        # 3. Loading in BigQuery
        print("\n3. Loading  ig posts data into BigQuery...")
        load_data_to_bigquery(website_transformed_data,gcp_project_id, bq_dataset_id, bq_table_id, service_account_key_path)
        
        
   
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 



    
  

 