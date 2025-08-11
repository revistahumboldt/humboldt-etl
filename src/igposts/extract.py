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
        
        # Campos que queremos buscar para cada post
        fields = [
            IGMedia.Field.id,
            IGMedia.Field.timestamp,
            IGMedia.Field.like_count,
            IGMedia.Field.comments_count,
            IGMedia.Field.media_url,
            IGMedia.Field.caption,
            IGMedia.Field.media_type
        ]

        # Dictionary for date filter parameters
        params = {}
        if since_date:
            params['since'] = since_date
        if until_date:
            params['until'] = until_date
        
        # Calls the API passing the fields and date parameters
        posts_cursor = ig_user.get_media(fields=fields, params=params)
        if isinstance(posts_cursor, Cursor):
            ig_posts = [post.export_all_data() for post in posts_cursor]
            for post in ig_posts:
                if 'caption' in post:
                    post['caption'] = CharUtils.remove_invalid_chars(post['caption'])
            
            return ig_posts

    except Exception as e:
        print(f"Error: {e}")
        return []
    
    return []

