from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime

from helpers.email_smtp import send_email

args = {
    'owner': 'Ammar Chalifah',
}

dag = DAG(
    dag_id='dag_development_email',
    default_args=args,
    schedule_interval='0 0,7,12,18 * * *',
    start_date=datetime.datetime(2021,8,23),
    dagrun_timeout=timedelta(minutes=60),
    tags=['test_dag'],
)

send_test_email = PythonOperator(
    task_id = 'send_test_email',
    python_callable = send_email,
    op_kwargs = {'recipient':'ammar.chalifah@gmail.com','subject':'DAG Test','body':'Hi Ammar! This is a DAG email test'},
    dag = dag
)