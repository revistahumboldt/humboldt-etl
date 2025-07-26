import os
from dotenv import load_dotenv
load_dotenv()
from fad.orchestration import orquerstrate_etl
from fad.init_fb_api import _initialize_facebook_api
from utils.get_date import DateUtils
from datetime import datetime, date, timedelta

META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
WINDOW = os.getenv("WINDOW","")

try:
    _initialize_facebook_api(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 

try:
    print(f"\nRunning ETL pipeline for window: {WINDOW}")
    # If it is an empty string (""), Python will treat it as "False" in a boolean context
    # and it will be None for the orquerstrate_etl function if the default is None.
    # It's best to explicitly check if it's an empty string and pass None if necessary.
    service_account_key = GCP_SERVICE_ACCOUNT_KEY_PATH if GCP_SERVICE_ACCOUNT_KEY_PATH and GCP_SERVICE_ACCOUNT_KEY_PATH.strip() else None

    orquerstrate_etl(
        META_AD_ACCOUNT_ID,
        GCP_PROJECT_ID,
        BQ_DATASET_ID,
        BQ_TABLE_ID,
        WINDOW,
        service_account_key 
    )
    print("\nMain script: Pipeline ETL finished.")
except Exception as e:
    print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
    exit(1) 
