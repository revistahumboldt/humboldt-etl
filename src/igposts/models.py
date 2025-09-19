from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Instagram Social
#    - Based on Facebook Marketing API response to AdsInsights
# --------------------------------------------------------------------------------



class InstaPostModel(BaseModel):
    id: str
    date: date
    link: str
    media_product_type: str
    media_type: str
    likes: int
    comments: int
    saves: int
    shares: int
    views: int
    impressions: int
    reach: int
    profile_activity: int
    total_interactions: int
    ig_reels_avg_watch_time: int
    ig_reels_video_view_total_time: int
    caption: str
    username: str
    page_id: str
    last_updated_timestamp: datetime 

  


