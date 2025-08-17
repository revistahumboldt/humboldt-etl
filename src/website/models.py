from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Instagram Social
#    - Based on Facebook Marketing API response to AdsInsights
# --------------------------------------------------------------------------------



class WebPageInsightModel(BaseModel):
    id: str
    title: str
    url: str
    date: date
    location_country: str
    device: int
    page_impressions: int
    pages_entries: int
    visits_bounces: int
    visitors: int
    pages_duration_avg: float
    last_updated_timestamp: datetime 

  


