from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime

from helpers.mysql_connection import query_mysql

args = {
    'owner': 'Ammar Chalifah',
}

dag = DAG(
    dag_id='dag_development_mysql',
    default_args=args,
    schedule_interval='0 0,7,12,18 * * *',
    start_date=datetime.datetime(2021,8,25),
    dagrun_timeout=timedelta(minutes=60),
    tags=['test_dag'],
)

dev_query_mysql = PythonOperator(
    task_id = 'dev_query_mysql',
    python_callable = query_mysql,
    op_kwargs = {'host':'ammarchalifah.com','port':3306,
        'user':os.environ['AMMARCHALIFAH_MYSQL_USER'], 
        'password':os.environ['AMMARCHALIFAH_MYSQL_PASSWORD'],
        'database':'ammarch1_staticdata'},
    dag = dag
)