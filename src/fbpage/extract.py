from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookRequestError, Cursor
from fbpage.utils.get_page_token import get_page_token
from dotenv import load_dotenv
from typing import Any, cast, Optional
from utils.get_date import DateUtils
load_dotenv()

INSIGHTS_METRICS = [
    'post_impressions_paid',
    'post_impressions_paid_unique',
    'post_impressions_organic',
    'post_impressions_organic_unique',
    'post_reactions_by_type_total',
    'post_activity_by_action_type',
    'post_clicks_by_type',
]
    

def get_fb_posts_raw_data(fb_page_id: str, time_range: dict) -> list:
    fb_page_token = get_page_token(fb_page_id)
    if not fb_page_token:
        print("Error: Could not retrieve page token. Aborting.")
        return []

    print(f"Extracting Facebook posts from {time_range['since']} to {time_range['until']}")

    page_obj = Page(fb_page_id)

    fields_query = (
        f'published_posts.since({time_range["since"]}).until({time_range["until"]})'
        '{id,created_time,message,permalink_url,'
        f'insights.metric({",".join(INSIGHTS_METRICS)})}}'
    )

    all_posts = []

    try:
        response = page_obj.api_get(params={"fields": fields_query})

        # Force type checker to treat as Any
        response_any: Any = cast(Any, response)

        # fetch posts
        published_posts_cursor = response_any.get("published_posts", {}).get("data", [])
        paging = response_any.get("published_posts", {}).get("paging", {})

        # To iterate with Cursor, just force it as Any
        cursor: Any = published_posts_cursor

        for post in cursor:
            # Each post is already dict; if it were FacebookRequest, use export_all_data()
            if hasattr(post, "export_all_data"):
                post_dict = post.export_all_data()
            else:
                post_dict = post
            all_posts.append(post_dict)

        print(f"Extracted {len(all_posts)} posts with insights.")

        return all_posts

    except FacebookRequestError as e:
        print(f"Facebook API Error: {e.api_error_code} - {e.api_error_message}")
        return []
    except Exception as e:
        print(f"Error while extracting insights from Facebook: {e}")
        return []
    
    
def get_fb_posts_data(fb_page_id: str, 
                        project_id:str, 
                        dataset_id:str, 
                        table_id:str,
                        increment: int = 1,
                        service_account_key_path: Optional[str]=None
                     ) -> list:
    extract_has_data = False
    increment = 1
    while not extract_has_data:
        time_range = DateUtils.get_bq_based_time_range(project_id, dataset_id, table_id,increment,service_account_key_path)
        print(f"Trying to get data for time_range: {time_range}") 
        print("\n", increment)
        print("\n", time_range)

        raw_data = get_fb_posts_raw_data(fb_page_id,time_range)
        
        if len(raw_data) == 0:
            increment = increment + 1
            print(len(raw_data))
            print(f"No data found for increment {increment}. Trying next increment.")
        if len(raw_data) > 0:
            extract_has_data = True
            print(f"Data found for increment {increment}. Extracted {len(raw_data)} records.")
            increment = 1  # Reset increment for next extraction
            return list(raw_data)
        if increment > 50:
            print("\nNo data found multiple tries. Exiting extraction.")
            return []
    # Ensure a list is always returned, even if the loop does not execute
    return []
        