import os
import sys

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SCRIPT_DIR)

from datetime import datetime, timezone

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from bronze_ingest import run as run_bronze
from load_to_bigquery import run as run_bq_load

DBT_PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dbt")

with DAG(
    dag_id="secom_pipeline",
    schedule=None, # no automatic schedule
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,

) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_ingest",
        python_callable=run_bronze,
    )

    dbt_build_task = BashOperator(
        task_id="dbt_build",
        bash_command=f"dbt build --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR}",
        cwd=DBT_PROJECT_DIR,
    )

    bq_load_task = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=run_bq_load
    )

    bronze_task >> dbt_build_task >> bq_load_task