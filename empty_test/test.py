import os
import requests

# Fetch environment variables
api_key = os.environ.get("RUNPOD_API_KEY")
endpoint_id = os.environ.get("ENDPOINT_ID")


print(api_key)
print(endpoint_id)


if not api_key or not endpoint_id:
    raise ValueError("Missing environment variables: RUNPOD_API_KEY or ENDPOINT_ID.")

# Define the API endpoint
url = f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1/chat/completions"

# Prepare the headers and payload
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "No names yet...",  # Replace with the correct model name
    "messages": [
        {"role": "user", "content": "Why is RunPod the best platform?"}
    ],
    "temperature": 0,
    "max_tokens": 100
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Handle the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
