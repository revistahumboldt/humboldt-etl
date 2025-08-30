import os
from dotenv import load_dotenv
load_dotenv()
from fad.orchestration import orchestrate_ad_insights_etl
from fad.init_fb_api import _initialize_facebook_api
import traceback

META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")


def run_fad_etl():
    try:
        print(f"\n run_fad_etl: Running ETL pipeline for facebook posts")
    # If it is an empty string (""), Python will treat it as "False" in a boolean context
    # and it will be None for the orquerstrate_etl function if the default is None.
    # It's best to explicitly check if it's an empty string and pass None if necessary.
    #service_account_key = GCP_SERVICE_ACCOUNT_KEY_PATH if GCP_SERVICE_ACCOUNT_KEY_PATH and GCP_SERVICE_ACCOUNT_KEY_PATH.strip() else None

        for table_id, breakdown in [(os.getenv("BQ_TABLE_ID1"), os.getenv("BREAKDOWN1")),
                                (os.getenv("BQ_TABLE_ID2"), os.getenv("BREAKDOWN2"))]:
            if table_id and breakdown:
                orchestrate_ad_insights_etl(
                META_AD_ACCOUNT_ID,
                GCP_PROJECT_ID,
                BQ_DATASET_ID,
                table_id,
                "WINDOW",
                breakdown,
                META_APP_SECRET,
                META_ACCESS_TOKEN,
                #GCP_SERVICE_ACCOUNT_KEY_PATH
                )
    except Exception as e:
        print(f"\n run_fad_etl script: A fatal error occurred in the ETL pipeline: {e}")
        traceback.print_exc() # Print the full stack trace for more details
        exit(1) 