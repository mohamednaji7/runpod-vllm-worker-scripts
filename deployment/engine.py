# engine.py
import logging
from unsloth import FastLanguageModel
import torch

class UnslothModel:
   def __init__(self):
       model_dir = "unsloth/tinyllama-bnb-4bit"
       cache_dir = './HF_HOME'
       max_seq_length = 2**9

       # Initialize model and tokenizer
       self.model, self.tokenizer = FastLanguageModel.from_pretrained(
           model_name=model_dir,
           max_seq_length=max_seq_length,
           dtype=torch.float16,
           load_in_4bit=True,
           cache_dir=cache_dir,
       )
       FastLanguageModel.for_inference(self.model)

   def generate_response(self, text, max_new_tokens=128):
       inputs = self.tokenizer([text], return_tensors="pt").to("cuda")
       outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
       return self.tokenizer.batch_decode(outputs)[0]

class UnslothEngine:
   def __init__(self):
       self.model = UnslothModel()
   
   def handle_request(self, messages):
       try:
           user_message = messages[-1]['content'] if messages else ""
           response = self.model.generate_response(user_message)
           
           return {
               "success": True,
               "choices": [{
                   "message": {
                       "role": "assistant",
                       "content": response
                   }
               }]
           }
       except Exception as e:
           return {
               "success": False,
               "error": str(e),
               "message": "Failed to generate response"
           }