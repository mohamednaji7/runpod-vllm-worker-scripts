import runpod
import subprocess
import os
# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.


def update():
    # Perform git pull to update
    subprocess.run(['git', 'pull'], check=True)
    print("Git pull successful.")
    
def handler(job):
    """ Handler function that will be used to process jobs. """
    if os.getenv('PULL_BEFORE_REQUEST')=='True':
        update()
    job_input = job['input']

    name = job_input.get('name', 'World')

    return f"Hello, {name}!"


runpod.serverless.start({"handler": handler})