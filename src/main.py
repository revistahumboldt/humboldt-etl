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
#GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
WINDOW = os.getenv("WINDOW","")

# ---  PRINTS DEBUG ---
#print(f"DEBUG: Verificando variáveis de entrada para orchestrate_etl...")
#print(f"DEBUG: META_AD_ACCOUNT_ID = '{META_AD_ACCOUNT_ID}'")
#print(f"DEBUG: GCP_PROJECT_ID = '{GCP_PROJECT_ID}'")
#print(f"DEBUG: BQ_DATASET_ID = '{BQ_DATASET_ID}'")
#print(f"DEBUG: BQ_TABLE_ID = '{BQ_TABLE_ID}'")
#print(f"DEBUG: WINDOW = '{WINDOW}'")
#print(f"DEBUG: service_account_key_path = '{GCP_SERVICE_ACCOUNT_KEY_PATH}'")
#print(f"DEBUG: Tipo de service_account_key_path = {type(GCP_SERVICE_ACCOUNT_KEY_PATH)}")

def verify_env_vars():
    # verificações básicas e saídas antecipadas para debugging
    if not META_AD_ACCOUNT_ID:
        print("CRITICAL ERROR: Environment variable GCP_PROJECT_ID not set. Exiting.")
        return 
    if not GCP_PROJECT_ID:
        print("CRITICAL ERROR: Environment variable GCP_PROJECT_ID not set. Exiting.")
        return
    if not BQ_DATASET_ID:
        print("CRITICAL ERROR: Environment variable BQ_DATASET_ID not set. Exiting.")
        return
    if not BQ_TABLE_ID:
        print("CRITICAL ERROR: Environment variable BQ_DATASET_ID not set. Exiting.")
        return
    if not WINDOW:
        print("CRITICAL ERROR: Environment variable WINDOW not set. Exiting.")
        return
verify_env_vars()

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
    #service_account_key = GCP_SERVICE_ACCOUNT_KEY_PATH if GCP_SERVICE_ACCOUNT_KEY_PATH and GCP_SERVICE_ACCOUNT_KEY_PATH.strip() else None

    for table_id, breakdown in [(os.getenv("BQ_TABLE_ID1"), os.getenv("BREAKDOWN1")),
                            (os.getenv("BQ_TABLE_ID2"), os.getenv("BREAKDOWN2"))]:
        if table_id and breakdown:
            orchestrate_ad_insights_etl(
            META_AD_ACCOUNT_ID,
            GCP_PROJECT_ID,
            BQ_DATASET_ID,
            table_id,
            WINDOW,
            breakdown,
            META_APP_SECRET,
            META_ACCESS_TOKEN,
            #GCP_SERVICE_ACCOUNT_KEY_PATH
            )
except Exception as e:
    print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
    traceback.print_exc() # Print the full stack trace for more details
    exit(1) 
