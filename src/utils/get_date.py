
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from datetime import datetime, date, timedelta
from typing import Optional, Dict
from utils.bq_auth import AuthUtils
from datetime import datetime

class DateUtils:

    default_start_date: Dict[str, str] = {'since': '2025-01-01', 'until': '2025-01-01'}

    @staticmethod
    def get_time_range(
        project_id: str,
        dataset_id: str,
        table_id: str,
        delta_days: int = 1,
        service_account_key_path: Optional[str] = None
        ):
        client = AuthUtils.bq_authenticate(project_id, service_account_key_path)
        try:
           # 3. Run query
            query_string = f"""
            SELECT MAX(date_start) as last_date
            FROM `{project_id}.{dataset_id}.{table_id}`
            """
            query_job = client.query(query_string).result()
            rows = list(query_job)
            if rows and rows[0].get("last_date"):
                last_date_from_bq = rows[0].get("last_date")
                start_day = last_date_from_bq + timedelta(delta_days)
                end_day = start_day  # Mesma data, um dia de extração

                time_range = {
                'since': start_day.strftime('%Y-%m-%d'),
                'until': end_day.strftime('%Y-%m-%d')
                }

                print(f"Last date in BigQuery: {last_date_from_bq}. Next extraction starts from: {time_range}")
                return time_range
            else:
                print(f"Table '{table_id}' is empty or 'date_start' has no values. Returning default date.")
            return DateUtils.default_start_date
        except NotFound as e:
            print(f"Dataset or table not found: {project_id}.{dataset_id}.{table_id}")
            return DateUtils.default_start_date     

