from .models import AdInsightModel, Action 
from datetime import date, datetime 

def get_action_value(actions_list: list, action_type_name: str, default_value: float = 0.0) -> float:
    for action in actions_list:
        if action.get('action_type') == action_type_name:
            try:
                return float(action.get('value', default_value))
            except (ValueError, TypeError): 
                return default_value
    return default_value

def transform_insights(raw_insights: list[dict]) -> list[AdInsightModel]:
    transformed_insights = []
    for raw_insight in raw_insights:
            actions_data = raw_insight.get('actions', []) # all the actions in a single dictionary
       
        # instance of AdInsightModel
            transformed_insight = AdInsightModel(
            id=raw_insight['ad_id'],
            ad_id=raw_insight['ad_id'],
            date_start=datetime.strptime(raw_insight['date_start'], '%Y-%m-%d').date(),
            date_stop=datetime.strptime(raw_insight['date_stop'], '%Y-%m-%d').date(),
            ad_name=raw_insight['ad_name'],
            adset_name=raw_insight['adset_name'],
            campaign_name=raw_insight['campaign_name'],
            objective=raw_insight.get('objective', 'N/A'), 
            optimization_goal=raw_insight.get('optimization_goal', 'N/A'),
            spend=float(raw_insight.get('spend', 0.0)),
            frequency=float(raw_insight.get('frequency', 0.0)),
            reach=int(raw_insight.get('reach', 0)),
            impressions=int(raw_insight.get('impressions', 0)),
            age=raw_insight.get('age', "N/A"),
            gender=raw_insight.get('gender', "N/A"),
            #those attributes are transformed with the function get_action_value
            link_clicks = int(get_action_value(actions_data, 'link_click')),
            post_reactions=int(get_action_value(actions_data, 'post_reaction')),
            pageview_br=int(get_action_value(actions_data, 'offsite_conversion.custom.1352741932244210')),
            pageview_latam=int(get_action_value(actions_data, 'offsite_conversion.custom.165961032929296')),
            comments=int(get_action_value(actions_data, 'comment')),
            post_engagement = int(get_action_value(actions_data, 'post_engagement')),
            page_engagement=int(get_action_value(actions_data, 'page_engagement')),
            shares=int(get_action_value(actions_data, 'post')),
            video_views=int(get_action_value(actions_data, 'video_view')),
        )
            transformed_insights.append(transformed_insight)
    return transformed_insights


