from fad.extract import extract_ad_insights
from fad.transform import transform_insights
from fad.load import load_data_to_bigquery
from google.cloud import bigquery # Importar bigquery para usar WriteDisposition

def run_etl_pipeline(account_id: str, date_preset: str, 
                     gcp_project_id: str ,
                     bq_dataset_id: str, bq_table_id: str, bq_service_account_key_path: str):
    print(f"Starting an ETL pipeline for an account {account_id} for period {date_preset}...")

    # 1. Extracting
    print("1. Extracting data from Facebook Ads...")
    raw_insights = extract_ad_insights(account_id, date_preset)
    print(f"Extracted {len(raw_insights)} items.")

    # 2. Transformação
    print("2. Data transformation...")
    transformed_insights = transform_insights(raw_insights)
    print(f"Transformation applied on {len(transformed_insights)} items.")

    if not transformed_insights:
        print("No transformed data to load. Closing the pipeline.")
        return

    # 3. Carregamento no BigQuery
    print("3. Loading data into BigQuery...")
    try:
        load_data_to_bigquery(
            transformed_insights,
            gcp_project_id,
            bq_dataset_id,
            bq_table_id,
            # Passa o caminho da chave. Será None se não estiver no .env ou ambiente da CF.
            service_account_key_path=bq_service_account_key_path, 
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        print("ETL pipeline successfully completed!")
    except Exception as e:
        print(f"ETL pipeline failed in the loading phase: {e}")
        raise

