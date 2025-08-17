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
from website.etl import run_etl

#GCP
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
MAPP_DATASET_ID = os.getenv("MAPP_DATASET_ID","")
MAPP_TABLE_ID = os.getenv("MAPP_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")


def verify_env_vars():
    # verificações básicas e saídas antecipadas para debugging
    if not GCP_PROJECT_ID:
        print("CRITICAL ERROR: Environment variable GCP_PROJECT_ID not set. Exiting.")
        return 
    if not MAPP_DATASET_ID:
        print("CRITICAL ERROR: Environment variable IG_DATASET_ID not set. Exiting.")
        return
    if not MAPP_TABLE_ID:
        print("CRITICAL ERROR: Environment variable IG_POSTS_TABLE_ID not set. Exiting.")
        return
verify_env_vars()

def run_website_etl():
    try:
        print(f"\nMain script: Executing ETL for page:")

        run_etl(GCP_PROJECT_ID,
                MAPP_DATASET_ID, 
                MAPP_TABLE_ID, 
                GCP_SERVICE_ACCOUNT_KEY_PATH
                    )
    except ValueError as ve:
        print(f"\n run_igpage_etl script: A fatal error occurred: {ve}")
        exit(1) 