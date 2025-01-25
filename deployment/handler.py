# handler.py
import runpod
import os
import logging
from engine import UnslothEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('runpod_handler.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize engine
engine = UnslothEngine()

def get_max_concurrency(default=300):
    """Get maximum concurrency from environment variable."""
    return int(os.getenv('MAX_CONCURRENCY', default))

async def async_handler(job):
    """Asynchronous job handler with comprehensive logging."""
    job_id = job.get('id', 'Unknown')
    logger.info(f"Processing job: {job_id}")
    
    try:
        # Extract job input
        job_input = job.get("input", {})
        messages = job_input.get('messages', [])
        
        logger.info(f"Job {job_id}: Received {len(messages)} messages")
        
        # Handle request
        response = engine.handle_request(messages)
        
        logger.info(f"Job {job_id}: Processed successfully")
        yield response
    
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        yield {
            "success": False,
            "error": str(e),
            "message": "Failed to process job"
        }

# Start RunPod serverless function
runpod.serverless.start({
    "handler": async_handler, 
    "concurrency_modifier": get_max_concurrency, 
    "return_aggregate_stream": True
})