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

#GCP
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
IG_DATASET_ID = os.getenv("IG_DATASET_ID","")
IG_PAGE_TABLE_ID = os.getenv("IG_PAGE_TABLE_ID","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")

#META
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")

#IG
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


from igposts.extract import get_raw_igposts
from fad.init_fb_api import _initialize_facebook_api

META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
ETL_TO_RUN = os.getenv("ETL_TO_RUN","")



try:
    _initialize_facebook_api(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 
try:
    # Exemplo de uso
    ig_posts = get_raw_igposts(
        '17841457253047574',
        since_date='2023-08-21', 
        until_date='2023-08-22'
    )

  
    print(ig_posts)
    

   
except ValueError as ve:
    print("Erro", ve)


""""
try:
    if ETL_TO_RUN == "fad":
        print(f"\nMain script: Runinng fad etl")
        run_fad_etl()
    if ETL_TO_RUN == "igpage":
        print(f"\nMain script: Runinng igpage etl")
        run_igpage_etl()
    if ETL_TO_RUN == None or ETL_TO_RUN == "":
        print(f"\nMain script: ETL_TO_RUN variable is not defined")
        sys.exit(1)
except ValueError as ve:
        print(f"\nMain script: A fatal error occurred during {ETL_TO_RUN} script: {ve}")
"""

