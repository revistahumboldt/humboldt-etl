import os
from dotenv import load_dotenv
load_dotenv()
import sys
# Adiciona o diretório-pai ao caminho de busca do Python
# Isso permite importar 'igpage' como um módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from igpage.etl import run_etl

GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
SOCIAL_DATASET_ID = os.getenv("SOCIAL_DATASET_ID","")
FB_POSTS_TABLE_ID = os.getenv("FB_POSTS_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
ETL_TO_RUN = os.getenv("ETL_TO_RUN","")
FB_PAGE_ID_PT = os.getenv("FB_PAGE_ID_PT","")


try:
    run_etl(GCP_PROJECT_ID,
            SOCIAL_DATASET_ID, 
            FB_POSTS_TABLE_ID, 
            FB_PAGE_ID_PT, 
            META_APP_ID, 
            META_APP_SECRET,
            META_ACCESS_TOKEN,
            GCP_SERVICE_ACCOUNT_KEY_PATH
    )
except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 


