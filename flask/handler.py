
from flask import Flask, request, jsonify
from unsloth import FastLanguageModel
import torch

app = Flask(__name__)

class UnslothModel:
    def __init__(self):
        """Initialize the Unsloth language model with comprehensive logging."""
        model_dir = "unsloth/tinyllama-bnb-4bit"
        self.model_id = model_dir
        cache_dir = './HF_HOME'

        dtype = None  # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
        load_in_4bit = True  # Use 4bit quantization to reduce memory usage. Can be False.
        max_seq_length = 2048  # Choose any! We auto support RoPE Scaling internally!

        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_dir,
            max_seq_length=max_seq_length,
            dtype=dtype,
            load_in_4bit=load_in_4bit,
            cache_dir=cache_dir,
        )

        FastLanguageModel.for_inference(self.model)

    def generate_response(self, prompt, max_new_tokens=128):
        """Generate a response with comprehensive logging."""
        inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
        response = self.tokenizer.batch_decode(outputs)[0]
        return response

model = UnslothModel()

@app.route('/v1/completions', methods=['POST'])
def completions():
    data = request.json
    prompt = data['prompt']
    max_new_tokens = data.get('max_tokens', 128)
    response = model.generate_response(prompt, max_new_tokens)
    return jsonify({
        'id': 'cmpl-123456',
        'object': 'text_completion',
        'created': int(time.time()),
        'model': model.model_id,
        'choices': [{'text': response, 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}],
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)