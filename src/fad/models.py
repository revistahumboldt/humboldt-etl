from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Model for Facebook Raw Ad Insights (as they come from the API)
#    - Based on Facebook Marketing API response to AdsInsights
# --------------------------------------------------------------------------------

class Action(BaseModel):
    action_type: str
    value: float

class AdInsightModel(BaseModel):
    id: str
    ad_id: str
    date_start: date
    date_stop: date
    ad_name: str
    adset_name: str
    campaign_name: str
    objective: str
    optimization_goal: str
    spend: float
    frequency: float
    reach: int
    impressions: int
    age: str
    gender: str
    link_clicks: int
    post_reactions: int
    pageview_br: int
    pageview_latam: int
    comments: int
    page_engagement: int
    post_engagement: int
    shares: int
    video_views: int 
