
from fad.etl import run_etl
from utils.get_date import DateUtils
import sys
import os
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict, Any, Optional

GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")

def orquerstrate_etl(account_id: str,
                     gcp_project_id: str,
                     bq_dataset_id: str, 
                     bq_table_id: str,
                     window:str,
                     service_account_key_path: Optional[str]=None):

    if window == "daily":
        try:
            print("Executing daily ETL")
            daily_time_range = DateUtils.get_time_range(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, 1,GCP_SERVICE_ACCOUNT_KEY_PATH)
            run_etl(account_id,gcp_project_id, bq_dataset_id, bq_table_id, daily_time_range, window, service_account_key_path)
        except Exception as e:
            print("\nError executing daily ETL", e)
            sys.exit(1)

    if window == "last_28_days":
        try:
            last_bq_date = DateUtils.get_bq_last_day(GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH)
            last_28_days = DateUtils.get_last_28_days()
            if last_bq_date is not None:
                delta = DateUtils.get_delta_days(last_bq_date)
                if delta > 3:
                    print("The actual data on bq are not recent. Wait until more fresh data come")
                    sys.exit(0)
                if delta <= 3:
                    print("Executing last 28 days etl - backfill")
                    run_etl(account_id,gcp_project_id, bq_dataset_id, bq_table_id, last_28_days, window)
        except Exception as e:
            print("\nError executing last 28 days etl", e)
            sys.exit(1)



