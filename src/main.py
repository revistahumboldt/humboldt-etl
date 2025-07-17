# Exemplo de main.py
from fad_etl.extract import extract_data_from_facebook
from fad_etl.transform import transform_facebook_data
from bigquery_loader.load import load_data_to_bigquery
import os
import json # Se usar config.json ou yaml

def main():

    print("Iniciando o pipeline ETL do Facebook para BigQuery...")
    """"
    # 1. Extração
    print("Extraindo dados do Facebook...")
    raw_data = extract_data_from_facebook(
        app_id=os.getenv('FB_APP_ID'),
        app_secret=os.getenv('FB_APP_SECRET'),
        access_token=os.getenv('FB_ACCESS_TOKEN'),
        ad_account_id=os.getenv('FB_AD_ACCOUNT_ID')
    )
    print(f"Extraídos {len(raw_data)} registros do Facebook.")

    # 2. Transformação
    print("Transformando os dados...")
    transformed_data = transform_facebook_data(raw_data)
    print(f"Dados transformados: {len(transformed_data)} registros.")

    # 3. Carga
    print("Carregando dados para o BigQuery...")
    load_data_to_bigquery(
        data=transformed_data,
        project_id=os.getenv('GCP_PROJECT_ID'), # ou 'humboldt-385013'
        dataset_id=os.getenv('BQ_DATASET_ID', 'facebook_ads_data'),
        table_id=os.getenv('BQ_TABLE_ID', 'ad_insights')
    )
    print("Carga no BigQuery concluída com sucesso."
    """

#if __name__ == "__main__":
 #   main()

