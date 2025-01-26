

## Initialize the model
model = MockModel()
## Initialize the engine
engine = OpenaiEngine(model)

import runpod
from openai import OpenAI

# Your model implementation here
class YourModel():
    def generate(seld, mgs):
        return "Dummy response!"
    
model = YourModel()

def chat_completions_handler(job):
    messages = job['input']['messages']
    # Process messages with your model
    response = model.generate(messages)
    
    return {
        "id": f"chatcmpl-{job['id']}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": job['input'].get('model', 'your-model-name'),
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": "stop"
        }],
        "usage": {
            # Implement token counting logic here
        }
    }

def models_handler(job):
    # Return list of available models
    return {
        "data": [
            {
                "id": "your-model-name",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "your-organization"
            }
        ],
        "object": "list"
    }

def handler(job):
    if job['input']['path'] == '/v1/chat/completions':
        return chat_completions_handler(job)
    elif job['input']['path'] == '/v1/models':
        return models_handler(job)
    else:
        raise ValueError("Unsupported path")

runpod.serverless.start({"handler": handler})


