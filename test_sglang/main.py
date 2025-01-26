import asyncio
import runpod
from worker import DummyWorker
from config import WORKER_CONFIG

async def dummy_handler(job):
    worker = DummyWorker()
    try:
        response = await worker.handle_request(job["input"])
        return response
    except Exception as e:
        return {"status": "error", "error": str(e)}

def handler(job):
    return asyncio.run(dummy_handler(job))

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})