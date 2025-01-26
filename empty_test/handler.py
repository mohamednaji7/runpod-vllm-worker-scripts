import runpod
import logging


def handler(job):
    """ Handler function that will be used to process jobs. """

    job_input = job['input']
    route = 'None'
    if 'openai_input' in  job_input:
        route = job_input.get['openai_route']
        job_input = job_input['openai_input']

    if 'messages' in job_input:
        input_to_process = job_input.get('messages')
    elif 'prompt' in job_input:
        input_to_process = job_input.get("prompt")

    output =  {"input_to_process": input_to_process,
             "route": f"Receveid on route {route}",
             "received_job_input": job['input']}
    logging.info(output)

    return output


runpod.serverless.start({"handler": handler})