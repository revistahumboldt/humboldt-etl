from igpage.models import InstaPageModel
from datetime import date, datetime

def transform_igpage_data(ig_page_raw_insights: list[dict], pageId:str) -> list[InstaPageModel]:
    transformed_insights = []

    for i in range(0, len(ig_page_raw_insights), 3):
        
        # Capturing the dictionaries for the current day
        insight_date_followers = ig_page_raw_insights[i]
        insight_profile_views = ig_page_raw_insights[i+1]
        insight_website_clicks = ig_page_raw_insights[i+2]
    
        # Extracting the date and metrics
        insight_date = insight_date_followers.get('date', "")
        new_followers = insight_date_followers.get('new_followers', 0)
        profile_views = insight_profile_views.get('profile_views', 0)
        website_clicks = insight_website_clicks.get('website_clicks', 0)

        # instance of AdInsightModel
        transformed_insight = InstaPageModel(
            id=str(insight_date).strip()+str(new_followers*2).strip()+str(profile_views*5).strip()+str(website_clicks*5).strip()+str(datetime.now()),
            date=datetime.strptime(insight_date, '%Y-%m-%d').date(),
            follow_count=new_followers,
            profile_views=profile_views,
            website_clicks=website_clicks,
            page_id=pageId,
            last_updated_timestamp=datetime.now()
        )
    
    transformed_insights.append(transformed_insight)
    return transformed_insights
    
   



