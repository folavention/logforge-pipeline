from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys

# Add project folder to sys.path
sys.path.append('/opt/airflow/logforge-pipeline')

from tasks import run_etl_script, run_classification

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'log_etl_pipeline',
    default_args=default_args,
    description='ETL and classification for Apache logs using logforge pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 7, 1),
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id='run_log_etl',
        python_callable=run_etl_script,
    )

    classify_logs_task = PythonOperator(
        task_id='classify_logs',
        python_callable=run_classification,
    )

    run_etl >> classify_logs_task
