from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound 
from typing import List, Dict, Any, Optional
from .models import AdInsightModel
from .schema import ad_insights_schema
from .transform import transform_insights
from .extract import extract_ad_insights
from datetime import date 

def load_data_to_bigquery(
    data: List[AdInsightModel],
    project_id: str,
    dataset_id: str, 
    table_id: str,
    target_partition_date: str,
    service_account_key_path: Optional[str] = None
) -> bigquery.job.LoadJob:
    
    # 1. Authentications
    try:
        credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        print("Successful authenticated in BQ.")
    except Exception as e:
        print(f"Bigquery error in authentication step: {e}")
        raise

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

    # 5. Setting up the Loading Job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema=ad_insights_schema, 
        # write_disposition will be set based on the target_partition_date
    )

    # The destination for the load job will be the specific daily partition
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    # Format the partition suffix as YYYYMMDD for daily partitioning
    partition_suffix = target_partition_date
    destination_for_load_job = client.dataset(dataset_id).table(f"{table_id}${partition_suffix}")

    print(f"Loading to specific partition: {destination_for_load_job.path}. Write disposition: {job_config.write_disposition}")

    # 6. Starting and Monitoring the Loading Job. CENTRAL FUNCTION
    try:
        # Use the calculated specific partition as the destination
        load_job = client.load_table_from_json(
            json_data, destination_for_load_job, job_config=job_config 
        )
        print(f"BigQuery loading job started: {load_job.job_id}")

        load_job.result()

        print(f"Loading job {load_job.job_id} completed.")

        if load_job.errors:
            print("Errors encountered during loading:")
            for error in load_job.errors:
                print(error)
            raise Exception("BigQuery loading job failed with errors.")
        else:
            print(f"Total lines loaded: {load_job.output_rows}")
        
        return load_job

    except Exception as e:
        print(f"Unexpected error during loading job in BigQuery: {e}")
        raise