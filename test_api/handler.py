import runpod
import time
import json
import logging
class YourCustomModel:
    def generate(self, messages):
        # Implement your generation logic here
        return "This is a response from your custom model."

model = YourCustomModel()

def chat_completions_handler(job):
    input_data = job['input']
    messages = input_data['messages']
    response = model.generate(messages)

    return {
        "id": f"chatcmpl-{job['id']}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": input_data.get('model', 'your-custom-model'),
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(json.dumps(messages)),
            "completion_tokens": len(response),
            "total_tokens": len(json.dumps(messages)) + len(response)
        }
    }
def handler(job):
    logging.info("job >>")
    logging.info("job >>")
    logging.info(f"job >> {str(job)}")

    if job['input'].get('openai_route') == '/v1/chat/completions':
        return chat_completions_handler(job)
    else:
        raise ValueError("Unsupported openai_route")

runpod.serverless.start({"handler": handler})

