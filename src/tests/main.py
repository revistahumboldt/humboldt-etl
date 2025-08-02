import os
from dotenv import load_dotenv
load_dotenv()
import sys

# Adiciona o diretório-pai ao caminho de busca do Python
# Isso permite importar 'igpage' como um módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

#from fad.orchestration import orchestrate_ad_insights_etl
from igpage.init_fb_api import _initialize_facebook_api
import traceback
from igpage.extract import get_instagram_data

META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
#GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
WINDOW = os.getenv("WINDOW","")
BR_IG_PAGE_ID = "17841457253047574"
TIME_RANGE = {'since':'2025-07-20', 'until': '2025-07-28'}

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
    get_instagram_data(BR_IG_PAGE_ID, TIME_RANGE)

except Exception as e:
    print(f"\nMain script: A fatal error occurred in the ETL pipeline: {e}")
    traceback.print_exc() # Print the full stack trace for more details
    exit(1) 
