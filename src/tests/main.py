import os
from dotenv import load_dotenv

from website.extract import get_mapp_data


load_dotenv()
import sys
# Adiciona o diretório-pai ao caminho de busca do Python
# Isso permite importar 'igpage' como um módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils.get_date import DateUtils

import traceback
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
IG_DATASET_ID = os.getenv("IG_DATASET_ID","")
IG_PAGE_TABLE_ID = os.getenv("IG_PAGE_TABLE_ID","")
IG_POSTS_TABLE_ID = os.getenv("IG_POSTS_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")
MAPP_DATASET_ID = os.getenv("MAPP_DATASET_ID","")
MAPP_TABLE_ID = os.getenv("MAPP_TABLE_ID","")

try:
    get_mapp_data(GCP_PROJECT_ID, MAPP_DATASET_ID, MAPP_TABLE_ID, 2,GCP_SERVICE_ACCOUNT_KEY_PATH)



except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 


