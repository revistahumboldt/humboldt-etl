import os
from dotenv import load_dotenv
load_dotenv()
import sys
# Adiciona o diretório-pai ao caminho de busca do Python
# Isso permite importar 'igpage' como um módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import traceback
from igposts.etl import run_etl

#GCP
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
SOCIAL_DATASET_ID = os.getenv("SOCIAL_DATASET_ID","")
IG_POSTS_TABLE_ID = os.getenv("IG_POSTS_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")

#META
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")

#IG
ES_IG_PAGE_ID = os.getenv("ES_IG_PAGE_ID","")
BR_IG_PAGE_ID = os.getenv("BR_IG_PAGE_ID","")

def verify_env_vars():
    # basic checks and early outputs for debugging
    if not GCP_PROJECT_ID:
        print("CRITICAL ERROR: Environment variable GCP_PROJECT_ID not set. Exiting.")
        return 
    if not SOCIAL_DATASET_ID:
        print("CRITICAL ERROR: Environment variable SOCIAL_DATASET_ID not set. Exiting.")
        return
    if not IG_POSTS_TABLE_ID:
        print("CRITICAL ERROR: Environment variable IG_POSTS_TABLE_ID not set. Exiting.")
        return
    if not META_APP_ID:
        print("CRITICAL ERROR: Environment variable META_APP_ID not set. Exiting.")
        return
    if not META_APP_SECRET:
        print("CRITICAL ERROR: Environment variable META_APP_SECRET not set. Exiting.")
        return
verify_env_vars()

def run_igposts_etl():
    try:
        for page_id in [BR_IG_PAGE_ID, ES_IG_PAGE_ID]:
            print(f"\nMain script: Executing ETL for page: {page_id}")

            run_etl(GCP_PROJECT_ID,
                    SOCIAL_DATASET_ID, 
                    IG_POSTS_TABLE_ID, 
                    page_id, 
                    META_APP_ID, 
                    META_APP_SECRET, 
                    META_ACCESS_TOKEN,
                    GCP_SERVICE_ACCOUNT_KEY_PATH
                    )
    except ValueError as ve:
        print(f"\n run_igpage_etl script: A fatal error occurred during Facebook API initialization: {ve}")
        exit(1) 