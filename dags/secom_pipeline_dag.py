import os 
import sys

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SCRIPT_DIR)

from bronze_ingest import run as run_bronze
from silver_transform import run as run_silver
from gold_transform import run as run_gold

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id="secom_pipeline",
    schedule=None, # no automatic schedule 
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:


    bronze_task = PythonOperator(
        task_id="bronze_ingest",
        python_callable=run_bronze,
    )

    silver_task = PythonOperator(
        task_id="silver_transform",
        python_callable=run_silver,
    )

    gold_task = PythonOperator(
        task_id="gold_transform",
        python_callable=run_gold,
    )


    bronze_task >> silver_task >> gold_task