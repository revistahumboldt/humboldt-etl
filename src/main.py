import os
from dotenv import load_dotenv
from fad.orchestration import run_etl_pipeline
load_dotenv()
from fad.init_fb_api import _initialize_facebook_api

FB_APP_ID = ""
APP_SECRET = ""
APP_SECRET = ""
ACCOUNT_ID = ""
GCP_PROJECT_ID = ""
BQ_DATASET_ID = ""
BQ_TABLE_ID = ""
GCP_SERVICE_ACCOUNT_KEY_PATH = ""


if __name__ == '__main__':
    print(ACCOUNT_ID)

    try:
        _initialize_facebook_api(FB_APP_ID, APP_SECRET, APP_SECRET)
    except ValueError as ve:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
    try:
    
        run_etl_pipeline(
            ACCOUNT_ID,
            'yesterday',
            GCP_PROJECT_ID,
            BQ_DATASET_ID,
            BQ_TABLE_ID,
            GCP_SERVICE_ACCOUNT_KEY_PATH
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
