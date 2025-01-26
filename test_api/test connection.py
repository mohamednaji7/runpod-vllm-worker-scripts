import openai
import asyncio

async def run():
    runpod_endpoint_id = "nqe3wqry3h7noa"
    runpod_api_key = "rpa_AOCVOF0Q05X0QVBS4YY096BP674SA3AQXEZCKEHH113m1b"
    runpod_base_url = f"https://api.runpod.ai/v2/{runpod_endpoint_id}/openai/v1"

    openai.api_base = runpod_base_url
    openai.api_key = runpod_api_key

    # Print out parameters to debug
    print("Parameters being sent to OpenAI:")
    params = {
        "model": "NousResearch/Meta-Llama-3-8B-Instruct",
        "prompt": "Classify this sentiment: vLLM is wonderful!",
        "max_tokens": 50
    }
    print(params)

    # Sending the request
    response = await openai.Completion.acreate(**params)

    # Print the response
    print("Response from OpenAI API:")
    print(response)


# Run the async functi
asyncio.run(run())