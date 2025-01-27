import logging
logging.basicConfig(
    level=logging.INFO,       # Set the minimum logging level
    format='[%(levelname)s] %(message)s'  # Text-only format
)
rich_console = logging

logging.info("[STARTING] HANDLER.....")

import runpod
from model_wraper import UnslothModel

model = UnslothModel()

def handler(job):
    """ Handler function that will be used to process jobs. """
    logging.info("[Processing] request...")

    job_input = job['input']

    prompt = job_input.get('prompt', False)
    if prompt != False:
        # [{"role": 'None', 'content': prompt}]
        model.max_new_tokens = job_input.get('max_new_tokens', model.max_new_tokens)
        output = model.generate_response(prompt)
    else:
        output = f"echo: No prompt Found!"

    logging.info(f"[handler] output: {output[:50]}.")
    return output



runpod.serverless.start({"handler": handler})