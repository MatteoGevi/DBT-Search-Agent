import os
from dotenv import load_dotenv
from src.utils import DbtMetadataExtractor

def check_env_variables():
    """Check if DBT_PROJECT_DIR environment variable is set."""
    if not os.getenv('DBT_PROJECT_DIR'):
        raise ValueError("Missing required environment variable: DBT_PROJECT_DIR")
    return True

def test_dbt_connection():
    """Test the connection to local dbt Core installation."""
    try:
        # Initialize the extractor
        project_dir = os.getenv('DBT_PROJECT_DIR')
        extractor = DbtMetadataExtractor(project_dir)
        
        # Test connection using dbt debug
        if extractor.test_connection():
            print("✅ Successfully connected to dbt Core")
            return True
        else:
            print("❌ Failed to connect to dbt Core")
            return False
    except Exception as e:
        print(f"❌ Error connecting to dbt Core: {str(e)}")
        return False

def main():
    print("\n🔍 Testing DBT Connection and Metadata Extraction")
    print("===============================================")
    
    try:
        # Load environment variables
        load_dotenv()
        print("✅ Environment variables loaded successfully")

        # Check required environment variables
        check_env_variables()
        print("✅ All required environment variables are present")

        # Test dbt connection
        if test_dbt_connection():
            # Extract metadata
            project_dir = os.getenv('DBT_PROJECT_DIR')
            extractor = DbtMetadataExtractor(project_dir)
            metadata = extractor.extract_model_metadata()
            
            if metadata:
                # Save the metadata
                os.makedirs('chatdbt_raw_data', exist_ok=True)
                output_file = 'chatdbt_raw_data/dbt_metadata.json'
                extractor.save_metadata(output_file)
                print(f"✅ Metadata extracted and saved to {output_file}")
            else:
                print("❌ Failed to extract metadata")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 