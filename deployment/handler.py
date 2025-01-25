import asyncio
import requests
from engine import UnslothEngine
from utils import process_response
import runpod
import os
import logging

# Initialize the engine
engine = UnslothEngine()
engine.start_server()
engine.wait_for_server()


def get_max_concurrency(default=300):
    """
    Returns the maximum concurrency value.
    By default, it uses 50 unless the 'MAX_CONCURRENCY' environment variable is set.

    Args:
        default (int): The default concurrency value if the environment variable is not set.

    Returns:
        int: The maximum concurrency value.
    """
    return int(os.getenv('MAX_CONCURRENCY', default))



async def async_handler(job):
    """Handle the requests asynchronously."""
    try:
        job_input = job["input"]
        print(f"JOB_INPUT: {job_input}")
        
        if job_input.get("openai_route"):
            openai_route, openai_input = job_input.get("openai_route"), job_input.get("openai_input")

            openai_url = f"{engine.base_url}" + openai_route
            headers = {"Content-Type": "application/json"}

            response = requests.post(openai_url, headers=headers, json=openai_input)
            # Process the streamed response
            if openai_input.get("stream", False):
                for formated_chunk in process_response(response):
                    yield formated_chunk
            else:
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        yield decoded_chunk        
        else:
            generate_url = f"{engine.base_url}/generate"
            headers = {"Content-Type": "application/json"}
            # Directly pass `job_input` to `json`. Can we tell users the possible fields of `job_input`?
            response = requests.post(generate_url, json=job_input, headers=headers)
            if response.status_code == 200:
                yield response.json()
            else:
                yield {"error": f"Generate request failed with status code {response.status_code}", "details": response.text}
    except Exception as e:
        """ Handler function that will be used to process jobs. """
        logging.info("\nFalied to use unsloth or module\n" + "_"*70 + f"\n{e}")
        logging.info("Faling back to the erro handler")
        logging.info("[Processing] request...")
        job_input = job['input']

        name = job_input.get('name', 'World 7!')
        output = f"[handler ERR] Hello, {name}!"
        logging.info(f"[handler ERR] output: {output}.")
        yield output


runpod.serverless.start({"handler": async_handler, "concurrency_modifier": get_max_concurrency, "return_aggregate_stream": True})
