import pandas as pd
import duckdb


df_sensors = pd.read_csv("../data/secom/secom.data", sep=r"\s+", header=None)
df_labels = pd.read_csv("../data/secom/secom_labels.data", sep=r"\s+", header=None)


con = duckdb.connect("../data/secom_bronze.duckdb")


con.execute("CREATE OR REPLACE TABLE raw_sensors AS SELECT * FROM df_sensors")
print("raw_sensors loaded")

con.execute("CREATE OR REPLACE TABLE raw_labels AS SELECT * FROM df_labels")
print("raw_labels loaded")

con.close()