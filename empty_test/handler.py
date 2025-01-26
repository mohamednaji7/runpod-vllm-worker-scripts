import runpod
import logging


def handler(job):
    """ Handler function that will be used to process jobs. """

    job_input = job['input']

    if 'openai_input' in  job_input:
        output =  {"messages": job_input['openai_input']['messages'],
                "openai_route": f"Receveid on route {job_input['openai_route']}"}
    else:
        output =  {"prompt":job_input.get("prompt", "No prompt found")}

    output["received_job_input"] = job_input

    logging.info(output)

    return output


runpod.serverless.start({"handler": handler})