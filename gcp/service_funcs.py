import ..bq_access_class as settings

def get_processed_files_from_bq():
    with settings.BigQueryConnection() as conn:
        df = conn.execute_query("SELECT * FROM `meli-bi-data.SBOX_FPSEQUALS.PROCESSED_BILLS`")
        file_names = set(df["file"].dropna().unique())
        return file_names


def insert_processed_file_to_bq(file_name: str, estado: int = 1):
    sql = f"""
    INSERT INTO `meli-bi-data.SBOX_FPSEQUALS.PROCESSED_BILLS` (file, estado, timestamp)
    VALUES (@file, @estado, CURRENT_TIMESTAMP())
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("file", "STRING", file_name),
            bigquery.ScalarQueryParameter("estado", "INT64", estado),
        ]
    )

    with settings.BigQueryConnection() as conn:
        conn.execute_query(sql, job_config=job_config)
        LOGGER.info(f"Inserted file '{file_name}' into PROCESSED_BILLS (bq).")
