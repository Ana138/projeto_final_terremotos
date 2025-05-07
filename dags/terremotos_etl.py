from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from etl import extrair_terremotos, transformar_dados

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def pipeline():
    df = extrair_terremotos()
    transformar_dados(df)

with DAG(
    dag_id='terremotos_etl',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@monthly',
    catchup=False
) as dag:
    executar_etl = PythonOperator(
        task_id='executar_pipeline',
        python_callable=pipeline
    )
    executar_etl
