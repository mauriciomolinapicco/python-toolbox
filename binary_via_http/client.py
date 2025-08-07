import os
import requests

# Nombre del archivo que ya debería existir en el mismo directorio
file_path = "MERCADOPAGO URUGUAY S.R.L._URUTEC S A_EFacturaA10771.pdf"

# Validar existencia del archivo
if not os.path.isfile(file_path):
    print(f"❌ El archivo '{file_path}' no existe en el directorio actual.")
    exit(1)

# Endpoint donde se envía el archivo
url = "http://localhost:5000/upload"

# Armado del request
with open(file_path, "rb") as file:
    files = {"file": (os.path.basename(file_path), file)}
    response = requests.post(url, files=files)

# Mostrar respuesta del servidor
print("✅ Archivo enviado:")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
