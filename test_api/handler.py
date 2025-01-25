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