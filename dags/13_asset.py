from airflow.sdk import dag, task, asset
from pendulum import datetime
import os

@asset(
    schedule="@daily",
    uri="/opt/airflow/logs/data/data_extract.txt",
    name="fetch_data"
)
def fetch_data(self):
    
    #to make sure directory exists
    os.makedirs(os.path.dirname(self.uri), exist_ok=True)
    
    #writing to file
    with open(self.uri, 'w') as f:
        f.write(f"Data fetched successfully")
    
    print(f"Data written to {self.uri}")