# handler.py
import runpod
import os
import logging
from engine import UnslothEngine

engine = UnslothEngine()

def get_max_concurrency(default=300):
    return int(os.getenv('MAX_CONCURRENCY', default))

async def async_handler(job):
    try:
        job_input = job.get("input", {})
        messages = job_input.get('messages', [])
        
        response = engine.handle_request(messages)
        yield response
    
    except Exception as e:
        logging.error(f"Handler error: {e}")
        yield {
            "success": False,
            "error": str(e),
            "message": "Failed to process job"
        }

runpod.serverless.start({
    "handler": async_handler, 
    "concurrency_modifier": get_max_concurrency, 
    "return_aggregate_stream": True
})