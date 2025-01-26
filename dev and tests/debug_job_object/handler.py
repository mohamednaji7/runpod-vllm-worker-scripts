import os
if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging
else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()
logging.info("[STARTING] TEMP HANDLER.....")

import runpod
import time

def handler(job):
    # Extract the input from the job
    job_input = job.get('input', {})
    
    # Extract the 'messages' list from the input
    messages = job_input.get('messages', [])
    
    # For this dummy example, we'll just echo the user's message
    user_message = ""
    for message in messages:
        if message.get('role') == 'user':
            user_message = message.get('content', '')
            break
    
    # Create a dummy response
    assistant_response = f"Echo: {user_message}"
    
    # Format the response in OpenAI API style
    response = {
        "id": job.get('id', 'dummy_id'),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "dummy-model",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": assistant_response
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(user_message.split()),
            "completion_tokens": len(assistant_response.split()),
            "total_tokens": len(user_message.split()) + len(assistant_response.split())
        }
    }
    
    return response

runpod.serverless.start({"handler": handler})
