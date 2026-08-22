from google.cloud import bigquery
import os
import duckdb


PROJECT_ID = "secom-yield-platform"
DATASET_ID = "secom_gold"
KEY_PATH = os.environ.get("GCP_KEY_PATH", os.path.expanduser("~/.gcp/secom-key.json"))


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")


def run():

    client = bigquery.Client.from_service_account_json(KEY_PATH, project=PROJECT_ID)
    client.create_dataset(DATASET_ID, exists_ok=True)
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_dbt.duckdb"), read_only=True)

    tables = ["gold_yield_by_month", "gold_sensor_correlation", "gold_summary"]

    for table_name in tables:
        df = conn.execute(f"SELECT * FROM {table_name}").df()
        client.load_table_from_dataframe(df, f"{DATASET_ID}.{table_name}", job_config=job_config).result()
        print(f"loaded {table_name}: {len(df)} rows")

    conn.close()


if __name__ == "__main__":
    run()
