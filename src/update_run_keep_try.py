import os
import subprocess
import time

def update():
    # Perform git pull to update
    subprocess.run(['git', 'pull'], check=True)
    print("Git pull successful.")
    
def run(scriptname):
    # Run the specified script
    print(f"Running {scriptname}...")
    subprocess.run(['python3', scriptname], check=True)
    print(f"Script {scriptname} executed successfully.")

def update_and_run(scriptname):
    update
    run(scriptname)


def try_update_and_run(scriptname):
    try:
        update_and_run(scriptname)
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Exiting after first failure.")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':   
        print(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        try_update_and_run(scriptname)

def main():
    scriptname  = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
