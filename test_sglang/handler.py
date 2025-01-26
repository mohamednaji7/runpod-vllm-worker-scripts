
import asyncio
import requests
from utils import process_response
import runpod
import os

# from engine import SGlangEngine
# # Initialize the engine
# engine = SGlangEngine()
# engine.start_server()
# engine.wait_for_server()


def get_max_concurrency(default=300):
    return int(os.getenv('MAX_CONCURRENCY', default))


async def async_handler(job):
    """Handle the requests asynchronously."""
    job_input = job["input"]
    print(f"JOB_INPUT: {job_input}")
    
    if job_input.get("openai_route"):
        openai_route, openai_input = job_input.get("openai_route"), job_input.get("openai_input")
        host="0.0.0.0"
        port=30000
        base_url = f"http://{host}:{port}"
        openai_url =  base_url + openai_route
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
        generate_url = base_url+"/generate"
        headers = {"Content-Type": "application/json"}
        # Directly pass `job_input` to `json`. Can we tell users the possible fields of `job_input`?
        response = requests.post(generate_url, json=job_input, headers=headers)
        if response.status_code == 200:
            yield response.json()
        else:
            yield {"error": f"Generate request failed with status code {response.status_code}", "details": response.text}

runpod.serverless.start({"handler": async_handler, "concurrency_modifier": get_max_concurrency, "return_aggregate_stream": True})



# async def async_handler(job):
#     """Handle the requests asynchronously."""
#     job_input = job["input"]
#     print(f"JOB_INPUT: {job_input}")
    
#     if job_input.get("openai_route"):
#         openai_route, openai_input = job_input.get("openai_route"), job_input.get("openai_input")

#         openai_url = f"{engine.base_url}" + openai_route
#         headers = {"Content-Type": "application/json"}

#         response = requests.post(openai_url, headers=headers, json=openai_input)
#         # Process the streamed response
#         if openai_input.get("stream", False):
#             for formated_chunk in process_response(response):
#                 yield formated_chunk
#         else:
#             for chunk in response.iter_lines():
#                 if chunk:
#                     decoded_chunk = chunk.decode('utf-8')
#                     yield decoded_chunk        
#     else:
#         generate_url = f"{engine.base_url}/generate"
#         headers = {"Content-Type": "application/json"}
#         # Directly pass `job_input` to `json`. Can we tell users the possible fields of `job_input`?
#         response = requests.post(generate_url, json=job_input, headers=headers)
#         if response.status_code == 200:
#             yield response.json()
#         else:
#             yield {"error": f"Generate request failed with status code {response.status_code}", "details": response.text}

