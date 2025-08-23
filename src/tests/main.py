import os
from dotenv import load_dotenv
load_dotenv()
import sys
# Adiciona o diretório-pai ao caminho de busca do Python
# Isso permite importar 'igpage' como um módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils.get_date import DateUtils
from fbpage.utils.get_page_token import get_page_token
from fbpage.init_fb_api import _initialize_facebook_api
from fbpage.extract import get_fb_posts_raw_data

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
    _initialize_facebook_api(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
    page_token = get_page_token(FB_PAGE_ID_PT)
    _initialize_facebook_api(META_APP_ID, META_APP_SECRET, page_token)
    posts = get_fb_posts_raw_data(FB_PAGE_ID_PT, GCP_PROJECT_ID, SOCIAL_DATASET_ID, FB_POSTS_TABLE_ID, GCP_SERVICE_ACCOUNT_KEY_PATH)
    print(f"\nMain script: Extracted {len(posts)} posts.")
    print(posts)
except ValueError as ve:
    print(f"\nMain script: A fatal error occurred during Facebook API initialization: {ve}")
    exit(1) 


