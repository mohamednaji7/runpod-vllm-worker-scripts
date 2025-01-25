# handler.py
import runpod
from engine_api import OpenaiEngine
from model_api import MockModel
from openai_routes import OpenAIRoutes
import os

if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG,       
        format='[%(levelname)s] %(message)s'  
    )
    rich_console = logging
else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()

# Initialize the model and engine
model = MockModel()
engine = OpenaiEngine(model)

# Initialize OpenAI Routes
openai_routes = OpenAIRoutes(engine, model)



# Example of make_request_with_retry function
import requests
from time import sleep

def make_request_with_retry(url, method="GET", retries=3, delay=2, headers=None, data=None):
    """
    Make an HTTP request with retry logic.
    
    Args:
        url: The URL to send the request to.
        method: The HTTP method (GET, POST, etc.).
        retries: The number of retries before failing.
        delay: The delay (in seconds) between retries.
        headers: The headers to send with the request.
        data: The body/data for POST requests.
    
    Returns:
        The response object from the request.
    """
    for attempt in range(retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # If response is successful, return it
            if response.status_code == 200:
                rich_console.debug(f"Request successful: {response.status_code}")
                return response
            else:
                rich_console.warning(f"Request failed: {response.status_code}")
        
        except Exception as e:
            rich_console.error(f"Error in request: {e}")
        
        # Retry after delay
        rich_console.info(f"Retrying request... attempt {attempt + 1} of {retries}")
        sleep(delay)

    raise Exception("Max retries reached. Request failed.")



    
def get_max_concurrency(default=300):
    """Get maximum concurrency from environment variable."""
    return int(os.getenv('MAX_CONCURRENCY', default))

async def async_handler(job):
    """Asynchronous job handler with comprehensive logging."""
    job_id = job.get('id', 'Unknown')
    rich_console.info(f"Processing job: {job_id}")
    
    # Extract job input + Handle request
    response = engine.process_job_input(job['input'])
    
    rich_console.info(f"Job {job_id}: Processed successfully")
    yield response

# Expose the OpenAI routes handler
def handler(event):
    return openai_routes.handler(event)

# Start RunPod serverless function
runpod.serverless.start({
    "handler": async_handler, 
    "concurrency_modifier": get_max_concurrency, 
    "return_aggregate_stream": True
})