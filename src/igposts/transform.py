from igposts.models import InstaPostModel
from datetime import date, datetime

def transform_igposts_data(ig_posts_raw_data: list[dict], page_id:str) -> list[InstaPostModel]:
    transformed_insights = []

    for i in range(0, len(ig_posts_raw_data), 3):

        # instance of AdInsightModel
        transformed_insight = InstaPostModel(
            id=ig_posts_raw_data[i]['id'],
            date=ig_posts_raw_data[i]['timestamp'][:10],
            link=ig_posts_raw_data[i]['permalink'],
            media_product_type=ig_posts_raw_data[i]['media_product_type'],
            media_type=ig_posts_raw_data[i]['media_type'],
            likes=ig_posts_raw_data[i]['like_count'],
            comments=ig_posts_raw_data[i]['comments_count'],
            saves=ig_posts_raw_data[i]['saved'],
            shares=ig_posts_raw_data[i]['shares'],
            views=ig_posts_raw_data[i]['views'],
            caption=ig_posts_raw_data[i]['caption'],
            username=ig_posts_raw_data[i]['username'],
            page_id=page_id,
            last_updated_timestamp=datetime.now()
        )
    
    transformed_insights.append(transformed_insight)
    return transformed_insights
    
   



