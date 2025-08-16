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
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
IG_DATASET_ID = os.getenv("IG_DATASET_ID","")
IG_PAGE_TABLE_ID = os.getenv("IG_PAGE_TABLE_ID","")
IG_POSTS_TABLE_ID = os.getenv("IG_POSTS_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
ES_IG_PAGE_ID = os.getenv("ES_IG_PAGE_ID","")
BR_IG_PAGE_ID = os.getenv("BR_IG_PAGE_ID","")

def verify_env_vars():
    # verificações básicas e saídas antecipadas para debugging
    if not GCP_PROJECT_ID:
        print("CRITICAL ERROR: Environment variable GCP_PROJECT_ID not set. Exiting.")
        return 
    if not IG_DATASET_ID:
        print("CRITICAL ERROR: Environment variable IG_DATASET_ID not set. Exiting.")
        return
    if not IG_PAGE_TABLE_ID:
        print("CRITICAL ERROR: Environment variable IG_PAGE_TABLE_ID not set. Exiting.")
        return
    if not META_APP_ID:
        print("CRITICAL ERROR: Environment variable META_APP_ID not set. Exiting.")
        return
    if not META_APP_SECRET:
        print("CRITICAL ERROR: Environment variable META_APP_SECRET not set. Exiting.")
        return
verify_env_vars()

from igposts.etl import run_etl
from utils.get_date import DateUtils


try:
    run_etl(GCP_PROJECT_ID, IG_DATASET_ID, IG_POSTS_TABLE_ID, BR_IG_PAGE_ID, META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN,GCP_SERVICE_ACCOUNT_KEY_PATH)




except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 


