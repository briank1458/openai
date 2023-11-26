#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Setup
import os
from openai import OpenAI, ChatCompletion
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to OpenAI API
client = OpenAI()

# Connect to Slack API
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)

#client.models.list()


# In[ ]:


@app.route('/slack/events', methods=['POST'])

def listen_and_reply():
    payload = request.json

    # Check the event type
    if payload['type'] == 'url_verification':
        # URL verification challenge
        return jsonify({'challenge': payload['challenge']})
    elif payload['type'] == 'event_callback':
        event = payload['event']

        if event['type'] == 'message' and 'bot_id' not in event:
            user = event['user']
            text = event['text']
            channel = event['channel']
    
    # Get the most recent message from Slack channel
    # result = slack_client.conversations_history(channel=channel_id, limit=1)
    # last_message = result.data['messages'][0]['text']

            # Set up ChatGPT thread
            model = 'gpt-3.5-turbo'
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text},
                ]

            # Generate ChatGPT response
            response = client.chat.completions.create(
                model=model,
                messages=messages
                )
    
            # Parse Assistant reply
            assistant_reply = response.choices[0].message.content
    
            # Post assistant reply to Slack channel
            try:
                response = slack_client.chat_postMessage(channel=channel, text=assistant_reply)
            except SlackApiError as e:
                assert e.response["error"]

        return jsonify({'status': 200})

if __name__ == "__main__":
    app.run(port=5000)

