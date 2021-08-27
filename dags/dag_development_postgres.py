from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime

from helpers.postgres_connection import query_postgres

args = {
    'owner': 'Ammar Chalifah',
}

dag = DAG(
    dag_id='dag_development_postgres',
    default_args=args,
    schedule_interval='0 0,7,12,18 * * *',
    start_date=datetime.datetime(2021,8,25),
    dagrun_timeout=timedelta(minutes=60),
    tags=['test_dag'],
)

dev_query_postgres = PythonOperator(
    task_id = 'dev_query_postgres',
    python_callable = query_postgres,
    op_kwargs = {'host':'ammarchalifah.com','port':5432,
        'user':os.environ['AMMARCHALIFAH_MYSQL_USER'], 
        'password':os.environ['AMMARCHALIFAH_MYSQL_PASSWORD'],
        'dbname':'ammarch1_postgres',
        'query':'select * from public.comics;',
        'execution_type':'cursor'},
    dag = dag
)