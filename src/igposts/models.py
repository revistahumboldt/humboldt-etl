from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Instagram Social
#    - Based on Facebook Marketing API response to AdsInsights
# --------------------------------------------------------------------------------



class InstaPostModel(BaseModel):
    id: str
    timestamp: date
    link: str
    media_product_type: str
    media_type: str
    likes: int
    comments: int
    saves: int
    reach: int
    impressions: int
    video_views: int
    caption: str
    username: int
    last_updated_timestamp: datetime 

  


