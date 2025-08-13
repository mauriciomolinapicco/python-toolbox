def filename_from_path(path: str) -> str:
    return path.strip().split("/")[-1]

def send_file_to_endpoint(file_obj, filename, codigo, endpoint):
    file_obj.seek(0)
    files = {"file": (filename, file_obj, "application/pdf")}
    data = {"codigo": codigo, "filename": filename}
    response = requests.post(endpoint, files=files, data=data)
    return response
