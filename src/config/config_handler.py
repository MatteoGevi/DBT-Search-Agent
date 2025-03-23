import os
from dotenv import load_dotenv
from typing import Dict, Optional

class ConfigHandler:
    def __init__(self):
        load_dotenv()
        
        # Slack configuration
        self.slack_config = {
            'token': os.getenv('SLACK_TOKEN'),
            'signing_secret': os.getenv('SLACK_SIGNING_SECRET'),
            'client_id': os.getenv('CLIENT_ID')
        }
        
        # DBT configuration
        self.dbt_config = {
            'api_token': os.getenv('DBT_API_TOKEN'),
            'account_id': os.getenv('ACCOUNT_ID'),
            'project_id': os.getenv('PROJECT_ID')
        }
        
        # Teams configuration
        self.teams_config = {
            'app_id': os.getenv('TEAMS_APP_ID'),
            'app_password': os.getenv('TEAMS_APP_PASSWORD')
        }
        
        # Google Chat configuration
        self.gchat_config = {
            'project_id': os.getenv('GOOGLE_CLOUD_PROJECT'),
            'credentials_path': os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        }

    def get_platform_config(self, platform: str) -> Dict:
        """Get configuration for specific platform."""
        config_map = {
            'slack': self.slack_config,
            'teams': self.teams_config,
            'gchat': self.gchat_config,
            'dbt': self.dbt_config
        }
        return config_map.get(platform, {})

    def validate_config(self, platform: str) -> bool:
        """Validate if all required configurations are present for a platform."""
        config = self.get_platform_config(platform)
        return all(config.values())

    @property
    def available_platforms(self) -> list:
        """Get list of platforms with valid configurations."""
        platforms = []
        for platform in ['slack', 'teams', 'gchat']:
            if self.validate_config(platform):
                platforms.append(platform)
        return platforms 