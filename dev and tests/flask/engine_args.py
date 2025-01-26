# Updated engine arguments for UnslothModel

MODEL_ARGS = {
    'model_path': 'unsloth/tinyllama-bnb-4bit',
    'cache_dir': './HF_HOME',
    'max_seq_length': 2048,
    'load_in_4bit': True,
}