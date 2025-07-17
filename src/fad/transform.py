# src/facebook_etl/transform.py
import datetime
# from .models import TransformedAdInsight # Se você tiver modelos para o formato final

def transform_facebook_data(raw_insights: list) -> list:
    """
    Transforma os dados brutos de insights de anúncios do Facebook.
    Args:
        raw_insights: Uma lista de dicionários contendo os dados brutos extraídos.
    Returns:
        Uma lista de dicionários com os dados transformados, prontos para o BigQuery.
    """
    transformed_data = []
    print(f"Iniciando transformação de {len(raw_insights)} registros...")

    for insight in raw_insights:
        transformed_row = {
            'ad_account_id': insight.get('account_id'),
            'campaign_name': insight.get('campaign_name'),
            'adset_name': insight.get('adset_name'),
            'ad_name': insight.get('ad_name'),
            'date': insight.get('date_start'), # BigQuery tipicamente gosta de STRING ou DATE
            'impressions': int(insight.get('impressions', 0)),
            'clicks': int(insight.get('clicks', 0)),
            'spend': float(insight.get('spend', 0.0)),
            'reach': int(insight.get('reach', 0)),
            # Adiciona o timestamp de quando o ETL foi executado
            'etl_load_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        # Lidar com o campo 'actions' que é uma lista de dicionários
        actions = insight.get('actions', [])
        for action in actions:
            action_type = action.get('action_type')
            value = float(action.get('value', 0.0))
            # Exemplo: mapear tipos de ação para colunas específicas
            if action_type == 'lead':
                transformed_row['leads'] = value
            elif action_type == 'offsite_conversion.fb_pixel_purchase':
                transformed_row['purchases'] = value
            # Adicione mais conforme necessário

        # Garantir que colunas não preenchidas existam com valor padrão (ex: 0)
        transformed_row['leads'] = transformed_row.get('leads', 0)
        transformed_row['purchases'] = transformed_row.get('purchases', 0)


        # Calcular CTR (Click-Through Rate)
        if transformed_row['impressions'] > 0:
            transformed_row['ctr'] = (transformed_row['clicks'] / transformed_row['impressions']) * 100
        else:
            transformed_row['ctr'] = 0.0

        transformed_data.append(transformed_row)

    print("Transformação concluída.")
    return transformed_data