import os

# DBT Variables Access
dbt_token = os.getenv("DBT_API_TOKEN")
dbt_account = os.getenv("ACCOUNT_ID")
dbt_project = os.getenv("PROJECT_ID")

# Claude credentials
claude_token = os.getenv("CLAUDE_API_TOKEN")
claude_url = os.getenv("CLAUDE_API_URL")

# Slack Variables
slack_client = os.getenv("CLIENT_ID")

# Prompt of our agent
prompt = """
You are a helpful assistant that can answer questions and help with tasks.
"""