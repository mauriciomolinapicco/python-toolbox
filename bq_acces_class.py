import os
import json
import base64
import logging
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError
import pandas as pd
from dotenv import load_dotenv
from secret_client import SecretClient

class BigQueryConnection:
    def __init__(self):
        self._secret_client = SecretClient()
        self._env = self.get_environment()
        self._credentials = self._get_credentials()
        self.client = bigquery.Client(
            project="project_id",
            credentials=self._credentials
        )

    def get_environment(self):
        try:
            env = self._secret_client.get_secret("EXEC_ENVIRONMENT")
            LOGGER.info(f"Execution environment: {env}")
            return env
        except Exception as ke:
            LOGGER.info(f"key error: {ke}")
            load_dotenv()
            env = "local"
            LOGGER.info(f"Default environment selected: {env}")
            return env

    def _get_credentials(self):
        if self._env == "local":
            encoded_credentials = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
        else:
            encoded_credentials = self._secret_client.get_secret("GOOGLE_SERVICE_ACCOUNT_KEY")
    
        if not encoded_credentials:
            raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_KEY in local environment.")

        google_cred: bytes = base64.b64decode(encoded_credentials)
        jsoncred: dict = json.loads(google_cred)
        return service_account.Credentials.from_service_account_info(
            jsoncred, 
            scopes=['https://www.googleapis.com/auth/cloud-platform', "https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/bigquery",]
            )
    

    def execute_query(self, sql: str, **kwargs) -> pd.DataFrame:
        """
        Ejecuta una query SQL y devuelve un DataFrame.
        kwargs se pasa a client.query(), útil por ejemplo para 'job_config'.
        """
        try:
            LOGGER.info(f"Executing query:\n{sql}")
            query_job = self.client.query(sql, **kwargs)
            result = query_job.result()
            df = result.to_dataframe()
            df["timestamp"] = df["timestamp"].astype(str)  
            return df
        except GoogleAPICallError as e:
            LOGGER.error(f"BigQuery error: {e}")
            raise
        except Exception as e:
            LOGGER.error(f"Unexpected error during query: {e}")
            raise