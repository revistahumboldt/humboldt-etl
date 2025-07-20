import os
from dotenv import load_dotenv
from fad.orchestration import run_etl_pipeline
load_dotenv()
from fad.init_fb_api import _initialize_facebook_api

AD_ACCOUNT_ID=os.getenv("AD_ACCOUNT_ID")
GCP_PROJECT_ID=os.getenv("DATASET_ID")  
BQ_DATASET_ID=os.getenv("GCP_PROJECT_ID")  
BQ_TABLE_ID = os.getenv("GCP_PROJECT_ID")
GCP_SERVICE_ACCOUNT_KEY_PATH = "C:/projetos/humboldt-etl/humboldt-gcp.json"
FB_APP_ID = os.getenv("GCP_PROJECT_ID")
APP_SECRET=os.getenv("GCP_PROJECT_ID")
ACCESS_TOKEN=os.getenv("GCP_PROJECT_ID")


if __name__ == '__main__':

    try:
        _initialize_facebook_api(FB_APP_ID, APP_SECRET, ACCESS_TOKEN)
    except ValueError as ve:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {ve}")
    try:
   
        run_etl_pipeline(
            AD_ACCOUNT_ID,
            GCP_PROJECT_ID,
            BQ_DATASET_ID,
            BQ_TABLE_ID,
            GCP_SERVICE_ACCOUNT_KEY_PATH
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
