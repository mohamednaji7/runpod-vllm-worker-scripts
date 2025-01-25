import json
import os

if os.environ.get('SCRIPT_NAME') is not None:
    import logging
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

    def handle_chat_completions(self, job_input):
        """Handle chat completions in OpenAI-compatible format."""
        return self.engine.process_job_input(job_input)

    def handler(self, event):
        """Main handler for OpenAI-compatible routes."""
        rich_console.info(f"Received event: {event}")
        
        # Route handling
        if event.get('httpMethod') == 'GET' and event.get('path') == '/models':
            return {
                'statusCode': 200,
                'body': json.dumps(self.handle_list_models()),
                'headers': {'Content-Type': 'application/json'}
            }
        
        if event.get('httpMethod') == 'POST':
            if event.get('path') == '/chat/completions':
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
        
        # Default route
        return {
            'statusCode': 404,
            'body': json.dumps({"error": "Not Found"}),
            'headers': {'Content-Type': 'application/json'}
        }