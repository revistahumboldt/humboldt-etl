from fad.extract import extract_raw_data
from fad.load import load_data_to_bigquery
from fad.transform import transform_insights
#from fad.load import load_data_to_bigquery
from google.cloud import bigquery # Importar bigquery para usar WriteDisposition
from utils.get_date import DateUtils
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
load_dotenv()


def run_etl_pipeline(account_id: str,
                     gcp_project_id: str ,
                     bq_dataset_id: str, 
                     bq_table_id: str,
                     time_range: dict,     
                     service_account_key_path: Optional[str]=None
):
    print(f"Starting an ETL pipeline for an account {account_id} for period {time_range}...")
   
    # 1. Extracting
    print("1. Extracting data from Facebook Ads...")
    raw_insights = extract_raw_data(account_id, time_range, service_account_key_path)
    print(f"Extracted {len(raw_insights)} items.")
    
    # 2. Transforming
    print("2. Data transformation...")
    transformed_insights = transform_insights(raw_insights)
    print(f"Transformation applied on {len(transformed_insights)} items.")

    if not transformed_insights:
        print("No transformed data to load. Closing the pipeline.")
        return
    
    # 3. Loading in BigQuery
    print("3. Loading data into BigQuery...")
   
    if service_account_key_path != None and service_account_key_path.strip():
        try:
            load_data_to_bigquery(
                transformed_insights,
                gcp_project_id,
                bq_dataset_id,
                bq_table_id,
                service_account_key_path
            )
            print("ETL pipeline successfully completed on local pc!")
    

        except Exception as e:
            print(f"ETL pipeline failed in the loading phase: {e}")
            raise
    
    if service_account_key_path == None or service_account_key_path == "":
        try:
            load_data_to_bigquery(
                transformed_insights,
                gcp_project_id,
                bq_dataset_id,
                bq_table_id,
            )
            print("ETL pipeline successfully completed on the cloud!")
    

        except Exception as e:
            print(f"ETL pipeline failed in the loading phase: {e}")
            raise
     
