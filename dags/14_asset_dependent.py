from airflow.sdk import dag, task, asset
from pendulum import datetime
import os
from asset_13 import fetch_data

@asset(
    schedule=fetch_data,
    uri="/opt/airflow/logs/data/data_processed.txt",
    name="process_data"
)
def process_data(self):
    
    #to make sure directory exists
    os.makedirs(os.path.dirname(self.uri), exist_ok=True)
    
    #writing to file
    with open(self.uri, 'w') as f:
        f.write(f"Data processed successfully")
    
    print(f"Data processed to {self.uri}")