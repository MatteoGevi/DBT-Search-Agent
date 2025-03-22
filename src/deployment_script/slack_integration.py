import os
import re
import pandas as pd
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.utils import fetch_dbt_models, parse_model_metadata

# Initialize Slack client with bot token from environment variables
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# Load dbt metadata
models_data = fetch_dbt_models()
dbt_metadata_df = parse_model_metadata(models_data) if models_data else None

def search_dbt_metadata(query):
    """Searches dbt metadata for matching models or fields based on the query."""
    if dbt_metadata_df is None:
        return pd.DataFrame()  # Return an empty DataFrame if metadata is not loaded

    results = dbt_metadata_df[
        dbt_metadata_df['Model Description'].str.contains(query, case=False, na=False) |
        dbt_metadata_df['Column Description'].str.contains(query, case=False, na=False)
    ]
    return results

def format_results(results):
    """Formats search results into a Slack message-friendly format."""
    if results.empty:
        return "No matching models or fields found for your query."

    message = "Here are the matching models and fields:\n"
    for _, row in results.iterrows():
        message += f"*Model:* {row['Model Name']}\n"
        message += f"  - Description: {row['Model Description']}\n"
        message += f"  - Column: {row['Column Name']} - {row['Column Description']}\n\n"
    return message

def handle_message(event_data):
    """Handles messages received from Slack and responds based on the query."""
    text = event_data.get('text', '')
    user_query = re.sub(r'<@.*?>', '', text).strip()  # Remove bot mentions from text
    
    results = search_dbt_metadata(user_query)
    response_message = format_results(results)

    channel_id = event_data.get('channel')
    try:
        client.chat_postMessage(channel=channel_id, text=response_message)
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

# Flask app to handle Slack Events
app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Main route for Slack events."""
    data = request.json

    # Handle Slack URL verification challenge
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]}), 200

    # Handle Slack events
    if "event" in data:
        event = data["event"]

        # Respond to app mentions
        if event.get("type") == "app_mention":
            user_message = event.get("text", "")
            channel_id = event.get("channel")
            # Process the user's message (custom logic can go here)
            print(f"Received message: {user_message} in channel {channel_id}")
    
    return jsonify({"status": "ok"}), 200

# AWS Lambda handler
def lambda_handler(event, context):
    """Lambda handler for integrating with Flask."""
    # Convert API Gateway event to WSGI request
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': event.get('queryStringParameters', '') or '',
        'CONTENT_TYPE': event.get('headers', {}).get('Content-Type', ''),
        'wsgi.input': event['body'].encode() if event.get('body') else b"",
        'wsgi.url_scheme': 'https',
    }

    # Add required WSGI headers
    for key, value in event.get('headers', {}).items():
        environ[f"HTTP_{key.upper().replace('-', '_')}"] = value

    # Dispatch the request to the Flask app
    request = Request(environ)
    response = DispatcherMiddleware(app)(environ, lambda: None)

    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True),
    }