
#!/bin/bash

# Display the RunPod endpoint and API key

# echo "ENDPOINT ID: $ENDPOINT_ID"

# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_openai_URL"
# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_run_URL"
# echo "RunPod Endpoint: $RUNPOD_ENDPOINT_runsync_URL"

# echo "RunPod API Key: $RUNPOD_API_KEY"

# Make a cURL request to RunPod API
curl "$RUNPOD_ENDPOINT_openai_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -d '{
    "model": "your-custom-model",
    "messages": [
      {
        "role": "user",
        "content": "Why is RunPod the best platform?"
      }
    ],
    "temperature": 0,
    "max_tokens": 100
  }'
