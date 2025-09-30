from facebook_business.api import FacebookAdsApi, Cursor, FacebookRequest
from facebook_business.adobjects.iguser import IGUser
from facebook_business.exceptions import FacebookRequestError
from typing import Dict, Any, List
from utils.get_date import DateUtils
from typing import List, Dict, Any, Optional


def get_igpage_raw_data(ig_business_account_id: str, 
                               time_range: Dict[str, str]
                              ) -> List[dict]:
 
    if not ig_business_account_id or not time_range:
        print("Error: Essential parameters not supplied.")
        return []

    params_ts = {
        'metric': 'follower_count',
        #'metric': 'follows_and_unfollows',
        'period': 'day',
        'since': time_range['since'],
        'until': time_range['until'],
    }
    
    params_tv = {
        'metric': 'profile_views,website_clicks',
        'period': 'day', 
        'metric_type': 'total_value',
        'since': time_range['since'],
        'until': time_range['until'],
    }

    final_results = []

    try:
        ig_user = IGUser(fbid=ig_business_account_id)
        
        # --- Auxiliary function to deal with SDK inconsistency ---
        def execute_if_needed(request_or_cursor):
            if isinstance(request_or_cursor, FacebookRequest):
                # If it's a Request, run it to get the Cursor
                return request_or_cursor.execute()
            # If it is already a Cursor, return it directly
            return request_or_cursor

        # --- 1. TIME SERIES data search ---
        print("Searching for daily variation in followers...")
        response_ts = ig_user.get_insights(params=params_ts)
        insights_ts_cursor = execute_if_needed(response_ts)

        if len(insights_ts_cursor) == 0:
            final_results.append({'follow_count': [{'date': params_ts['since'], 'new_followers': 0}]})

        for insight in insights_ts_cursor:
            daily_values = insight.get('values', [])
            for entry in daily_values:
                final_results.append({
                    "date": entry['end_time'].split('T')[0],
                    "new_followers": entry['value']
                })

        # --- 2. TOTAL VALUE data search ---
        print("Getting data for profile_views and website_clicks...")
        response_tv = ig_user.get_insights(params=params_tv)
        insights_tv_cursor = execute_if_needed(response_tv)

        if len(insights_tv_cursor) == 0:
            final_results.append({'website_clicks':0})
            final_results.append({'profile_views':0})

        for insight in insights_tv_cursor:
            metric_name = insight.get('name')
            total_value = insight['total_value'].get('value')
            final_results.append({metric_name: total_value})
        
        print("\nData extraction successfully completed.")
        return final_results

    except FacebookRequestError as e:
        print(f"Facebook API error: {e.api_error_message()}")
        print(f"Error code: {e.api_error_code()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []



def get_ig_page_next_day_data(ig_account_id: str, 
                        gcp_project_id:str, 
                        ig_dataset_id:str, 
                        ig_table_id:str,
                        increment: int = 1,
                        service_account_key_path: Optional[str]=None
                     ) -> list:
    extract_has_data = False
    increment = 1
    
    while not extract_has_data:
        time_range = DateUtils.get_ig_last_day(gcp_project_id, ig_dataset_id, ig_table_id,increment,ig_account_id,service_account_key_path)
        print(f"Trying to get data for time_range: {time_range}") 
        print("\n", increment)
        print("\n", time_range)

        raw_data = get_igpage_raw_data(ig_account_id, time_range)
        
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
        