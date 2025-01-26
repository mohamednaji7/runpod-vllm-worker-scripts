import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)

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
    logging.info(f"Received request: {request}")
    try:
        # Return a dummy response for testing
        response = ChatCompletionResponse(
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
        logging.info(f"Sending response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)