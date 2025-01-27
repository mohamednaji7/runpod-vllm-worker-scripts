# model_api.py
import os
import time
from rich.console import Console

# Initialize rich console for logging
rich_console = Console()


class OpenaiResponse:
    """Handles generation of OpenAI-style success and error responses."""

    def generate_success_response(self, model_id, response, input_tokens, output_tokens):
        """
        Generate a success response in OpenAI-style format.

        Args:
            model_id (str): The model's identifier.
            response (str): The generated response content.
            input_tokens (int): Number of tokens in the input text.
            output_tokens (int): Number of tokens in the generated output.

        Returns:
            dict: A structured success response.
        """
        return {
            "id": f"chatcmpl-{os.urandom(16).hex()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model_id,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.strip()
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            }
        }

    def generate_error_response(self, message, error_type="invalid_request_error", param=None, code="500"):
        """
        Generate an error response in OpenAI-style format.

        Args:
            message (str): Error message to include in the response.
            error_type (str): Type of the error (default: "invalid_request_error").
            param (str, optional): Additional parameter info (default: None).
            code (str): Error code (default: "500").

        Returns:
            dict: A structured error response.
        """
        return {
            "object": "error",
            "error": {
                "message": message,
                "type": error_type,
                "param": param,
                "code": code
            }
        }


class OpenaiEngine(OpenaiResponse):
    def __init__(self, model_api):
        """Initialize the API engine with the model."""
        rich_console.info("Initializing OpenAI API Engine")
        self.model_api = model_api

    def format_messages_to_prompt(self, messages):
        """
        Convert OpenAI-style messages to a single prompt string.
        
        Args:
            messages (list): List of dictionaries with 'role' and 'content'.

        Returns:
            str: A formatted prompt string.
        """
        try:
            rich_console.info(f"Formatting {len(messages)} messages into a prompt")
            if not isinstance(messages, list) or not all(isinstance(msg, dict) for msg in messages):
                raise ValueError("Messages must be a list of dictionaries with 'role' and 'content' keys.")
            
            prompt = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                if role == 'system':
                    prompt += f"System: {content}\n"
                elif role == 'user':
                    prompt += f"Human: {content}\n"
                elif role == 'assistant':
                    prompt += f"Assistant: {content}\n"
                else:
                    raise ValueError(f"Unsupported role: {role}")
            prompt += "Assistant:"
            rich_console.debug(f"Formatted prompt: {prompt}")
            return prompt
        except Exception as e:
            rich_console.error(f"Error formatting messages: {e}", exc_info=True)
            raise

    def process_request(self, messages):
        """
        Process a request and return a response in OpenAI-compatible format.

        Args:
            messages (list or str): Messages to process.

        Returns:
            dict: OpenAI-compatible response (success or error).
        """
        try:
            rich_console.info("Processing request")
            # Convert messages to prompt
            formatted_prompt = self.format_messages_to_prompt(messages)
            # Generate response from the model
            response = self.model_api.generate_response(formatted_prompt)
            # Get token usage
            prompt_tokens = self.model_api.processed_prompt_tokens
            completion_tokens = self.model_api.processed_completion_tokens
            # Return success response
            return self.generate_success_response(
                model_id=self.model_api.model_id,
                response=response,
                input_tokens=prompt_tokens,
                output_tokens=completion_tokens
            )
        except Exception as e:
            rich_console.error(f"Request processing failed: {e}", exc_info=True)
            # Return error response
            return self.generate_error_response(str(e), error_type="server_error", code="500")


class SimpleOpenaiEngine(OpenaiEngine):
    def format_messages_to_prompt(self, messages):
        """
        Convert messages to a single prompt string.
        
        Args:
            messages (list): List of one dictionary with 'role' and 'content'.

        Returns:
            str: A formatted prompt string.
        """
        try:
            rich_console.info(f"Formatting {len(messages)} messages into a prompt")
            if not isinstance(messages, list) or not all(isinstance(msg, dict) for msg in messages):
                rich_console.debug(messages)
                raise ValueError("Messages must be a list of dictionaries with 'role' and 'content' keys.")
            assert len(messages)==1
            prompt = messages[0]['content']
            rich_console.debug(f"Formatted prompt: {prompt[:20]}")
            return prompt
        except Exception as e:
            rich_console.error(f"Error formatting messages: {e}", exc_info=True)
            raise
