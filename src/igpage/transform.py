from igpage.models import InstaPageModel
from datetime import date, datetime

def transform_igpage_data(ig_page_raw_insights: list[dict], pageId:str) -> list[InstaPageModel]:
        transformed_insights = []

        # Capturing the dictionaries for the current day
        insight_date_followers = ig_page_raw_insights[0]
        insight_profile_views = ig_page_raw_insights[2]['website_clicks']
        insight_website_clicks = ig_page_raw_insights[1]['profile_views']
    
        # Extracting the date and metrics
        insight_date = insight_date_followers['date']
        new_followers = insight_date_followers['new_followers']
        print(f"Date: {insight_date}, New Followers: {new_followers}, Profile Views: {insight_profile_views}, Website Clicks: {insight_website_clicks}")
        
        # instance of AdInsightModel
        transformed_insight = InstaPageModel(
            id=str(insight_date).strip()+str(new_followers*2).strip()+str(insight_profile_views*5).strip()+str(insight_website_clicks*5).strip()+str(datetime.now()),
            date=datetime.strptime(insight_date, '%Y-%m-%d').date(),
            follow_count=new_followers,
            profile_views=insight_profile_views,
            website_clicks=insight_website_clicks,
            page_id=pageId,
            last_updated_timestamp=datetime.now()
        )
        
    
        transformed_insights.append(transformed_insight)
        return transformed_insights
    
   



