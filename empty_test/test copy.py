import os
from openai import OpenAI

print(os.environ.get("RUNPOD_API_KEY"))
print(os.environ.get("ENDPOINT_ID"))
client = OpenAI(
    api_key=os.environ.get("RUNPOD_API_KEY"),
    base_url=f"https://api.runpod.ai/v2/{os.environ.get("ENDPOINT_ID")}/openai/v1",
)

response = client.chat.completions.create(
    model="No names yet...",
    messages=[{"role": "user", "content": "Why is RunPod the best platform?"}],
    temperature=0,
    max_tokens=100,
)