import asyncio
from typing import Dict, Any
import json

# Instead of using sglang.backend, we'll create a simple base worker
class BaseWorker:
    def __init__(self):
        self.model_name = None

class DummyWorker(BaseWorker):
    def __init__(self):
        super().__init__()
        self.model_name = "dummy-model"
        
    async def handle_request(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming requests
        """
        prompt = request_dict.get("prompt", "")
        response = {
            "text": f"Dummy response to: {prompt}",
            "status": "success",
            "model": self.model_name
        }
        return response

    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Basic generation method
        """
        return f"Dummy response to: {prompt}"

    async def start(self, host: str, port: int):
        """
        Start the worker service
        """
        print(f"Starting dummy worker on {host}:{port}")
        # In a real implementation, you'd set up a server here
        await asyncio.sleep(0.1)  # Simulate startup

    async def stop(self):
        """
        Stop the worker service
        """
        print("Stopping dummy worker")