import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLAUDE_API_KEY")

url = "https://api.anthropic.com/v1/messages"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01"
}

payload = {
    "model": "claude-sonnet-4-5",
    "max_tokens": 1000,
    "messages": [
        {
            "role": "user",
            "content": "What should I search for to find the latest developments in renewable energy?"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())
