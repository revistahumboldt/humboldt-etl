from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Website
#    - Based on Mapp Standard Fields
# --------------------------------------------------------------------------------
class WebPageInsightModel(BaseModel):
    id: str
    registered_date: date
    title: str
    url: str
    location_country: str
    device: int
    page_impressions: int
    pages_entries: int
    pages_exits: int
    bounces: int
    clicks: int
    pages_duration_avg: float
    count_scrolldepth: float
    scrolldepth_50: float
    scrolldepth_abs: float
    last_updated_timestamp: datetime 

  


