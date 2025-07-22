import os
from dotenv import load_dotenv
load_dotenv()
from fad.orchestration import run_etl_pipeline
from fad.init_fb_api import _initialize_facebook_api

META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")


if GCP_SERVICE_ACCOUNT_KEY_PATH == None or GCP_SERVICE_ACCOUNT_KEY_PATH == "":
    try:
        _initialize_facebook_api(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
    except ValueError as ve:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {ve}")
    try:
        run_etl_pipeline(
            META_AD_ACCOUNT_ID,
            GCP_PROJECT_ID,
            BQ_DATASET_ID,
            BQ_TABLE_ID,
            1,  # Default delta_days to 1
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
    

if GCP_SERVICE_ACCOUNT_KEY_PATH != None or GCP_SERVICE_ACCOUNT_KEY_PATH != "":
    try:
        _initialize_facebook_api(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
    except ValueError as ve:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {ve}")
    try:
        print("Running ETL pipeline with service account key path:")
        print(GCP_SERVICE_ACCOUNT_KEY_PATH)
        run_etl_pipeline(
            META_AD_ACCOUNT_ID,
            GCP_PROJECT_ID,
            BQ_DATASET_ID,
            BQ_TABLE_ID,
            1,  # Default delta_days to 1
            GCP_SERVICE_ACCOUNT_KEY_PATH
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
