from airflow.sdk import dag, task

@dag(
    dag_id="branch_dag"
)
def branch_dag():
    
    @task.python
    def extract_task(**kwargs):
        print("Extracting data...")
        
        ti = kwargs["ti"]
        
        extracted_data_dict = {"api_extracted_data": [1, 2, 3],
                               "db_extracted_data": [4, 5, 6],
                               "s3_extracted_data": [7, 8, 9],
                               "weekend_flag": "false"}
        
        ti.xcom_push(key="return_value", value=extracted_data_dict)
        
        
    @task.python
    def transfrom_task_api(**kwargs):
        ti = kwargs["ti"]
        
        api_extracted_data = ti.xcom_pull(task_ids="extract_task")["api_extracted_data"]
        
        print(f"Transforming API data: {api_extracted_data}...")
        
        transformed_api_data = [i*10 for i in api_extracted_data]
        
        ti.xcom_push(key="return_value", value=transformed_api_data)
        

    @task.python
    def transfrom_task_db(**kwargs):
        ti = kwargs["ti"]
        
        db_extracted_data = ti.xcom_pull(task_ids="extract_task")["db_extracted_data"]
        
        print(f"Transforming DB data: {db_extracted_data}...")
        
        transformed_db_data = [i*100 for i in db_extracted_data]
        
        ti.xcom_push(key="return_value", value=transformed_db_data)
        
    
    @task.python
    def transfrom_task_s3(**kwargs):
        ti = kwargs["ti"]
        
        s3_extracted_data = ti.xcom_pull(task_ids="extract_task")["s3_extracted_data"]
        
        print(f"Transforming S3 data: {s3_extracted_data}...")
        
        transformed_s3_data = [i*1000 for i in s3_extracted_data]
        
        ti.xcom_push(key="return_value", value=transformed_s3_data)
        
    
    #Creating the Decider Node
    @task.branch
    def decider_task(**kwargs):
        ti = kwargs["ti"]
        
        weekend_flag = ti.xcom_pull(task_ids="extract_task")["weekend_flag"]
        
        if weekend_flag == "true":
            return "no_load_task"
        else:
            return "load_task"
    
    
    @task.bash
    def load_task(**kwargs):
        ti = kwargs["ti"]
        
        api_data = ti.xcom_pull(task_ids="transfrom_task_api")
        db_data = ti.xcom_pull(task_ids="transfrom_task_db")
        s3_data = ti.xcom_pull(task_ids="transfrom_task_s3")
        
        return f"echo 'Loaded data: {api_data}, {db_data}, {s3_data}'"
    
    
    @task.bash
    def no_load_task(**kwargs):
        
        print("No loading on weekends.....")
        
        return "echo 'No Load Task Executed'"
        
      
    extract = extract_task()
    transform_api = transfrom_task_api()
    transform_db = transfrom_task_db()
    transform_s3 = transfrom_task_s3()
    load = load_task()
    no_load = no_load_task()

    extract >> [transform_api, transform_db, transform_s3] >> decider_task() >> [load, no_load]
    
branch_dag()