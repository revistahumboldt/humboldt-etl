from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from datetime import datetime, date, timedelta

# Define the default date as a date object for consistency
DEFAULT_START_DATE = {'since': '2025-01-01', 'until': '2025-01-01'}  

def get_bq_last_date(
    project_id: str = "humboldt-385013",
    dataset_id: str = "fads",
    table_id: str = "ad_insights",
    service_account_key_path: str = "C:/projetos/humboldt-etl/humboldt-gcp.json" 
) -> dict: # Explicitly type-hint the return as dict
    
    client = None # Initialize client outside try for broader scope if needed

    try:
        # 1. Authentication
        credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
        client = bigquery.Client(credentials=credentials, project=project_id) # Use the passed project_id
        print("Authenticated with BigQuery successfully.")

        # 2. Check for dataset and table, then query
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        # Using specific exceptions for clarity
        try:
            client.get_dataset(dataset_ref) # Check if dataset exists
            client.get_table(table_ref)     # Check if table exists
            print(f"Dataset '{dataset_id}' and table '{table_id}' found.")

            query_string = f"""
                SELECT MAX(date_start) as last_date
                FROM `{project_id}.{dataset_id}.{table_id}`
            """

            query_job = client.query(query_string).result() # client.query().result() waits for job completion
            
            # Check if any rows were returned (table might be empty)
            rows = list(query_job)
            
            if rows and rows[0].get("last_date"): # Check if row exists and 'last_date' is not None
                last_date_from_bq = rows[0].get("last_date") # This is already a datetime.date object
                
                # Increment by one day
                start_day_for_extraction = last_date_from_bq + timedelta(days=1)
                end_day_for_extraction = last_date_from_bq + timedelta(days=2)
                time_range ={'since': start_day_for_extraction.strftime('%Y-%m-%d'),
                             'until': end_day_for_extraction.strftime('%Y-%m-%d')}

                print(f"Last date in BigQuery: {start_day_for_extraction}. Next extraction starts from: {time_range}")
                return DEFAULT_START_DATE
                #return time_range
            else:
                # Table exists but is empty, or MAX(date_start) returned NULL
                print(f"Table '{table_id}' is empty or 'date_start' column has no values. Returning default start date.")
                return DEFAULT_START_DATE

        except NotFound: # Catch specific NotFound error for dataset/table
            print(f"Dataset '{dataset_id}' or table '{table_id}' not found.")
            print("Returning default start date.")
            return DEFAULT_START_DATE
        except Exception as e: # Catch any other unexpected errors during query execution
            print(f"An unexpected error occurred during query execution: {e}")
            print("Returning default start date.")
            return DEFAULT_START_DATE

    except Exception as e: 
        print(f"BigQuery authentication or client creation error: {e}")
        raise # Re-raise authentication errors as they are critical

# Example usage:
start_date_for_pipeline = get_bq_last_date()
print(f"Pipeline will start data extraction from: {start_date_for_pipeline}")