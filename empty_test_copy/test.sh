
#!/bin/bash

# Display the RunPod endpoint and API key

# echo "ENDPOINT ID: $ENDPOINT_ID"

# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_openai_URL"
# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_run_URL"
# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_runsync_URL"

# echo "RunPod API Key: $RUNPOD_API_KEY"

# # Make a cURL request to RunPod API
# curl "$RUNPOD_ENDPOINT_openai_URL" \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $RUNPOD_API_KEY" \
#   -d '{
#     "model": "your-custom-model",
#     "messages": [
#       {
#         "role": "user",
#         "content": "Why is RunPod the best platform?"
#       }
#     ],
#     "temperature": 0,
#     "max_tokens": 100
#   }'
# curl -X POST https://api.runpod.ai/v2/$ENDPOINT_ID/runsync     -H 'Content-Type: application/json'     -H "Authorization: Bearer $API_KEY"     -d '{"input": {"prompt": "Your prompt"}}'
curl -X POST https://api.runpod.ai/v2/$ENDPOINT_ID/runsync \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"input": {"prompt": "Your prompt"}}'

# https://api.runpod.ai/v2/{endpoint_id}/runsync
# https://api.runpod.ai/v2/nqe3wqry3h7noa/runsync