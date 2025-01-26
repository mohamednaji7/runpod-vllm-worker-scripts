import runpod
import subprocess
import os
import logging

# Configure logging
if os.environ.get('SCRIPT_NAME') is not None:
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging
else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()

logging.info("[STARTING] HANDLER.....")

# Function to start the OpenAI server
def start_openai_server(port):
    """Start the OpenAI server in a non-blocking way."""
    try:
        # Use Popen to start the server without blocking
        subprocess.Popen(['python3', 'openai_server.py', port])
        logging.info(f"OpenAI server started on port {port}.")
    except Exception as e:
        logging.error(f"Failed to start openai_server.py: {e}")

async def handler(job):
    """ Handler function that will be used to process jobs. """
    
    # Get the port from environment variable or default to 8080
    port = os.environ.get('PORT', '8080')

    # Start the OpenAI server (non-blocking)
    start_openai_server(port)

    logging.info("[Processing] request...")

    job_input = job['input']

    name = job_input.get('name', 'World')
    output = f"`handler.py` Hello, {name}!"
    logging.info(f"[handler] output: {output}.")
    return output

runpod.serverless.start({"handler": handler})
