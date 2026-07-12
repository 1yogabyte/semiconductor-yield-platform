import pandas as pd
import duckdb
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")


def run():

    df_sensors = pd.read_csv(os.path.join(DATA_DIR, "secom", "secom.data"), sep=r"\s+", header=None)
    df_labels = pd.read_csv(os.path.join(DATA_DIR, "secom", "secom_labels.data"), sep=r"\s+", header=None)

    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_bronze.duckdb"))

    conn.execute("CREATE OR REPLACE TABLE raw_sensors AS SELECT * FROM df_sensors")
    print("raw_sensors loaded")

    conn.execute("CREATE OR REPLACE TABLE raw_labels AS SELECT * FROM df_labels")
    print("raw_labels loaded")

    conn.close()

if __name__ == "__main__":
    run()


