import os
import re
import json
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from metadata_retrieval import fetch_dbt_models, parse_model_metadata

# Initialize Slack client with bot token from environment variables
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# Load dbt metadata
models_data = fetch_dbt_models()
dbt_metadata_df = parse_model_metadata(models_data) if models_data else None

def search_dbt_metadata(query):
    """Searches dbt metadata for matching models or fields based on the query."""
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
    text = event_data['event']['text']
    user_query = re.sub(r'<@.*?>', '', text).strip()  # Remove bot mentions from text
    
    results = search_dbt_metadata(user_query)
    response_message = format_results(results)

    channel_id = event_data['event']['channel']
    try:
        client.chat_postMessage(channel=channel_id, text=response_message)
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

def process_event(event_data):
    """Processes incoming events and determines if the bot needs to respond."""
    if 'bot_id' in event_data['event']:  # Ignore messages from bots
        return
    
    if 'text' in event_data['event']:
        handle_message(event_data)

# Flask app to handle Slack Events
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    
    if "challenge" in data:
        return Response(data["challenge"], status=200, mimetype='application/json')

    if data["event"]["type"] == "app_mention":
        process_event(data)
    
    return Response(status=200)

if __name__ == "__main__":
    # Run the Flask app
    app.run(port=3000)