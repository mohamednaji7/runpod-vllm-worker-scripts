import os
if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging
else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()
logging.info("[STARTING] HANDLER.....")

import runpod


def handler(job):
    """ Handler function that will be used to process jobs. """
    logging.info("[Processing] request...")

    job_input = job['input']

    name = job_input.get('name', 'World')
    output = f"`handler_hello.py` Hello, {name}!"
    logging.info(f"[handler] output: {output}.")
    return output


runpod.serverless.start({"handler": handler})