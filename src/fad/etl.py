from fad.extract import get_fb_raw_data, get_next_day_data
from fad.load import load_data_to_bigquery
from fad.transform import transform_insights
#from fad.load import load_data_to_bigquery
from google.cloud import bigquery 
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()


def run_etl(ad_account_id: str,
            gcp_project_id: str,
            bq_dataset_id: str, 
            bq_table_id: str,
            time_range: dict,
            window: str,     
            service_account_key_path: Optional[str]=None
):

    # 1. Extracting. Note -- we are using if daily/last28days beaucause 
    raw_insights = []

    if window == "daily":
        try:
            print(f"Starting an ETL pipeline for an account {ad_account_id} for period {time_range}...")
            print("\n1. Extracting data from Facebook Ads...")
            raw_insights = get_next_day_data(ad_account_id, gcp_project_id, bq_dataset_id,bq_table_id)
            print(f"Extracted {len(raw_insights)} items.")
        except Exception as e:
             print("Error by colleting raw daily data", e)
    
    if window == "last_28_days":
        try:
            print("1. Extracting data from Facebook Ads...")
            raw_insights = get_fb_raw_data(ad_account_id, time_range, service_account_key_path)
            print(f"Extracted {len(raw_insights)} items.")
        except Exception as e:
            print("Error by colleting raw last_28_days data", e)


    # 2. Transforming
    print("\n2. Data transformation...")
    transformed_insights = transform_insights(raw_insights)
    print(f"Transformation applied on {len(transformed_insights)} items.")

    if not transformed_insights:
        print("No transformed data to load. Closing the pipeline.")
        return
    
    # 3. Loading in BigQuery
    print("\n3. Loading data into BigQuery...")
   
    if service_account_key_path != None and service_account_key_path.strip():
        try:
                load_data_to_bigquery(
                    transformed_insights,
                    gcp_project_id,
                    bq_dataset_id,
                    bq_table_id,
                    service_account_key_path
                )
                print("\nETL pipeline successfully completed on local pc!")
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
                print("\nETL pipeline successfully completed on the cloud!")
        except Exception as e:
                print(f"ETL pipeline failed in the loading phase: {e}")
                raise
     
