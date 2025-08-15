from facebook_business.api import FacebookAdsApi, Cursor
from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.igmedia import IGMedia
from typing import List, Dict, Any, Optional
import sys
from utils.char_utils import CharUtils

# Tenta definir a codificação de saída para UTF-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
except (IOError, AttributeError):
    pass # Ignora se não for possível reabrir

def get_raw_igposts(
    ig_business_account_id: str,
    since_date: Optional[str] = None,
    until_date: Optional[str] = None
) -> List[dict]:
    """
    Searches for posts from an Instagram account, filtering by date in the API call.
    Args:
        ig_business_account_id: O ID da conta de negócios do Instagram.
        since_date: Data de início do período, no formato 'YYYY-MM-DD'.
        until_date: Data de fim do período, no formato 'YYYY-MM-DD'.

    Returns:
        Uma lista de dicionários com os dados dos posts filtrados.
    """
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
        if since_date:
            params['since'] = since_date
        if until_date:
            params['until'] = until_date

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
    
    return []

