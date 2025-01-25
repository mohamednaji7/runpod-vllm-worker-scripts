# handler.py
import runpod
from engine_api import OpenaiEngine
from model_api import MockModel
import os

if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    # Configure logging to output plain text to stdout
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging

else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()



## Initialize the model
model = MockModel()
## Initialize the engine
engine = OpenaiEngine(model)

def get_max_concurrency(default=300):
    """Get maximum concurrency from environment variable."""
    return int(os.getenv('MAX_CONCURRENCY', default))

async def async_handler(job):
    """Asynchronous job handler with comprehensive logging."""
    job_id = job.get('id', 'Unknown')
    rich_console.info(f"Processing job: {job_id}")
    
    job_id = job.get('id')
    rich_console.info(f"Processing job: {job_id}")
    
    # Extract job input + Handle request
    response = engine.process_job_input(job['input'])
    
    rich_console.info(f"Job {job_id}: Processed successfully")
    yield response


# Start RunPod serverless function
runpod.serverless.start({
    "handler": async_handler, 
    "concurrency_modifier": get_max_concurrency, 
    "return_aggregate_stream": True
})