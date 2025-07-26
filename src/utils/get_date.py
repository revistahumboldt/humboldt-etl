
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from datetime import datetime, date, timedelta
from typing import Optional, Dict
from utils.bq_auth import AuthUtils
from datetime import datetime

class DateUtils:

    @staticmethod
    def default_time_range(delta: int = 0):
        since = date(2023,2,15) + timedelta(delta)
        until = date(2023,2,15) + timedelta(delta)
        return {'since':since.strftime('%Y-%m-%d'),'until': until.strftime('%Y-%m-%d')
        }


    @staticmethod
    def get_current_date() -> dict:
        """Returns the current date in 'YYYY-MM-DD' format."""
        return {'since': datetime.now().strftime('%Y-%m-%d'), 'until': datetime.now().strftime('%Y-%m-%d')}

    @staticmethod
    def get_last_28_days() -> Dict[str, str]:
        """Returns a dictionary with the start and end dates for the last 28 days."""
        today = date.today()
        start_date = today - timedelta(days=28)
        return {
            'since': start_date.strftime('%Y-%m-%d'),
            'until': today.strftime('%Y-%m-%d')
        }

    @staticmethod
    def get_bq_based_time_range(
        project_id: str,
        dataset_id: str,
        table_id: str,
        delta_days: int = 1,
        service_account_key_path: Optional[str] = None
    ) -> Dict[str, str]:
        """Fetches the last date from BigQuery and returns the next date for extraction."""
        client = AuthUtils.bq_authenticate(project_id, service_account_key_path)
        try:
            query_string = f"""
            SELECT MAX(date_start) as last_date
            FROM `{project_id}.{dataset_id}.{table_id}`
            """
            query_job = client.query(query_string).result()
            rows = list(query_job)
            if rows and rows[0].get("last_date"):
                last_date_from_bq = rows[0].get("last_date")
                start_day = last_date_from_bq + timedelta(1)
                end_day = start_day + timedelta(delta_days) # Same date, one day extraction

                return {
                    'since': start_day.strftime('%Y-%m-%d'),
                    'until': end_day.strftime('%Y-%m-%d')
                }
            else:
                print(f"Table '{table_id}' is empty or 'date_start' has no values. Returning default date.")
            return DateUtils.default_time_range(delta_days)
        except NotFound as e:
            print(f"Dataset or table not found: {project_id}.{dataset_id}.{table_id}")
            return DateUtils.default_time_range(delta_days)

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
            return DateUtils.default_time_range(delta_days)
        except NotFound as e:
            print(f"Dataset or table not found: {project_id}.{dataset_id}.{table_id}")
            return DateUtils.default_time_range(delta_days)    

    @staticmethod
    def get_bq_last_day(
        project_id: str,
        dataset_id: str,
        table_id: str,
        service_account_key_path: Optional[str] = None
    ) -> Optional[date]:
        """Fetches the last date from BigQuery."""
        client = AuthUtils.bq_authenticate(project_id, service_account_key_path)

        try:
            query_string = f"""
            SELECT MAX(date_start) as last_date
            FROM `{project_id}.{dataset_id}.{table_id}`
            """
            query_job = client.query(query_string).result()
            rows = list(query_job)
            if rows and rows[0].get("last_date"):
                return rows[0].get("last_date")
            else:
                print(f"Table '{table_id}' is empty or 'date_start' has no values.")
                return None
        except NotFound as e:
            print(f"Dataset or table not found: {project_id}.{dataset_id}.{table_id}")
            return None
        
    
    
    @staticmethod
    def get_delta_days(bq_last_date:date):
        current_date = datetime.now()
        if bq_last_date is not None:
            bq_last_date_dt = datetime.combine(bq_last_date, datetime.min.time())
            return (current_date-bq_last_date_dt).days 
        
