from dotenv import load_dotenv
from facebook_business.adobjects import adaccount, campaign, adset, ad, adcreative, adsinsights

def extract_ad_insights(ad_account_id: str, date_preset: str = 'yesterday') -> list:
  
    ad_account = adaccount.AdAccount(ad_account_id)
    if not ad_account:
        raise ValueError(f"Ad account with ID {ad_account_id} not found.")   
    insights_data = []

    # Defining the fields we want to extract
    # https://developers.facebook.com/docs/marketing-api/insights/reference
    fields = [
    'ad_id',
    'campaign_name',
    'adset_name',
    'ad_name',
    'frequency',
    'spend',
    'reach',
    'impressions', 
    'objective',
    "optimization_goal",
    "clicks",
    "actions"
]
    
    # parameter dictionary
    params = {
        'time_increment': 7, # daily nsights 
        'date_preset': date_preset, # 'yesterday', 'last_7_days', etc.
        # 'time_range': {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}, # Alternative to date_preset
        'level': 'ad', # level (account, campaign, adset, ad)
        'breakdowns': ['age', 'gender'],       
        'action_breakdowns': ['action_type']  
    }

    print(f"Extracting insights for the account {ad_account_id} for the period {date_preset}...")
    try:
        # get_insights() returns an iterator, which handles pagination automatically
        # insights is a list of dictionaries
        insights = ad_account.get_insights(fields=fields, params=params)
        print("Successful insights data.")
        #first_insight = next(insights, None) # None' is a default value if the cursor is empty
        #print(first_insight)

        for insight in insights:
           #print(insight)
           insights_data.append(insight)
    except Exception as e:
        print(f"Error while extracting insights from Facebook: {e}")
        raise # Re-raise so that main.py can capture

    return insights_data

