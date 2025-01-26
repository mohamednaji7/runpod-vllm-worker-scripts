import json
import runpod

def handler(job):
    """Handler function to process jobs."""
    job_input = job['input']
    prompt = job_input.get('prompt', 'Hello, World!')
    # Replace this with your model's inference logic
    response_text = f"Generated response for: {prompt}"
    return json.dumps({"choices": [{"text": response_text}]})

runpod.serverless.start({"handler": handler})
