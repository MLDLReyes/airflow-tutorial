from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.interval import CronDataIntervalTimetable

@dag(
    schedule=CronDataIntervalTimetable("@daily", timezone="Asia/Manila"),
    start_date=datetime(year=2026, month=3, day=18, tz="Asia/Manila"),
    end_date=datetime(year=2026, month=3, day=31, tz="Asia/Manila"),
    is_paused_upon_creation=False,
    catchup=True
)
def incremental_load_dag():
    
    @task.python
    def incremental_data_fetch(**kwargs):
        date_interval_start = kwargs['data_interval_start']
        date_interval_end = kwargs['data_interval_end']
        print(f"Fetching data from {date_interval_start} to {date_interval_end}")
        
    @task.bash
    def incremental_data_process():
        return "echo 'Processing incremental data from {{data_interval_start}} to {{data_interval_end}}'"
    
    fetch_task = incremental_data_fetch()
    process_task = incremental_data_process()
    
    fetch_task >> process_task
    
incremental_load_dag()