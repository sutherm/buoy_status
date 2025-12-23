import os
import requests
import json
import pandas as pd
from pandas import json_normalize
from pathlib import Path

def query_glos_api(endp):
    url = f"https://seagull-api.glos.org/api/v1/{endp}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the JSON payload
        response_data = response.json()
        # Normalize the JSON to create a DataFrame
        norm_data = json_normalize(response_data)
        return norm_data
    else:
        errors = print(f"Error: {response.status_code}")
        return errors

DATA_PATH = Path("data/buoys.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

summary_df = query_glos_api("obs-dataset-summaries")
buoy_df = summary_df[(summary_df['obs_dataset_platform_assignment.platform.platform_type'] == 'moored_buoy')]
final_df = buoy_df[['org_platform_id', 'platform_name',
                     'obs_dataset_platform_assignment.platform.platform_event.collection_status',
                     'deployment_site.latitude', 'deployment_site.longitude']]
final_df.columns = ['buoy', 'name', 'status', 'lat', 'lng']
json_records = final_df.to_json("data/buoys.json", orient='records')
