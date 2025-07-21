from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from datetime import datetime, date, timedelta
from typing import Optional

class AuthUtils:
    @staticmethod
    def bq_authenticate(
        project_id: str,
        service_account_key_path: Optional[str] = None
    ):
        try:
            # 1. Authentication
            if service_account_key_path and service_account_key_path.strip():
                credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
                client = bigquery.Client(credentials=credentials, project=project_id)
                print("Authenticated with BigQuery using service account key.")
                return client
            else:
                client = bigquery.Client(project=project_id)
                print("Authenticated with BigQuery using default environment credentials.")
                return client
      
        except Exception as e:
            print(f"BigQuery error by authentication step: {e}")
            raise  # Raise for visibility

