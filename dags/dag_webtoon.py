from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime

from helpers.line_webtoon_official_scrape import scrape_official_webtoons

args = {
    'owner': 'Ammar Chalifah',
}

dag = DAG(
    dag_id='dag_webtoon',
    default_args=args,
    schedule_interval='0 11 * * *',
    start_date=datetime.datetime(2021,8,30),
    dagrun_timeout=timedelta(minutes=60),
    tags=['webtoon'],
)

dev_scrape_webtoon_officials = PythonOperator(
    task_id = 'dev_scrape_webtoon_officials',
    python_callable = scrape_official_webtoons,
    op_kwargs = {'host':'ammarchalifah.com','port':3306,
        'user':os.environ['AMMARCHALIFAH_MYSQL_USER'], 
        'password':os.environ['AMMARCHALIFAH_MYSQL_PASSWORD'],
        'database':'ammarch1_airflow'},
    dag = dag
)