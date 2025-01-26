import os
import requests

# Fetch environment variables
api_key = os.environ.get("RUNPOD_API_KEY")
endpoint_id = os.environ.get("ENDPOINT_ID")

if not api_key or not endpoint_id:
    raise ValueError("Missing environment variables: RUNPOD_API_KEY or ENDPOINT_ID.")

# Define the endpoint URL
url = f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1/chat/completions"

# Define the request payload
payload = {
    "model": "mock-model",
    "messages": [{"role": "user", "content": "Why is RunPod the best platform?"}],
    "temperature": 0,
    "max_tokens": 100,
}

# Add headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Make the request
response = requests.post(url, json=payload, headers=headers)

# Check for errors
response.raise_for_status()

# Print the response
print(response.json())
