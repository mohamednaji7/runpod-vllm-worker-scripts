import runpod
import logging


def handler(job):
    """ Handler function that will be used to process jobs. """

    job_input = job['input']
    output = {}

    if 'openai_input' in  job_input:
        state =  {"messages": job_input['openai_input']['messages'],
                "openai_route": f"Receveid on route {job_input['openai_route']}"}
        logging.info(state)

        # messages = job_input['openai_input']['messages']
        output = {
            "choices": [
                {"message": {"role": "assistant", "content": "RunPod is the best because it offers great scalability."}}
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
        }
    else:
        output =  {"prompt":job_input.get("prompt", "No prompt found"),
                   "error": "No openai_input found"}
        output["received_job_input"] = job_input
    
    logging.info(output)
    return output

runpod.serverless.start({"handler": handler})