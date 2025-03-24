import os
import json
import yaml
import subprocess
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DbtMetadataExtractor:
    def __init__(self, project_dir: str = None):
        """
        Initialize the DBT metadata extractor
        Args:
            project_dir: Path to the dbt project directory. If None, will try to find it from DBT_PROJECT_DIR env var
        """
        self.project_dir = project_dir or os.getenv('DBT_PROJECT_DIR')
        if not self.project_dir:
            raise ValueError("DBT project directory not specified. Either pass it to the constructor or set DBT_PROJECT_DIR environment variable")
        
        self.metadata = {
            "models": [],
            "sources": [],
            "relationships": []
        }

    def run_dbt_command(self, command: List[str]) -> str:
        """Run a dbt command and return its output"""
        try:
            result = subprocess.run(
                ['dbt'] + command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running dbt command: {e.stderr}")
            raise

    def test_connection(self) -> bool:
        """Test if dbt is properly configured and can connect to the database"""
        try:
            self.run_dbt_command(['debug'])
            return True
        except Exception as e:
            print(f"Failed to connect to database: {str(e)}")
            return False

    def compile_models(self):
        """Compile dbt models to get the latest metadata"""
        try:
            self.run_dbt_command(['compile'])
        except Exception as e:
            print(f"Failed to compile models: {str(e)}")
            raise

    def extract_model_metadata(self):
        """Extract metadata from local dbt project"""
        try:
            # First compile the project to ensure manifest is up to date
            self.compile_models()
            
            # Read the manifest.json file which contains all model metadata
            manifest_path = os.path.join(self.project_dir, 'target', 'manifest.json')
            if not os.path.exists(manifest_path):
                raise FileNotFoundError(f"manifest.json not found at {manifest_path}. Make sure dbt compile ran successfully.")
            
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Process nodes (models)
            for node_id, node in manifest.get('nodes', {}).items():
                if node.get('resource_type') == 'model':
                    model_info = {
                        'name': node.get('name'),
                        'description': node.get('description', ''),
                        'columns': [
                            {
                                'name': col_name,
                                'description': col_info.get('description', ''),
                                'tests': col_info.get('tests', []),
                                'meta': col_info.get('meta', {})
                            }
                            for col_name, col_info in node.get('columns', {}).items()
                        ],
                        'sql': node.get('raw_sql', ''),
                        'tags': node.get('tags', []),
                        'meta': node.get('meta', {}),
                        'depends_on': node.get('depends_on', {}).get('nodes', [])
                    }
                    self.metadata['models'].append(model_info)
            
            # Process sources
            for node_id, node in manifest.get('sources', {}).items():
                source_info = {
                    'name': node.get('name'),
                    'description': node.get('description', ''),
                    'tables': node.get('tables', []),
                    'meta': node.get('meta', {})
                }
                self.metadata['sources'].append(source_info)
            
            # Extract relationships from column tests
            for model in self.metadata['models']:
                for column in model.get('columns', []):
                    for test in column.get('tests', []):
                        if isinstance(test, dict) and 'relationships' in test:
                            self.metadata['relationships'].append({
                                'from_model': model['name'],
                                'from_column': column['name'],
                                'to_model': test['relationships'].get('to'),
                                'to_column': test['relationships'].get('field')
                            })
            
            return self.metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {str(e)}")
            return None

    def save_metadata(self, output_file: str):
        """Save the extracted metadata to a JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

def main():
    # Initialize the extractor
    project_dir = os.getenv('DBT_PROJECT_DIR')
    if not project_dir:
        print("Error: DBT_PROJECT_DIR environment variable not set")
        return
    
    extractor = DbtMetadataExtractor(project_dir)
    
    # Test connection
    if not extractor.test_connection():
        print("Failed to connect to dbt")
        return
    
    # Extract metadata
    metadata = extractor.extract_model_metadata()
    
    if metadata:
        # Save to a JSON file
        os.makedirs('chatdbt_raw_data', exist_ok=True)
        output_file = 'chatdbt_raw_data/dbt_metadata.json'
        extractor.save_metadata(output_file)
        print(f"Metadata has been extracted and saved to {output_file}")
    else:
        print("Failed to extract metadata from dbt Core")

if __name__ == "__main__":
    main() 