import os
import sys
from dotenv import load_dotenv

from fad.run import run_fad_etl
from igpage.run import run_igpage_etl
from igposts.run import run_igposts_etl
load_dotenv()
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
    if ETL_TO_RUN == "fad":
        print(f"\nMain script: Runinng fad etl")
        run_fad_etl()
    if ETL_TO_RUN == "igpage":
        print(f"\nMain script: Runinng igpage etl")
        run_igpage_etl()
    if ETL_TO_RUN == "igposts":
        print(f"\nMain script: Runinng igposts etl")
        run_igposts_etl()
    if ETL_TO_RUN == None or ETL_TO_RUN == "":
        print(f"\nMain script: ETL_TO_RUN variable is not defined")
        sys.exit(1)
except ValueError as ve:
        print(f"\nMain script: A fatal error occurred during {ETL_TO_RUN} script: {ve}")


