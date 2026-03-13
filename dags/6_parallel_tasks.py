from airflow.sdk import dag, task

@dag(
    dag_id="parallel_dag"
)
def parallel_dag():
    
    @task.python
    def extract_task(**kwargs):
        print("Extracting data...")
        
        ti = kwargs["ti"]
        
        extracted_data_dict = {"api_extracted_data": [1, 2, 3],
                               "db_extracted_data": [4, 5, 6],
                               "s3_extracted_data": [7, 8, 9]}
        
        ti.xcom_push(key="return_value", value=extracted_data_dict)
        
        
    @task.python
    def second_task():
        print("This is the second task")
        
    @task.python
    def third_task():
        print("This is the third task")
        
    first = first_task()
    second = second_task()
    third = third_task()
    
    first >> second >> third
    
parallel_dag()