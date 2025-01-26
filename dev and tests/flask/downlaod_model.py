# Updated imports and code for UnslothModel
from unsloth import FastLanguageModel

def download_model(model_path):
    model, _ = FastLanguageModel.from_pretrained(
        model_name=model_path,
        cache_dir='./HF_HOME',
        load_in_4bit=True,
    )
    return model

# Example usage
if __name__ == "__main__":
    model = download_model('unsloth/tinyllama-bnb-4bit')