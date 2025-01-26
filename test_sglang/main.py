import asyncio
from worker import DummyWorker
from config import WORKER_CONFIG

async def main():
    # Initialize the worker
    worker = DummyWorker()
    
    # Start the worker
    await worker.start(
        host=WORKER_CONFIG["host"],
        port=WORKER_CONFIG["port"]
    )
    
    try:
        # Keep the worker running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Graceful shutdown
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())