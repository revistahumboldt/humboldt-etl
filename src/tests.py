from fad.init_fb_api import _initialize_facebook_api
from utils.get_date import DateUtils
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from fad.extract import get_fb_raw_data, get_next_day_data
import os
load_dotenv()

currentDate = DateUtils.get_current_date() 
last28Days = DateUtils.get_last_28_days() 

META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID", "")  
BQ_DATASET_ID=os.getenv("BQ_DATASET_ID", "")  
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID","")
META_APP_ID = os.getenv("META_APP_ID","")
META_APP_SECRET=os.getenv("META_APP_SECRET","")
META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN","")
GCP_SERVICE_ACCOUNT_KEY_PATH = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH","")






