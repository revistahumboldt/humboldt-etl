from igposts.models import InstaPostModel
from datetime import date, datetime

def transform_igposts_data(ig_posts_raw_data: list[dict], page_id:str) -> list[InstaPostModel]:
    transformed_insights = []

    for post in ig_posts_raw_data:
        transformed_insight = InstaPostModel(
            id=post['id'],
            date=post['timestamp'][:10],
            link=post['permalink'],
            media_product_type=post['media_product_type'],
            media_type=post['media_type'],
            likes=post['like_count'],
            comments=post['comments_count'],
            saves=post.get('saved', 0),
            shares=post.get('shares', 0),
            views=post.get('views', 0),
            caption = post.get('caption', ""),
            username = post.get('username', ""),
            page_id=page_id,
            last_updated_timestamp=datetime.now()
        )
        transformed_insights.append(transformed_insight)
    
    return transformed_insights

   



