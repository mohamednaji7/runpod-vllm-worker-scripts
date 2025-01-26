import os
from openai import OpenAI

# Fetch environment variables
api_key = os.environ.get("RUNPOD_API_KEY")
endpoint_id = os.environ.get("ENDPOINT_ID")

client = OpenAI(
    api_key=api_key,
    base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
)

response = client.chat.completions.create(
    model="No names yet...",
    messages=[{"role": "user", "content": "Why is RunPod the best platform?"}],
    temperature=0,
    max_tokens=100,
)

print(response)