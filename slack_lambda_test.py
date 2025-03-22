import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack events and respond to URL verification or app mentions."""
    data = request.json

    # Handle Slack URL verification challenge
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Handle Slack events
    if "event" in data:
        event = data["event"]

        # Respond to app mentions
        if event.get("type") == "app_mention":
            user_message = event.get("text", "")
            channel_id = event.get("channel")

            print(f"Received message: {user_message} in channel {channel_id}")
            return jsonify({"text": f"Hello! You said: {user_message}"}), 200

    return jsonify({"status": "ok"}), 200

# AWS Lambda handler
def lambda_handler(event, context):
    """Lambda handler for testing Slack app."""
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.wrappers import Request, Response

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
    response = DispatcherMiddleware(app)(environ, lambda: None)

    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True),
    }