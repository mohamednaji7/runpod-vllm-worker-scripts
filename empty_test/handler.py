import runpod


def handler(job):
    """ Handler function that will be used to process jobs. """


    job_input = job['input']
    if 'openai_input' in  job_input:
        job_input = job_input['openai_input']

    return  {"output": {"route": f"Receveid on the route {job_input.get('openai_route', 'Not openai_route')}",
                        "input": job_input}}


runpod.serverless.start({"handler": handler})