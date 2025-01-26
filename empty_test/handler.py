import runpod


def handler(job):
    """ Handler function that will be used to process jobs. """

    job_input = job['input']
    if 'openai_input' in  job_input:
        job_input = job_input['openai_input']

    if 'messages' in job_input:
        input_to_process = job_input.get('messages')
    elif 'prompt' in job_input:
        input_to_process = job_input.get("prompt")

    return  {"route": f"Receveid on route {job_input.get('openai_route', 'other than openai_route')}",
             "input_to_process": input_to_process,
             "input": job_input}

runpod.serverless.start({"handler": handler})