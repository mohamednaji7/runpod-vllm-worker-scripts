# openai_routes.py
import json
import os
import time
import logging

# Setup logging configuration
if os.environ.get('SCRIPT_NAME') is not None:
    logging.basicConfig(
        level=logging.DEBUG,       
        format='[%(levelname)s] %(message)s'  
    )
    rich_console = logging
else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()

class OpenAIRoutes:
    def __init__(self, engine, model):
        """
        Initialize OpenAI-compatible routes.
        
        Args:
            engine: The API engine for processing requests
            model: The underlying language model
        """
        self.engine = engine
        self.model = model

    def handle_list_models(self):
        """Handle the /models endpoint to list available models."""
        rich_console.debug("Handling list models request")
        try:
            return {
                "object": "list",
                "data": [
                    {
                        "id": self.model.model_id,
                        "object": "model",
                        "created": int(os.path.getctime("./model")),
                        "owned_by": "unsloth",
                    }
                ]
            }
        except Exception as e:
            rich_console.error(f"Error handling list models: {e}")
            raise

    def handle_chat_completions(self, job_input):
        """Handle chat completions in OpenAI-compatible format."""
        rich_console.debug(f"Handling chat completions with input: {job_input}")
        try:
            return self.engine.process_job_input(job_input)
        except Exception as e:
            rich_console.error(f"Error processing job input for chat completions: {e}")
            raise

    def handler(self, event):
        """Main handler for OpenAI-compatible routes."""
        rich_console.info(f"Received event: {event}")
        
        try:
            # Route handling
            if event.get('httpMethod') == 'GET' and event.get('path') == '/models':
                rich_console.debug("Route matched: /models (GET)")
                response = self.handle_list_models()
                return {
                    'statusCode': 200,
                    'body': json.dumps(response),
                    'headers': {'Content-Type': 'application/json'}
                }
            
            if event.get('httpMethod') == 'POST':
                if event.get('path') == '/chat/completions':
                    rich_console.debug("Route matched: /chat/completions (POST)")
                    try:
                        job_input = json.loads(event.get('body', '{}'))
                        response = self.handle_chat_completions(job_input)
                        return {
                            'statusCode': 200,
                            'body': json.dumps(response),
                            'headers': {'Content-Type': 'application/json'}
                        }
                    except Exception as e:
                        rich_console.error(f"Error processing chat completion: {e}")
                        return {
                            'statusCode': 500,
                            'body': json.dumps({
                                "error": {
                                    "message": str(e),
                                    "type": "server_error"
                                }
                            }),
                            'headers': {'Content-Type': 'application/json'}
                        }

        except Exception as e:
            rich_console.error(f"Unhandled error: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    "error": {
                        "message": "Internal server error",
                        "type": "server_error"
                    }
                }),
                'headers': {'Content-Type': 'application/json'}
            }

        # Default route
        return {
            'statusCode': 404,
            'body': json.dumps({"error": "Not Found"}),
            'headers': {'Content-Type': 'application/json'}
        }

