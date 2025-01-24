import runpod
import os
print("[STARTING] handler...")

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


def handler(job):
    """ Handler function that will be used to process jobs. """

    logging.info("[Processing] request...")

    job_input = job['input']

    name = job_input.get('name', 'World')
    output = f"Hello, {name}!"
    logging.info(f"[handler] output: {output}.")
    return output

logging.info("[STARTING] HANDLER...")

runpod.serverless.start({"handler": handler})