import pandas as pd
import duckdb 


con = duckdb.connect("../data/secom_bronze.duckdb")

df_sensors = con.execute("SELECT * FROM raw_sensors").df()
df_labels = con.execute("SELECT * FROM raw_labels").df()

col_to_keep = df_sensors.isnull().mean() < 0.2
df_sensors_cleaned = df_sensors.loc[:, col_to_keep]


print(f"Sensor data before : {df_sensors.shape[1]}, Sensor data after cleaned : {df_sensors_cleaned.shape[1]}")

df_sensors_imputed = df_sensors_cleaned.fillna(df_sensors_cleaned.median())

print(f"Sensor before impute : {df_sensors_cleaned.isnull().sum().sum()}, Sensors after impute : {df_sensors_imputed.isnull().sum().sum()}")

df_sensors_imputed.columns = [f"sensor_{n}" for n in range(0, df_sensors_imputed.shape[1])]

print(df_sensors_imputed.columns)



df_labels.columns = ["label", "timestamp"]

print(df_labels.columns)




df_silver = pd.concat([df_sensors_imputed, df_labels], axis=1)

print(df_silver)


df_silver["timestamp"] = pd.to_datetime(df_silver["timestamp"])

print(df_silver["timestamp"])



conn = duckdb.connect("../data/secom_silver.duckdb")
conn.execute("CREATE OR REPLACE TABLE silver_data AS SELECT * FROM df_silver")

con.close()
conn.close()