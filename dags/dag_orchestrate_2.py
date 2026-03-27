from airflow.sdk import dag, task
import os

@dag(
    dag_id="second_orchestrator_dag"
)
def second_orchestrator_dag():
    
    @task.python
    def first_task():
        print("Ths is the first task")
        
    @task.python
    def second_task():
        print("This is the second task")
        
    @task.python
    def third_task():
        os.makedirs(os.path.dirname("/opt/airflow/logs/data"), exist_ok=True)
        
        with open("/opt/airflow/logs/data/output_2.txt", 'w') as f:
            f.write(f"Data processesed successfully")
        
    first = first_task()
    second = second_task()
    third = third_task()
    
    first >> second >> third
    
second_orchestrator_dag()