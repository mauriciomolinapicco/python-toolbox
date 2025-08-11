import boto3
import pandas as pd
import io
from datetime import datetime
from botocore.exceptions import ClientError
from typing import Set, Optional

class S3Manager:
    def __init__(self, bucket_name: str, csv_filename: str):
        """
        Args:
            bucket_name: Nombre del bucket S3
            csv_filename: Nombre del archivo CSV
        """
        self.bucket_name = bucket_name
        self.csv_filename = csv_filename
        print("Conectando a S3")
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=ENVIRONMENT.get_aws_keys()['access_key'],
            aws_secret_access_key=ENVIRONMENT.get_aws_keys()['secret_key']
        )
    
    def _read_csv(self) -> pd.DataFrame:
        """Lee el CSV desde S3."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.csv_filename)
            csv_content = response['Body'].read().decode('utf-8')
            return pd.read_csv(io.StringIO(csv_content))
        except ClientError:
            # Si no existe, crear DataFrame vacío
            return pd.DataFrame(columns=['nombre_archivo', 'timestamp'])
    
    def _write_csv(self, df: pd.DataFrame):
        """Escribe el CSV a S3."""
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=self.csv_filename,
            Body=csv_buffer.getvalue()
        )
    
    def load_filenames_to_set(self) -> Set[str]:
        """Carga todos los nombres de archivos en un set (siempre lee desde S3)."""
        df = self._read_csv()
        if df.empty:
            return set()
        return set(df['nombre_archivo'].dropna())
    
    def append_new_record(self, filename: str, timestamp: Optional[str] = None) -> bool:
        """Agrega un nuevo registro al CSV."""
        if not filename.strip():
            return False
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        try:
            df = self._read_csv()
            new_record = pd.DataFrame([{
                'nombre_archivo': filename.strip(),
                'timestamp': timestamp
            }])
            
            df = pd.concat([df, new_record], ignore_index=True)
            self._write_csv(df)
            return True
        except Exception:
            return False
