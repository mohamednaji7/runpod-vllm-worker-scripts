
class MockModel:
    def __init__(self):
        self.model_id = "mock-model-1.0"
        self.processed_prompt_tokens = 0
        self.processed_completion_tokens = 0

    def generate_response(self, prompt):
        # For demonstration, the response is a simple echo of the prompt
        self.processed_prompt_tokens = len(prompt.split())
        response = f"Echo: {prompt[:70]}"
        self.processed_completion_tokens = len(response.split()) - self.processed_prompt_tokens
        return response
    