# Updated imports and code for UnslothModel
from unsloth import FastLanguageModel

def get_tokenizer(model_path):
    _, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_path,
        cache_dir='./HF_HOME',
    )
    return tokenizer

# Example usage
if __name__ == "__main__":
    tokenizer = get_tokenizer('unsloth/tinyllama-bnb-4bit')