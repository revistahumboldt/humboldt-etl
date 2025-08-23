from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Facebook Raw Facebook Posts (as they come from the API)
#    - Based on Facebook Marketing API response 
# --------------------------------------------------------------------------------

class Action(BaseModel):
    action_type: str
    value: float

class FacePostsModel(BaseModel):
    id: str
    id_page: str
    created_time: datetime
    post_impressions_paid: int
    post_impressions_paid_unique: int
    post_impressions_organic: int
    post_impressions_organic_unique: int
    likes: int
    shares: int
    comments: int
    others_clicks: int
    photo_clicks: int
    link_clicks: int
    caption: str
    url: str
   