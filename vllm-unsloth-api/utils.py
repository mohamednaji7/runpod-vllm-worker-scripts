# src/utils.py

class JobInput:
    def __init__(self, job):
        self.llm_input = job.get("messages", job.get("prompt"))
        self.stream = job.get("stream", False)
        self.max_batch_size = job.get("max_batch_size")
        self.apply_chat_template = job.get("apply_chat_template", False)
        self.use_openai_format = job.get("use_openai_format", False)
        self.sampling_params = SamplingParams(**job.get("sampling_params", {}))
        self.request_id = random_uuid()
        self.batch_size_growth_factor = float(job.get("batch_size_growth_factor", 1))
        self.min_batch_size = int(job.get("min_batch_size", 1))
        self.openai_route = job.get("openai_route")
        self.openai_input = job.get("openai_input")
        self.model_id = job.get("model_id")  # Add this line to get the model identifier