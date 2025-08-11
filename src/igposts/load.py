from google.cloud import bigquery
from utils.bq_auth import AuthUtils
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from typing import List, Dict, Any, Optional
from igpage.models import InstaPageModel
from igpage.schema import instagram_page_schema
from datetime import date, datetime

def load_data_to_bigquery(
    data: List[InstaPageModel],
    project_id: str,
    dataset_id: str,
    table_id: str,
    service_account_key_path: Optional[str]=None
) -> Optional[bigquery.LoadJob]:

    def get_table_schema(table_id: str) -> List[bigquery.SchemaField]:
        if table_id == "hu_igpage":
            return instagram_page_schema
        raise ValueError(f"Schema not found for table_id: {table_id}")

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

    # 3. Creating table
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=get_table_schema(table_id))
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",
        expiration_ms=None
    )
    table.clustering_fields = ["page_id"]        
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

    # 3. Preparing data for loading
    json_data = [item.model_dump(mode='json') for item in data]

    if not json_data:
        print("No data to load. Ending the loading job.")
        return None

    # --- MERGE ---
    temp_table_id = f"{table_id}_temp_{client.project}_{dataset_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    temp_table_ref = client.dataset(dataset_id).table(temp_table_id)

    temp_load_job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema=get_table_schema(table_id),
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    try:
        print(f"Loading {len(json_data)} records into temporary table: {temp_table_ref.path}")
        load_temp_job = client.load_table_from_json(
            json_data, temp_table_ref, job_config=temp_load_job_config
        )
        load_temp_job.result()
        print(f"Data loaded to temporary table {temp_table_id}. Total rows: {load_temp_job.output_rows}")

        # 1. the columns that come from the source table (S)
        update_cols_from_source = [
            "follow_count", "profile_views", "website_clicks",
        ]
        
        # 2. Create the list of UPDATE statements from these columns
        update_statements_list = [f"T.{col} = S.{col}" for col in update_cols_from_source]
        
        # 3. Add the UPDATE statement for the timestamp
        update_statements_list.append("T.last_updated_timestamp = CURRENT_TIMESTAMP()")
        
        # 4. Join all instructions with a comma
        update_statements = ", ".join(update_statements_list)

        # The rest of the code for INSERT remains the same as in the previous correction
        insertable_fields = [field for field in get_table_schema(table_id) if field.name != 'last_updated_timestamp']
        insert_cols = ", ".join([f"{field.name}" for field in insertable_fields])
        insert_values = ", ".join([f"S.{field.name}" for field in insertable_fields])

        #print(f"Update statements: {update_statements}")
        #print(f"Generated insert_cols: '{insert_cols}'")
        #print(f"Generated insert_values: '{insert_values}'")

        # 5. Simplify the MERGE query to use the generated string
        merge_query = f"""
        MERGE INTO `{project_id}.{dataset_id}.{table_id}` T
        USING `{project_id}.{dataset_id}.{temp_table_id}` S
        ON
        T.id = S.id AND
        T.date = S.date AND
        T.page_id = S.page_id
        WHEN MATCHED THEN
            UPDATE SET {update_statements}
        WHEN NOT MATCHED BY TARGET THEN
            INSERT ({insert_cols}, last_updated_timestamp)
            VALUES ({insert_values}, CURRENT_TIMESTAMP());
        """

        print("--- Generated MERGE Query ---")
        print(merge_query)
        print("-----------------------------")

        print(f"Executing MERGE query from {temp_table_id} to {table_id}...")
        query_job = client.query(merge_query)
        query_job.result()
        print("MERGE operation completed successfully.")

        client.delete_table(temp_table_ref)
        print(f"Temporary table {temp_table_id} deleted.")

        return load_temp_job

    except Exception as e:
        print(f"Error during BigQuery MERGE operation: {e}")
        try:
            client.delete_table(temp_table_ref)
            print(f"Temporary table {temp_table_id} deleted after error.")
        except Exception as cleanup_e:
            print(f"Error cleaning up temporary table: {cleanup_e}")
        raise
