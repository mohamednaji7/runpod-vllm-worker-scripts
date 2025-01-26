# utils.py - Utility functions

from unsloth import FastLanguageModel

def preprocess_input(input_text):
    # Example preprocessing for UnslothModel
    return input_text.lower()

def postprocess_output(output_text):
    # Example postprocessing for UnslothModel
    return output_text.strip()

def load_model(model_path):
    # Updated model loading for UnslothModel
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_path,
        cache_dir='./HF_HOME',
        load_in_4bit=True,
    )
    return model, tokenizer