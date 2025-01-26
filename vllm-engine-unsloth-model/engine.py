import os
import logging
import json
import asyncio

from dotenv import load_dotenv
from typing import AsyncGenerator
import time

from unsloth import FastLanguageModel
from unsloth import rich_console

from utils import DummyRequest, JobInput, BatchSize, create_error_response
from constants import DEFAULT_MAX_CONCURRENCY, DEFAULT_BATCH_SIZE, DEFAULT_BATCH_SIZE_GROWTH_FACTOR, DEFAULT_MIN_BATCH_SIZE

class UnslothModel:
    def __init__(self):
        """Initialize the Unsloth language model with comprehensive logging."""
        self.processed_prompt_tokens = -1
        self.processed_completion_tokens = -1
        try:
            rich_console.info("Initializing UnslothModel")
            
            # Model configuration
            model_dir = "unsloth/tinyllama-bnb-4bit"
            self.model_id = model_dir
            cache_dir = './HF_HOME'

            # Model initialization with detailed logging
            rich_console.info(f"Loading model from {model_dir}")
            dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
            load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
            max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!

            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_dir,
                max_seq_length=max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                cache_dir=cache_dir,
            )
            
            # Prepare model for inference
            FastLanguageModel.for_inference(self.model)
            rich_console.info("Model initialized successfully")

        except Exception as e:
            rich_console.error(f"Model initialization failed: {e}", exc_info=True)
            raise

    def generate_response(self, prompt, max_new_tokens=128):
        """Generate a response with comprehensive logging."""
        try:
            rich_console.info(f"Generating response. Prompt length: {len(prompt)}")
            rich_console.debug(f"Prompt preview: {prompt[:100]}...")

            # Prepare input
            inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
            
            # Generate response
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
            response = self.tokenizer.batch_decode(outputs)[0]

            rich_console.info(f"Response generated. Length: {len(response)}")
            rich_console.debug(f"Response preview: {response[:100]}...")

            # Calculate token usage
            self.processed_prompt_tokens  = len(prompt.split())
            self.processed_completion_tokens = len(response.split())
            return response

        except Exception as e:
            rich_console.error(f"Response generation failed: {e}", exc_info=True)
            raise

class vLLMEngine:
    def __init__(self, engine=None):
        load_dotenv()  # For local development
        self.engine_args = get_engine_args()
        logging.info(f"Engine args: {self.engine_args}")
        self.llm = self._initialize_llm() if engine is None else engine.llm
        self.max_concurrency = int(os.getenv("MAX_CONCURRENCY", DEFAULT_MAX_CONCURRENCY))
        self.default_batch_size = int(os.getenv("DEFAULT_BATCH_SIZE", DEFAULT_BATCH_SIZE))
        self.batch_size_growth_factor = int(os.getenv("BATCH_SIZE_GROWTH_FACTOR", DEFAULT_BATCH_SIZE_GROWTH_FACTOR))
        self.min_batch_size = int(os.getenv("MIN_BATCH_SIZE", DEFAULT_MIN_BATCH_SIZE))

    def dynamic_batch_size(self, current_batch_size, batch_size_growth_factor):
        return min(current_batch_size * batch_size_growth_factor, self.default_batch_size)

    async def generate(self, job_input: JobInput):
        try:
            async for batch in self._generate_unsloth(
                llm_input=job_input.llm_input,
                validated_sampling_params=job_input.sampling_params,
                batch_size=job_input.max_batch_size,
                stream=job_input.stream,
                apply_chat_template=job_input.apply_chat_template,
                request_id=job_input.request_id,
                batch_size_growth_factor=job_input.batch_size_growth_factor,
                min_batch_size=job_input.min_batch_size
            ):
                yield batch
        except Exception as e:
            yield {"error": create_error_response(str(e)).model_dump()}

    async def _generate_unsloth(self, llm_input, validated_sampling_params, batch_size, stream, apply_chat_template, request_id, batch_size_growth_factor, min_batch_size: str) -> AsyncGenerator[dict, None]:
        if apply_chat_template or isinstance(llm_input, list):
            llm_input = self.tokenizer.apply_chat_template(llm_input)
        results_generator = self.llm.generate(llm_input, validated_sampling_params, request_id)
        n_responses, n_input_tokens, is_first_output = validated_sampling_params.n, 0, True
        last_output_texts, token_counters = ["" for _ in range(n_responses)], {"batch": 0, "total": 0}

        batch = {
            "choices": [{"tokens": []} for _ in range(n_responses)],
        }

        max_batch_size = batch_size or self.default_batch_size
        batch_size_growth_factor, min_batch_size = batch_size_growth_factor or self.batch_size_growth_factor, min_batch_size or self.min_batch_size
        batch_size = BatchSize(max_batch_size, min_batch_size, batch_size_growth_factor)

        async for request_output in results_generator:
            if is_first_output:  # Count input tokens only once
                n_input_tokens = len(request_output.prompt_token_ids)
                is_first_output = False

            for output in request_output.outputs:
                output_index = output.index
                token_counters["total"] += 1
                if stream:
                    new_output = output.text[len(last_output_texts[output_index]):]
                    batch["choices"][output_index]["tokens"].append(new_output)
                    token_counters["batch"] += 1

                    if token_counters["batch"] >= batch_size.current_batch_size:
                        batch["usage"] = {
                            "input": n_input_tokens,
                            "output": token_counters["total"],
                        }
                        yield batch
                        batch = {
                            "choices": [{"tokens": []} for _ in range(n_responses)],
                        }
                        token_counters["batch"] = 0
                        batch_size.update()

                last_output_texts[output_index] = output.text

        if not stream:
            for output_index, output in enumerate(last_output_texts):
                batch["choices"][output_index]["tokens"] = [output]
            token_counters["batch"] += 1

        if token_counters["batch"] > 0:
            batch["usage"] = {"input": n_input_tokens, "output": token_counters["total"]}
            yield batch

    def _initialize_llm(self):
        try:
            start = time.time()
            engine = UnslothModel()
            end = time.time()
            logging.info(f"Initialized Unsloth model in {end - start:.2f}s")
            return engine
        except Exception as e:
            logging.error("Error initializing Unsloth model: %s", e)
            raise e