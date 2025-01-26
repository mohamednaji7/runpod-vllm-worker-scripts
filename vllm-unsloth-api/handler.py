# src/handler.py

import os
import runpod
from utils import JobInput
from engine import vLLMEngine, OpenAIvLLMEngine
from worker_vllm_unsloth_tinyllama_bnb_4bit import handler as unsloth_handler

vllm_engine = vLLMEngine()
OpenAIvLLMEngine = OpenAIvLLMEngine(vllm_engine)

async def handler(job):
    job_input = JobInput(job["input"])
    if job_input.openai_route:
        engine = OpenAIvLLMEngine
    else:
        engine = vllm_engine

    # Route to the Unsloth handler if specified
    if job_input.model_id == "unsloth/tinyllama-bnb-4bit":
        return await unsloth_handler(job)

    results_generator = engine.generate(job_input)
    async for batch in results_generator:
        yield batch

runpod.serverless.start({
    "handler": handler,
    "concurrency_modifier": lambda x: vllm_engine.max_concurrency,
    "return_aggregate_stream": True,
})