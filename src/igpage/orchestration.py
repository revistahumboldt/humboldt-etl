from fad.etl import run_etl
from utils.get_date import DateUtils
import sys
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict, Any, Optional
import traceback

def orchestrate_ad_insights_etl(account_id: str,
                                gcp_project_id: str,
                                bq_dataset_id: str,
                                bq_table_id: str,
                                window: str,
                                breakdown: str,
                                meta_app_secret: str,
                                meta_access_token: str,
                                service_account_key_path: Optional[str] = None):

    
    print(f"DEBUG: >>> ENTERED orchestrate_ad_insights_etl function for window: '{window}' <<<")
    window_handled = False 

    if window == "daily":
        window_handled = True 
        try:
            print("Executing daily ETL")
            daily_time_range = DateUtils.get_time_range(
                gcp_project_id,
                bq_dataset_id,
                bq_table_id,
                1,
                service_account_key_path
            )
            print(f"DEBUG: Daily time range determined: {daily_time_range}")
            run_etl(
                account_id,
                gcp_project_id,
                bq_dataset_id,
                bq_table_id,
                daily_time_range,
                window,
                breakdown,
                meta_app_secret,
                meta_access_token,
                service_account_key_path
            )
            print("Daily ETL completed successfully.")
        except Exception as e:
            print(f"\nError executing daily ETL: {e}")
            traceback.print_exc()
            sys.exit(1)

    if window == "last_28_days":
        window_handled = True 
        try:
            print("Executing last 28 days ETL - backfill logic")
            last_bq_date = DateUtils.get_bq_last_day(gcp_project_id, bq_dataset_id, bq_table_id, service_account_key_path)
            last_28_days_range = DateUtils.get_last_28_days()

            if last_bq_date is not None:
                delta = DateUtils.get_delta_days(last_bq_date)
                if delta > 3:
                    print("The actual data on BQ is not recent enough. Waiting for fresher data.")
                    sys.exit(0)
                else: # delta <= 3
                    print("Performing backfill for last 28 days as data is recent or needs update.")
                    run_etl(
                    account_id,
                    gcp_project_id,
                    bq_dataset_id,
                    bq_table_id,
                    last_28_days_range,
                    window,
                    breakdown,
                    meta_app_secret,
                    meta_access_token,
                    )
            else: # last_bq_date is None
                print("BigQuery table seems empty or has no recent data. Running initial backfill for last 28 days.")
                run_etl(
                    account_id,
                    gcp_project_id,
                    bq_dataset_id,
                    bq_table_id,
                    last_28_days_range,
                    window,
                    breakdown,
                    meta_app_secret,
                    meta_access_token,
                    service_account_key_path
                )
            print("Last 28 days ETL completed successfully.")
        except Exception as e:
            print(f"\nError executing last 28 days ETL: {e}")
            traceback.print_exc()
            sys.exit(1)

   
    if not window_handled:
        print(f"\nError: Window '{window}' is not recognized. Supported values are 'daily' or 'last_28_days'.")
        sys.exit(1)