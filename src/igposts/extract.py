from facebook_business.api import FacebookAdsApi, Cursor
from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.igmedia import IGMedia
from typing import List, Dict, Any, Optional
import sys
from utils.char_utils import CharUtils
from utils.get_date import DateUtils

# Try setting the output encoding to UTF-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
except (IOError, AttributeError):
    pass # Ignore if cannot be reopened

def get_raw_igposts(
    ig_business_account_id: str,
    time_range: Dict[str, str]

) -> List[dict]:

    try:
        ig_user = IGUser(fbid=ig_business_account_id) 
        # Fields we want to search for each post
        fields = [
            IGMedia.Field.id,
            IGMedia.Field.timestamp,
            IGMedia.Field.permalink,
            IGMedia.Field.media_product_type,
            IGMedia.Field.media_type,
            IGMedia.Field.like_count,
            IGMedia.Field.comments_count,
            #saves
            #reach
            #impressions
            #video views
            IGMedia.Field.caption,
            IGMedia.Field.username,
        ]

        # List of insight metrics 
        insights_metrics = [
        'views',
        'comments',
        'likes',
        'saved',
        'shares',
        'total_interactions'
        #'impressions',
        ]
        # Dictionary for date filter parameters

    
        params = {}
        if time_range:
            params['since'] = time_range['since']
            params['until'] = time_range['until']

        ig_posts = []
        ig_posts_insights = []
        processed_ids = set()
        final_posts = []
        
        posts_cursor = ig_user.get_media(fields=fields, params=params)
        if isinstance(posts_cursor, Cursor):
            ig_posts = [post.export_all_data() for post in posts_cursor]
            
            #for each post, we do
            for post in ig_posts:
                #remove invalid chars
                if 'caption' in post:
                    post['caption'] = CharUtils.remove_invalid_chars(post['caption'])

                #17953504346470677
                #17973115214140706
                # get the insights metrics 
                ig_media = IGMedia(post['id'])
                insights_data_cursor = ig_media.get_insights(params={
                    'metric': insights_metrics
                })

                if isinstance(insights_data_cursor, Cursor):
                    
                    for insight_post in insights_data_cursor:
                        
                        # Extrai o ID e o nome do insights
                        insight_id = insight_post['id'][:17]
                        insight_name = insight_post['name']
                        insight_values = insight_post['values'][0]['value']

                        if insight_id not in processed_ids:
                            processed_ids.add(insight_id) 
                            ig_posts_insights.append({
                            'id': insight_id })
                        
                        if insight_id in processed_ids:
                              for item in ig_posts_insights:
                                if item['id'] == insight_id:
                                    item[insight_name] = insight_values
                               
        
        # mapping dictionary
        posts_por_id = {post['id']: post for post in ig_posts}

        for insight in ig_posts_insights:
            insight_id = insight['id']
            
            # Check if the insight ID exists in our dictionary of posts
            if insight_id in posts_por_id:
                # Take the corresponding posting dictionary
                post_correspondente = posts_por_id[insight_id]
                
                # Creates a new copy by combining the two dictionaries
                # It's safer not to modify the originals
                combined_post = {**post_correspondente, **insight}
                
                final_posts.append(combined_post)
        
        return final_posts
                                   

    except Exception as e:
        print(f"Error: {e}")
        return []
    


def get_ig_posts_next_day_data(page_id: str, 
                        gcp_project_id:str, 
                        dataset_id:str, 
                        table_id:str,
                        increment: int = 1,
                        service_account_key_path: Optional[str]=None
                     ) -> list:
    extract_has_data = False
    increment = 1
    
    while not extract_has_data:
        time_range = DateUtils.get_ig_last_day(gcp_project_id, dataset_id, table_id,increment,page_id,service_account_key_path)
        print(f"Trying to get data for time_range: {time_range}") 
        print("\n", increment)
        print("\n", time_range)

        raw_data = get_raw_igposts(page_id, time_range)
        
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