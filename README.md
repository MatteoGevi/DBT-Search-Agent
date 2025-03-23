# DBT Search Agent

[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://slack.com)
[![Microsoft Teams](https://img.shields.io/badge/Microsoft_Teams-6264A7?style=for-the-badge&logo=microsoft-teams&logoColor=white)](https://teams.microsoft.com)
[![Google Chat](https://img.shields.io/badge/Google%20Chat-00AC47?style=for-the-badge&logo=google-chat&logoColor=white)](https://workspace.google.com/products/chat/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

A chatbot that helps users understand and query dbt models across multiple messaging platforms using native platform integrations.

## Features

- Query dbt model descriptions and metadata
- Get column information and lineage
- View model relationships and dependencies
- Multi-platform support:
  - Slack (using slack-sdk)
  - Microsoft Teams (using microsoft-teams-sdk)
  - Google Chat (using google-cloud-pubsub)

## Architecture

```
DBT-Search-Agent/
├── src/
│   ├── bot/           # Platform-specific bot implementations
│   ├── config/        # Configuration management
│   ├── actions/       # Query handling and responses
│   └── main.py        # Application entry point
├── models/            # Your dbt models
└── docker/            # Containerization
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- dbt Cloud account
- Platform-specific credentials:
  - Slack Bot Token
  - Microsoft Teams App credentials
  - Google Chat API credentials

## Local Development

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your platform credentials
```

3. Run locally:
```bash
python -m src.main
```

## Production Deployment

### 1. Build the Container

```bash
docker build -t dbt-search-bot .
```

### 2. Deploy to Cloud Platform

Choose your preferred platform:

#### Option A: Google Cloud Run
```bash
# Initialize Google Cloud
gcloud init

# Deploy container
gcloud run deploy dbt-search-bot \
  --image dbt-search-bot \
  --platform managed \
  --allow-unauthenticated
```

#### Option B: AWS ECS
```bash
# Configure AWS CLI
aws configure

# Create ECR repository
aws ecr create-repository --repository-name dbt-search-bot

# Push and deploy
aws ecs create-service ...
```

### 3. Platform-Specific Setup

#### Slack
1. Create app at api.slack.com
2. Add scopes:
   - chat:write
   - im:history
   - im:read
   - im:write
3. Install to workspace
4. Add token to .env

#### Microsoft Teams
1. Register in Azure AD
2. Create bot channel
3. Configure webhook URL
4. Add to Teams

#### Google Chat
1. Enable Chat API
2. Configure bot
3. Set up pub/sub

## Environment Variables

```bash
# Slack
SLACK_TOKEN=xxx
SLACK_SIGNING_SECRET=xxx
CLIENT_ID=xxx

# Microsoft Teams
TEAMS_APP_ID=xxx
TEAMS_APP_PASSWORD=xxx

# Google Chat
GOOGLE_CLOUD_PROJECT=xxx
GOOGLE_APPLICATION_CREDENTIALS=xxx

# DBT Cloud
DBT_API_TOKEN=xxx
ACCOUNT_ID=xxx
PROJECT_ID=xxx
```

## How It Works

1. **Metadata Extraction**:
   - Connects to dbt Cloud API
   - Extracts model definitions, relationships, and documentation
   - Caches metadata for quick responses

2. **Query Processing**:
   - Receives messages from any configured platform
   - Processes natural language queries
   - Returns relevant dbt metadata

3. **Platform Integration**:
   - Uses native SDKs for each platform
   - Maintains persistent connections
   - Handles platform-specific message formats

## Security Considerations

- All credentials stored as environment variables
- HTTPS endpoints required
- Regular API key rotation
- Rate limiting implemented
- Activity monitoring

## Support

For issues and feature requests, please create an issue in the repository.


