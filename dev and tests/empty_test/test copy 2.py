import os
import openai

# Fetch environment variables
api_key = os.environ.get("RUNPOD_API_KEY")
endpoint_id = os.environ.get("ENDPOINT_ID")

if not api_key or not endpoint_id:
    raise ValueError("Missing environment variables: RUNPOD_API_KEY or ENDPOINT_ID.")

# Configure the OpenAI library with a custom base URL
openai.api_key = api_key
openai.api_base = f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1"

# Make a request to the chat completions endpoint
response = openai.ChatCompletion.create(
    model="mock-model",
    messages=[{"role": "user", "content": "Why is RunPod the best platform?"}],
    temperature=0,
    max_tokens=100,
)

# Print the response
print(response)
