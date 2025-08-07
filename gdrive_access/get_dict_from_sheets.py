import json
import base64
from typing import List, Dict
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SimpleGoogleSheetsReader:
    """Lector simple para obtener datos específicos de Google Sheets."""
    
    def __init__(self, json_encoded_key: str):
        """
        Inicializa el lector con tu JSON encoded key.
        
        Args:
            json_encoded_key: Tu clave JSON encoded en base64
        """
        self.service = self._authenticate(json_encoded_key)
    
    def _authenticate(self, json_encoded_key: str):
        """Autentica usando el JSON encoded key."""
        try:
            # Decodificar el JSON
            decoded_json = base64.b64decode(json_encoded_key).decode('utf-8')
            credentials_info = json.loads(decoded_json)
            
            # Crear credenciales
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            credentials = Credentials.from_service_account_info(
                credentials_info, 
                scopes=scopes
            )
            
            return build('sheets', 'v4', credentials=credentials)
            
        except Exception as e:
            raise ValueError(f"Error al autenticar: {str(e)}")
    
    def get_rows_as_dict_list(self, 
                             spreadsheet_id: str, 
                             sheet_name: str,
                             columns: List[str] = ['CODIGO', 'REGEX', 'PATH']) -> List[Dict[str, str]]:
        """
        Obtiene las filas como lista de diccionarios con las columnas especificadas.
        
        Args:
            spreadsheet_id: ID del spreadsheet
            sheet_name: Nombre de la hoja
            columns: Lista de nombres de columnas a buscar (por defecto: ['CODIGO', 'REGEX', 'PATH'])
        
        Returns:
            Lista de diccionarios, uno por fila de datos
        """
        try:
            # Leer todas las filas de la hoja
            range_name = f"{sheet_name}!A:Z"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                LOGGER.info("⚠️ No se encontraron datos en la hoja")
                return []
            
            # La primera fila son los headers
            headers = values[0]
            data_rows = values[1:]
            
            # Encontrar índices de las columnas que necesitamos
            column_indices = {}
            missing_columns = []
            
            for col in columns:
                try:
                    # Buscar la columna (case insensitive)
                    index = next(i for i, header in enumerate(headers) 
                               if header.strip().upper() == col.upper())
                    column_indices[col] = index
                except StopIteration:
                    missing_columns.append(col)
            
            if missing_columns:
                available_columns = [h.strip() for h in headers if h.strip()]
                raise ValueError(
                    f"No se encontraron las columnas: {missing_columns}. "
                    f"Columnas disponibles: {available_columns}"
                )
            
            # Convertir filas a diccionarios
            result_list = []
            for row_num, row in enumerate(data_rows, start=2):  # start=2 porque fila 1 son headers
                # Saltar filas vacías
                if not any(cell.strip() for cell in row if cell):
                    continue
                
                row_dict = {}
                for col in columns:
                    col_index = column_indices[col]
                    # Obtener valor de la celda (vacío si la fila es más corta)
                    cell_value = row[col_index].strip() if col_index < len(row) else ""
                    row_dict[col] = cell_value
                
                # Solo agregar si al menos una columna tiene datos
                if any(row_dict.values()):
                    result_list.append(row_dict)
            
            LOGGER.info(f"Procesadas {len(result_list)} filas con datos desde '{sheet_name}'")
            return result_list
            
        except HttpError as error:
            if error.resp.status == 404:
                raise ValueError(f"Spreadsheet o hoja '{sheet_name}' no encontrada")
            elif error.resp.status == 403:
                raise ValueError("Sin permisos para acceder al spreadsheet")
            else:
                raise ValueError(f"Error de API: {error}")
                
        except Exception as e:
            raise ValueError(f"Error al procesar datos: {str(e)}")


def get_sheet_data(json_encoded_key: str, 
                   spreadsheet_id: str, 
                   sheet_name: str) -> List[Dict[str, str]]:
    """
    Función helper para obtener los datos rápidamente.
    
    Args:
        json_encoded_key: Tu JSON key encoded
        spreadsheet_id: ID del spreadsheet
        sheet_name: Nombre de la hoja
    
    Returns:
        Lista de diccionarios con CODIGO, REGEX, PATH
    """
    reader = SimpleGoogleSheetsReader(json_encoded_key)
    return reader.get_rows_as_dict_list(spreadsheet_id, sheet_name)
