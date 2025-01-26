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


async def handler(job):
    """ Handler function that will be used to process jobs. """
    
    # Get the port from environment variable or default to 8080
    port = os.environ.get('PORT', '8080')

    # Start the OpenAI server
    try:
        subprocess.run(['python3', 'openai_server.py', port], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start openai_server.py: {e}")


    logging.info("[Processing] request...")

    job_input = job['input']

    name = job_input.get('name', 'World')
    output = f"`handler_hello.py` Hello, {name}!"
    logging.info(f"[handler] output: {output}.")
    return output

runpod.serverless.start({"handler": handler})