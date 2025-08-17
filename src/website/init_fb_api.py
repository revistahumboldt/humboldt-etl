from facebook_business.api import FacebookAdsApi

def _initialize_facebook_api(fb_app_id: str, app_secret: str, access_token: str):
    
    try:
        if not all([fb_app_id, app_secret, access_token]):
         raise ValueError("Facebook API credentials (FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN) must be defined as environment variables.")
        FacebookAdsApi.init(fb_app_id, app_secret, access_token)
        print("Facebook Ads API init.")
    except Exception as e:
        print("Error by logging Facebook.")
        print(e)