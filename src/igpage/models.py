from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Instagram Social
#    - Based on Facebook Marketing API response to AdsInsights
# --------------------------------------------------------------------------------



class InstaPageModel(BaseModel):
    id: str
    date: date
    follow_count: int
    profile_views: int
    website_clicks: str
    page_id: str
  


