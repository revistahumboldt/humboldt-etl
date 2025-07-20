from fad.extract import extract_ad_insights
from fad.transform import transform_insights
from fad.load import load_data_to_bigquery
from google.cloud import bigquery # Importar bigquery para usar WriteDisposition
from utils.get_bq_last_date import get_bq_last_date

import os
from dotenv import load_dotenv
load_dotenv()

GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")

def run_etl_pipeline(account_id: str,
                     gcp_project_id: str ,
                     bq_dataset_id: str, bq_table_id: str, bq_service_account_key_path: str):
    print(f"Starting an ETL pipeline for an account {account_id} for period {get_bq_last_date(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH)}...")

    # 1. Extracting
    print("1. Extracting data from Facebook Ads...")
    raw_insights = extract_ad_insights(account_id)
    print(f"Extracted {len(raw_insights)} items.")

    
    # 2. Transformação
    print("2. Data transformation...")
    transformed_insights = transform_insights(raw_insights)
    print(f"Transformation applied on {len(transformed_insights)} items.")

    if not transformed_insights:
        print("No transformed data to load. Closing the pipeline.")
        return

    # 3. Carregamento no BigQuery
    print("3. Loading data into BigQuery...")
    try:
        load_data_to_bigquery(
            transformed_insights,
            gcp_project_id,
            bq_dataset_id,
            bq_table_id,
            bq_service_account_key_path, 
        )
        print("ETL pipeline successfully completed!")
    except Exception as e:
        print(f"ETL pipeline failed in the loading phase: {e}")
        raise

