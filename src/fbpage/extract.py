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
    

def get_fb_posts_raw_data(fb_page_id: str, gcp_project_id:str, gcp_dataset_id: str, gcp_table_id:str, gcp_service_acc_path: str) -> list:
    fb_page_token = get_page_token(fb_page_id)
    if not fb_page_token:
        print("Error: Could not retrieve page token. Aborting.")
        return []

    time_range = DateUtils.get_bq_based_time_range(gcp_project_id,gcp_dataset_id, gcp_table_id, 1, gcp_service_acc_path)
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
