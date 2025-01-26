# src/worker_vllm_unsloth_tinyllama_bnb_4bit.py

import runpod
from mock_model import MockModel

# Initialize the Unsloth model
unsloth_model = MockModel()

async def handler(job):
    """Handle incoming job requests and generate responses using the Unsloth model."""
    prompt = job["input"]["prompt"]
    max_new_tokens = job["input"].get("max_new_tokens", 128)
    response = unsloth_model.generate_response(prompt, max_new_tokens)
    return {"response": response}

runpod.serverless.start({
    "handler": handler,
    "concurrency_modifier": lambda x: 300,  # Adjust the concurrency as needed
    "return_aggregate_stream": True,
})