import runpod
import logging


def handler(job):
    """Handler function that processes jobs."""
    job_input = job.get("input", {})
    output = {}

    if "openai_input" in job_input:
        openai_input = job_input["openai_input"]
        messages = openai_input.get("messages", [])
        route = job_input.get("openai_route", "unknown route")

        state = {"messages": messages, "openai_route": f"Received on route {route}"}
        logging.info(state)

        # Respond with a mock completion
        output = {
            "model": "mock-model",  # Include a model name
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "RunPod is the best because it offers great scalability.",
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 15,
                "total_tokens": 25,
            },
        }
    else:
        # Handle missing input case
        output = {
            "error": "No openai_input found",
            "received_job_input": job_input,
        }

        logging.info({'output': output})
        return output


runpod.serverless.start({"handler": handler})
