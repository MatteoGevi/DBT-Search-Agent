import requests
import pandas as pd
from constants import DBT_API_TOKEN, ACCOUNT_ID, PROJECT_ID

# dbt API URL for fetching model metadata
BASE_URL = f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/projects/{PROJECT_ID}/models/"

# Headers for API authorization
headers = {
    "Authorization": f"Token {DBT_API_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_dbt_models():
    """Fetches model metadata from dbt Cloud API."""
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        models_data = response.json().get('data', [])
        return models_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def parse_model_metadata(models_data):
    """Parses model metadata and extracts relevant information."""
    models = []
    for model in models_data:
        model_name = model.get('name')
        description = model.get('description', 'No description')
        columns = model.get('columns', {})
        
        # Extract column names and descriptions
        for column_name, column_info in columns.items():
            models.append({
                "Model Name": model_name,
                "Model Description": description,
                "Column Name": column_name,
                "Column Description": column_info.get('description', 'No description')
            })
    
    return pd.DataFrame(models)

# Fetch and parse dbt model metadata
models_data = fetch_dbt_models()
if models_data:
    models_df = parse_model_metadata(models_data)
    print(models_df)
else:
    print("No data retrieved.")