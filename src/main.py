import os
from dotenv import load_dotenv
load_dotenv()
from fad.orchestration import run_etl_pipeline
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
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")

#if delta bt last bq dateand curr date > 28 days 
bq_last_date = DateUtils.get_bq_last_date(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH)

bq_last_date_delta = None

if bq_last_date is not None:
    bq_last_date_dt = datetime.combine(bq_last_date, datetime.min.time())

if (datetime.now()-bq_last_date_dt).days > 28:
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
            DateUtils.get_bq_based_time_range(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, 3), 
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")

#if delta bt last bq dateand curr date < 28 days: get data for the last 28 days 
if (datetime.now()-bq_last_date_dt).days < 28:
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
            DateUtils.get_last_28_days() 
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")








""""
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
            bq_next_2days,  # Default delta_days to 1
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
            bq_next_2days,  # Default delta_days to 1
            GCP_SERVICE_ACCOUNT_KEY_PATH
        )
        print("\nMain script: Pipeline ETL finished.")
    except Exception as e:
        print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")

"""