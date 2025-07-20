from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from datetime import datetime, date, timedelta
from typing import Optional

# Define the default date as a date object for consistency
DEFAULT_START_DATE = {'since': '2025-01-01', 'until': '2025-01-01'}

def get_bq_last_date(
    project_id: str = "humboldt-385013",
    dataset_id: str = "fads",
    table_id: str = "ad_insights",
    service_account_key_path: Optional[str] = None
) -> dict:
    try:
        # 1. Authentication
        if service_account_key_path and service_account_key_path.strip():
            credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
            client = bigquery.Client(credentials=credentials, project=project_id)
            print("Authenticated with BigQuery using service account key.")
        else:
            client = bigquery.Client(project=project_id)
            print("Authenticated with BigQuery using default environment credentials.")

        # 2. Check dataset and table
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        client.get_dataset(dataset_ref)
        client.get_table(table_ref)
        print(f"Dataset '{dataset_id}' and table '{table_id}' found.")

        # 3. Run query
        query_string = f"""
            SELECT MAX(date_start) as last_date
            FROM `{project_id}.{dataset_id}.{table_id}`
        """

        query_job = client.query(query_string).result()
        rows = list(query_job)

        if rows and rows[0].get("last_date"):
            last_date_from_bq = rows[0].get("last_date")
            start_day = last_date_from_bq + timedelta(days=1)
            end_day = start_day  # Mesma data, um dia de extração

            time_range = {
                'since': start_day.strftime('%Y-%m-%d'),
                'until': end_day.strftime('%Y-%m-%d')
            }

            print(f"Last date in BigQuery: {last_date_from_bq}. Next extraction starts from: {time_range}")
            return time_range
        else:
            print(f"Table '{table_id}' is empty or 'date_start' has no values. Returning default date.")
            return DEFAULT_START_DATE

    except NotFound:
        print(f"Dataset or table not found: {project_id}.{dataset_id}.{table_id}")
        return DEFAULT_START_DATE

    except Exception as e:
        print(f"BigQuery error: {e}")
        raise  # Raise for visibility
