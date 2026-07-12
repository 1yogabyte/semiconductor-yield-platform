import pandas as pd
import duckdb 
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")

def run():
    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_silver.duckdb"))

    df_silver = conn.execute("SELECT * FROM silver_data").df()

    conn.close()


    df_silver["month"] = df_silver["timestamp"].dt.to_period("M")
    print(df_silver["month"])

    gold_yield = df_silver.groupby("month")["label"].apply(lambda x: (x == -1).mean() * 100).reset_index()
    gold_yield.columns = ["month", "yield_rate_pct"]
    print(gold_yield)

    gold_yield["month"] = gold_yield["month"].astype(str)

    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_gold.duckdb"))
    conn.execute("CREATE OR REPLACE TABLE gold_yield_by_month AS SELECT * FROM gold_yield")
    print("Gold yield by month table created")

    conn.close()

    df_pass = df_silver[df_silver["label"] == -1]   
    df_fail = df_silver[df_silver["label"] == 1]

    sensors_col = [col for col in df_silver.columns if col.startswith("sensor_")]
    mean_pass = df_pass[sensors_col].mean()
    mean_fail = df_fail[sensors_col].mean()

    diff = (mean_pass - mean_fail).abs()
    diff = diff.sort_values(ascending=False)

    sensor_correlation = diff.head(20).reset_index()
    sensor_correlation.columns = ["sensor" , "mean_difference"]
    print(sensor_correlation)

    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_gold.duckdb"))
    conn.execute("CREATE OR REPLACE TABLE gold_sensor_correlation AS SELECT * FROM sensor_correlation")
    print("Gold correlation table executed")

    conn.close()

    total_units = len(df_silver)
    total_pass = (df_silver["label"] == -1).sum()
    total_fail = (df_silver["label"] == 1).sum()
    yield_rate_pct = (total_pass / total_units) * 100
    date_start = df_silver["timestamp"].min()
    date_end = df_silver["timestamp"].max()
    n_sensors = len(sensors_col)

    gold_summary = pd.DataFrame([{
        "total_units": total_units,
        "total_pass": total_pass,
        "total_fail": total_fail,
        "yield_rate_pct": yield_rate_pct,
        "date_start": date_start,
        "date_end": date_end,
        "n_sensors": n_sensors
    }])

    conn = duckdb.connect(os.path.join(DATA_DIR, "secom_gold.duckdb"))

    conn.execute("CREATE OR REPLACE TABLE gold_summary AS SELECT * FROM gold_summary")
    print("Gold summary table executed")
    conn.close()


if __name__ == "__main__":
    run()