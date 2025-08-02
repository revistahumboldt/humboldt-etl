from facebook_business.api import FacebookAdsApi, Cursor, FacebookRequest
from facebook_business.adobjects.iguser import IGUser
from facebook_business.exceptions import FacebookRequestError
from typing import Dict, Any, List

def get_instagram_data(ig_business_account_id: str, 
                               time_range: Dict[str, str]
                              ) -> List[dict]:
 
    if not ig_business_account_id or not time_range:
        print("Erro: Parâmetros essenciais não foram fornecidos.")
        return []

    params_ts = {
        'metric': 'follower_count',
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
        
        # --- Função auxiliar para lidar com a inconsistência do SDK ---
        def execute_if_needed(request_or_cursor):
            if isinstance(request_or_cursor, FacebookRequest):
                # Se for um Request, execute para obter o Cursor
                return request_or_cursor.execute()
            # Se já for um Cursor, retorne-o diretamente
            return request_or_cursor

        # --- 1. Busca de dados de SÉRIE TEMPORAL ---
        print("Buscando variação diária de seguidores...")
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

        # --- 2. Busca de dados de VALOR TOTAL ---
        print("Buscando totais do período para profile_views e website_clicks...")
        response_tv = ig_user.get_insights(params=params_tv)
        insights_tv_cursor = execute_if_needed(response_tv)

        if len(insights_tv_cursor) == 0:
            final_results.append({'website_clicks':0})
            final_results.append({'profile_views':0})

        for insight in insights_tv_cursor:
            metric_name = insight.get('name')
            total_value = insight['total_value'].get('value')
            final_results.append({metric_name: total_value})
        
        print("\nExtração de dados concluída com sucesso.")
        print(insights_ts_cursor)
        print(insights_tv_cursor)
        print(final_results)
        return final_results

    except FacebookRequestError as e:
        print(f"Facebook API error: {e.api_error_message()}")
        print(f"Error code: {e.api_error_code()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []

