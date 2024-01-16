from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import pendulum
from airflow.models import Param, Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 0,  # Set retries to 0

}

dag = DAG(
    dag_id='branch_test_4',
    schedule_interval=None,
    start_date=pendulum.now(),
    catchup=False,
    dagrun_timeout=None,
    max_active_runs=1,
     params={
        'skip_last_task_condition': Param(type='boolean', default=False)
    }

)

# Define empty tasks
task1 = PythonOperator(
    task_id='task1',
    python_callable=lambda: print('Executing task 1'),
    dag=dag,
)

task2 = PythonOperator(
    task_id='task2',
    python_callable=lambda: print('Executing task 2'),
    dag=dag,
)

task3 = PythonOperator(
    task_id='task3',
    python_callable=lambda: print('Executing task 3'),
    dag=dag,
)

# this is the chekcing function to decide next step 
def decide_skip_last_task(**kwargs):
    condition = kwargs['params'].get('skip_last_task_condition')
    if condition:
        return 'task4'
    else:
        return 'task3'

# checking task 
check_skip_last_task = BranchPythonOperator(
    task_id='check_skip_last_task_condition',
    python_callable=decide_skip_last_task,
    provide_context=True,
    dag=dag,
)

# empty task 
task4 = PythonOperator(
    task_id='task4',
    python_callable=lambda: print('Skipping last task'),
    dag=dag,
)

# Set up task dependencies based on the condition
task1 >> task2 >> check_skip_last_task >> [task4, task3]

# when the skip_last_task_condition = true, skip 3 , run 4 ; when skip_last_task_condition = false , skip 4 , run 3 ; 