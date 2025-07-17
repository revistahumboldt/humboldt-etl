# src/facebook_etl/extract.py
import os
from facebook_business.api import FacebookAdsApi
#from facebook_business.objects import AdAccount, Campaign, AdSet, Ad, AdCreative, AdsInsights
import datetime

import facebook_business
from dotenv import load_dotenv

#for item in dir(facebook_business):
load_dotenv()  # Carrega variáveis do .env na raiz do projeto

print(os.getenv('FB_APP_ID'))

print

"""""
# Função para inicializar a API (pode ser chamada uma vez no main ou neste módulo)
def _initialize_facebook_api():
    app_id = os.getenv('FB_APP_ID')
    app_secret = os.getenv('FB_APP_SECRET')
    access_token = os.getenv('FB_ACCESS_TOKEN')
    if not all([app_id, app_secret, access_token]):
        raise ValueError("Credenciais da API do Facebook (FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN) devem ser definidas como variáveis de ambiente.")
    FacebookAdsApi.init(app_id, app_secret, access_token)
    print("Facebook Ads API inicializada.")


_initialize_facebook_api()  # Inicializa a API ao importar o módulo
"""
""""
def extract_ad_insights(ad_account_id: str, date_preset: str = 'yesterday') -> list:
   
    _initialize_facebook_api() # Garante que a API está inicializada

    ad_account = AdAccount(ad_account_id)
    insights_data = []

    # Define os campos que você deseja extrair. Consulte a documentação da API para mais campos.
    fields = [
        AdsInsights.Field.account_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.ad_name,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.reach,
        AdsInsights.Field.date_start,
        AdsInsights.Field.date_stop,
        AdsInsights.Field.actions # Para obter conversões e outros eventos
    ]
    params = {
        'time_increment': 1, # Insights diários
        'date_preset': date_preset, # 'yesterday', 'last_7_days', etc.
        # 'time_range': {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}, # Alternativa a date_preset
        'level': 'ad', # Nível de detalhe (account, campaign, adset, ad)
    }

    print(f"Extraindo insights para a conta {ad_account_id} para o período {date_preset}...")
    try:
        # get_insights() retorna um iterador, que lida com a paginação automaticamente
        insights = ad_account.get_insights(fields=fields, params=params)
        for insight in insights:
            insights_data.append(insight.export_all_data()) # Converte o objeto SDK em dict
        print(f"Extração de insights concluída. Total de registros: {len(insights_data)}")
    except Exception as e:
        print(f"Erro durante a extração de insights do Facebook: {e}")
        raise # Re-levanta para que o main.py possa capturar

    return insights_data

    """
""""
# Você pode adicionar outras funções de extração aqui, ex:
def extract_campaigns(ad_account_id: str) -> list:
    _initialize_facebook_api()
    ad_account = AdAccount(ad_account_id)
    campaigns_data = []
    fields = [Campaign.Field.name, Campaign.Field.status, Campaign.Field.start_time, Campaign.Field.stop_time]
    params = {'effective_status': ['ACTIVE']}
    print(f"Extraindo campanhas ativas para a conta {ad_account_id}...")
    try:
        campaigns = ad_account.get_campaigns(fields=fields, params=params)
        for campaign in campaigns:
            campaigns_data.append(campaign.export_all_data())
        print(f"Extração de campanhas concluída. Total de registros: {len(campaigns_data)}")
    except Exception as e:
        print(f"Erro durante a extração de campanhas do Facebook: {e}")
        raise
    return campaigns_data

# Se você tiver um módulo models.py, pode importar classes de lá para tipagem/validação
# from .models import AdInsightData # Exemplo se você tiver modelos Pydantic
"""
