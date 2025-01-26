import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float
    max_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, str]]

@app.post("/openai/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    # Return a dummy response for testing
    return ChatCompletionResponse(
        id="dummy-id",
        object="text_completion",
        created=1234567890,
        model=request.model,
        choices=[{
            "text": "This is a dummy response from the model.",
            "index": 0,
            "logprobs": None,
            "finish_reason": "length"
        }]
    )

if __name__ == "__main__":
    import uvicorn
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)