# DBT Search Agent

[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://slack.com)
[![Microsoft Teams](https://img.shields.io/badge/Microsoft_Teams-6264A7?style=for-the-badge&logo=microsoft-teams&logoColor=white)](https://teams.microsoft.com)
[![Google Chat](https://img.shields.io/badge/Google%20Chat-00AC47?style=for-the-badge&logo=google-chat&logoColor=white)](https://workspace.google.com/products/chat/)

A chatbot that helps users understand and query dbt models across multiple messaging platforms (Slack, Microsoft Teams, and Google Chat).

## Features

- Query dbt model descriptions
- Get column information
- View model relationships
- Multi-platform support (Slack, MS Teams, Google Chat)

## Prerequisites

- Docker and Docker Compose
- dbt Cloud account
- Messaging platform credentials (Slack/Teams/Google Chat)

## Local Development

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables in `.env`:
```bash
# Copy the example env file
cp .env.example .env
# Edit with your credentials
```

3. Train the model:
```bash
rasa train
```

4. Run locally:
```bash
# Terminal 1: Run the Rasa server
rasa run --enable-api --cors "*"

# Terminal 2: Run the actions server
rasa run actions
```

## Production Deployment

### 1. Cloud Platform Setup

Choose one of the following platforms:

#### Option A: Google Cloud Run
1. Install Google Cloud SDK
2. Create a new project
3. Enable Cloud Run API
4. Set up Google Cloud credentials

```bash
# Initialize Google Cloud
gcloud init
# Build and push containers
gcloud builds submit --tag gcr.io/[PROJECT_ID]/rasa-bot
gcloud builds submit --tag gcr.io/[PROJECT_ID]/rasa-actions
```

#### Option B: AWS Elastic Beanstalk
1. Install AWS CLI
2. Create an Elastic Beanstalk application
3. Configure environment variables in EB console

### 2. Deploy Using Docker

1. Build the images:
```bash
docker-compose build
```

2. Push to your container registry:
```bash
docker-compose push
```

3. Deploy to your chosen platform using the provided Dockerfiles and docker-compose.yml

### 3. Messaging Platform Setup

#### Slack
1. Create a Slack App at api.slack.com
2. Add Bot Token Scopes:
   - chat:write
   - im:history
   - im:read
   - im:write
3. Install app to workspace
4. Copy Bot User OAuth Token to .env

#### Microsoft Teams
1. Register app in Azure Active Directory
2. Create a bot channel
3. Configure messaging endpoint
4. Add app to Teams

#### Google Chat
1. Create project in Google Cloud Console
2. Enable Chat API
3. Configure bot settings
4. Download credentials JSON

## Environment Variables

Required environment variables:
```
# Slack
SLACK_TOKEN=your_token
SLACK_CHANNEL=your_channel
SLACK_SIGNING_SECRET=your_secret

# Microsoft Teams
TEAMS_APP_ID=your_app_id
TEAMS_APP_PASSWORD=your_password

# Google Chat
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path_to_credentials.json

# DBT
DBT_API_TOKEN=your_dbt_api_token
ACCOUNT_ID=your_account_id
PROJECT_ID=your_project_id
```

## Maintenance

- Regularly update the model with new training data
- Monitor bot performance and errors
- Keep dependencies updated
- Backup model files and configurations

## Security Considerations

- All credentials should be stored as environment variables
- Use secure HTTPS endpoints
- Regularly rotate API keys
- Implement rate limiting
- Monitor for suspicious activities

## Support

For issues and feature requests, please create an issue in the repository.


