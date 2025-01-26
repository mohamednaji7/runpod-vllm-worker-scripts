import asyncio
import runpod
from worker import DummyWorker
from config import WORKER_CONFIG

# Create a global worker instance
worker = DummyWorker()
import requests
import json

def test_worker():
    url = "http://localhost:8000/run"  # Note the /run endpoint
    payload = {
        "input": {
            "prompt": "Hello, world!"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(json.dumps(response.json(), indent=2))

def handler(job):
    """
    Handler function for runpod serverless
    """
    try:
        # Get the event loop
        loop = asyncio.get_event_loop()
        
        # Run the async handler in the existing event loop
        response = loop.run_until_complete(worker.handle_request(job["input"]))
        return response
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": str(type(e).__name__)
        }

if __name__ == "__main__":

    test_worker()
    runpod.serverless.start({"handler": handler})