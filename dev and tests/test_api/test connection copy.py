
from openai import OpenAI
import os

base_url=os.environ.get("RUNPOD_BASE_URL")
api_key=os.environ.get("RUNPOD_API_KEY")
print(base_url, api_key)
client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

messages = [
    {
        "role": "assistant",
        "content": "Hello, I'm your assistant. How can I help you today?",
    }
]

def get_assistant_response(messages):
    r = client.chat.completions.create(
        model="your_model_name",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        temperature=0.7,
        top_p=0.8,
        max_tokens=100,
    )
    response = r.choices[0].message.content
    return response

# Example usage
prompt = "Your prompt here"
messages.append({"role": "user", "content": prompt})
response = get_assistant_response(messages)
print(response)