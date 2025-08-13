def log_file_sample(file_obj, bytes_to_read=300):
    file_obj.seek(0)
    sample = file_obj.read(bytes_to_read)
    file_obj.seek(0)
    print(f"Primeros {bytes_to_read} bytes del archivo:\n{sample}")
