import requests
import pandas as pd
import os
import yaml
import json
from typing import Dict, List, Optional
from constants import dbt_account, dbt_project, dbt_token

# dbt API URL for fetching model metadata
BASE_URL = f"https://cloud.getdbt.com/api/v2/accounts/{dbt_account}/projects/{dbt_project}/models/"

class DbtMetadataExtractor:
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        self.schema_file = os.path.join(models_dir, "schema.yml")
        self.metadata = {
            "models": [],
            "sources": [],
            "relationships": []
        }

    def read_schema_file(self) -> Dict:
        """Read and parse the schema.yml file."""
        with open(self.schema_file, 'r') as f:
            return yaml.safe_load(f)

    def read_model_sql(self, model_name: str) -> str:
        """Read the SQL content of a model."""
        sql_file = os.path.join(self.models_dir, f"{model_name}.sql")
        if os.path.exists(sql_file):
            with open(sql_file, 'r') as f:
                return f.read()
        return ""

    def extract_model_metadata(self):
        """Extract metadata from schema.yml and SQL files."""
        schema_data = self.read_schema_file()
        
        # Process models
        for model in schema_data.get('models', []):
            model_name = model.get('name')
            model_info = {
                'name': model_name,
                'description': model.get('description', ''),
                'columns': model.get('columns', []),
                'sql': self.read_model_sql(model_name),
                'tags': model.get('tags', []),
                'meta': model.get('meta', {}),
            }
            self.metadata['models'].append(model_info)

        # Process sources
        for source in schema_data.get('sources', []):
            source_info = {
                'name': source.get('name'),
                'description': source.get('description', ''),
                'tables': source.get('tables', []),
            }
            self.metadata['sources'].append(source_info)

        # Extract relationships from column references
        for model in self.metadata['models']:
            for column in model.get('columns', []):
                if 'tests' in column:
                    for test in column['tests']:
                        if isinstance(test, dict):
                            if 'relationships' in test:
                                self.metadata['relationships'].append({
                                    'from_model': model['name'],
                                    'from_column': column['name'],
                                    'to_model': test['relationships'].get('to'),
                                    'to_column': test['relationships'].get('field')
                                })

    def save_metadata(self, output_file: str):
        """Save the extracted metadata to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

def main():
    # Initialize the extractor with the models directory
    extractor = DbtMetadataExtractor('models')
    
    # Extract metadata
    extractor.extract_model_metadata()
    
    # Save to a JSON file in the chatdbt_raw_data directory
    os.makedirs('chatdbt_raw_data', exist_ok=True)
    output_file = 'chatdbt_raw_data/dbt_metadata.json'
    extractor.save_metadata(output_file)
    print(f"Metadata has been extracted and saved to {output_file}")

if __name__ == "__main__":
    main() 