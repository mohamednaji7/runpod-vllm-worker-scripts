from typing import Dict, Any
import sglang as sgl
from sglang.backend.runtime_endpoint import BaseWorker

class DummyWorker(BaseWorker):
    def __init__(self):
        super().__init__()
        self.model_name = "dummy-model"
        
    async def generate_stream(self, 
                            prompt: str, 
                            sampling_params: Dict[str, Any],
                            request_id: str = "") -> str:
        """
        Simulates a streaming response for the dummy worker
        """
        # This is a dummy implementation that just echoes the prompt
        yield "This is a dummy response: " + prompt

    async def generate(self,
                      prompt: str,
                      sampling_params: Dict[str, Any],
                      request_id: str = "") -> str:
        """
        Simulates a single response for the dummy worker
        """
        # Simple dummy implementation
        return "This is a dummy response: " + prompt