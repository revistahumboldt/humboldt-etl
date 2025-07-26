from google.cloud import bigquery 
from utils.bq_auth import AuthUtils
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from typing import List, Dict, Any, Optional
from .models import AdInsightModel
from .schema import ad_insights_schema
from datetime import date, datetime
import json 

def load_data_to_bigquery(
    data: List[AdInsightModel],
    project_id: str,
    dataset_id: str,
    table_id: str,
    window_type: str, 
    service_account_key_path: Optional[str]=None
) -> Optional[bigquery.LoadJob]:

    # 1. Authentication
    client = AuthUtils.bq_authenticate(project_id, service_account_key_path)

    # 2. Check/verify dataset
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset '{dataset_id}' exists.")
    except NotFound:
        print(f"Dataset '{dataset_id}' not found. Creating one...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "southamerica-east1"
        try:
            client.create_dataset(dataset)
            print(f"Dataset '{dataset_id}' created.")
        except Exception as e:
            print(f"Error creating dataset '{dataset_id}': {e}")
            raise

    # 3. Creating table (if not exists)
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=ad_insights_schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date_start", 
        expiration_ms=None
    )
    table.clustering_fields = ["ad_id", "campaign_name"] 

    try:
        client.get_table(table_ref)
        print(f"Table '{table_id}' already exists in dataset '{dataset_id}'.")
    except NotFound:
        print(f"Table '{table_id}' not found. Creating a new one with defined schema...")
        try:
            client.create_table(table)
            print(f"Table '{table_id}' created")
        except Exception as e:
            print(f"Error creating table '{table_id}': {e}")
            raise

    # 4. Preparing data for loading
    json_data = [item.model_dump(mode='json') for item in data]

    if not json_data:
        print("No data to load. Ending the loading job.")
        return None

    # --- MERGE ---
    # For MERGE, we load all the data into a temporary table.
    # The name of the temporary table must be unique per run.
    temp_table_id = f"{table_id}_temp_{client.project}_{dataset_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    temp_table_ref = client.dataset(dataset_id).table(temp_table_id)

    # Configuration for loading into the temporary table
    temp_load_job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema=ad_insights_schema, 
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Always truncate the temp table before loading.
    )

    try:
        print(f"Loading {len(json_data)} records into temporary table: {temp_table_ref.path}")
        load_temp_job = client.load_table_from_json(
            json_data, temp_table_ref, job_config=temp_load_job_config
        )
        load_temp_job.result() # Wait for the temp table to load
        print(f"Data loaded to temporary table {temp_table_id}. Total rows: {load_temp_job.output_rows}")

        # Defining the columns to be updated/inserted.
        # These are the columns that may change over time or that you always want to be the most recent.
        # We exclude primary keys or columns that should not be updated.
        update_cols = [
             # Metrics
            "spend",
            "frequency",
            "reach",
            "impressions",
            "link_clicks",
            "post_reactions",
            "pageview_br",
            "pageview_latam",
            "comments",
            "page_engagement",
            "post_engagement",
            "shares",
            "video_views",
        ]
        update_statements = ", ".join([f"T.{col} = S.{col}" for col in update_cols])
        insert_cols = ", ".join([f"T.{field.name}" for field in ad_insights_schema])
        insert_values = ", ".join([f"S.{field.name}" for field in ad_insights_schema])

        # 5. Perform the MERGE (UPSERT) operation
        # Important: The ON clause must identify a row ONLY.
        # It is usually made up of the ID (ad_id) and the date (date_start).
        merge_query = f"""
        MERGE INTO `{project_id}.{dataset_id}.{table_id}` T
        USING `{project_id}.{dataset_id}.{temp_table_id}` S
        ON 
        T.ad_id = S.ad_id AND 
        T.date_start = S.date_start AND
        T.ad_name = S.ad_name AND
        T.adset_name = S.adset_name AND
        T.campaign_name = S.campaign_name AND
        T.optimization_goal = S.optimization_goal AND
        T.age = S.age AND
        T.gender = S.gender
        WHEN MATCHED THEN
            UPDATE SET
                {update_statements},
                T.last_updated_timestamp = CURRENT_TIMESTAMP() -- Adicione um campo para rastrear a última atualização
        WHEN NOT MATCHED BY TARGET THEN
            INSERT ({insert_cols}, last_updated_timestamp) -- Inclua last_updated_timestamp aqui também
            VALUES ({insert_values}, CURRENT_TIMESTAMP());
        """


        print(f"Executing MERGE query from {temp_table_id} to {table_id}...")
        query_job = client.query(merge_query)
        query_job.result() # Awaiting completion of MERGE query
        print("MERGE operation completed successfully.")

        # 6. Delete the temporary table
        client.delete_table(temp_table_ref)
        print(f"Temporary table {temp_table_id} deleted.")

        return load_temp_job # Returns the temporary loading job or a success status

    except Exception as e:
        print(f"Error during BigQuery MERGE operation: {e}")
        # Ensure that the temporary table is deleted even in the event of an error
        try:
            client.delete_table(temp_table_ref)
            print(f"Temporary table {temp_table_id} deleted after error.")
        except Exception as cleanup_e:
            print(f"Error cleaning up temporary table: {cleanup_e}")
        raise # Re-raise original erro 