from typing import Dict, Any
import asyncio

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
        try:
            prompt = request_dict.get("prompt", "")
            # Simulate some async work
            await asyncio.sleep(0.1)
            
            response = {
                "status": "success",
                "output": f"Dummy response to: {prompt}",
                "model": self.model_name
            }
            return response
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": str(type(e).__name__)
            }

    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Basic generation method
        """
        await asyncio.sleep(0.1)  # Simulate async work
        return f"Dummy response to: {prompt}"