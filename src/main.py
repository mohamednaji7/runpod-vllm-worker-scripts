import os
import subprocess
import time

def update_run_keep_try(scriptname):
    # Try to run the first time regardless of KEEP_TRY
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        print("Git pull successful.")
        
        # Run the specified script
        subprocess.run(['python', scriptname], check=True)
        print(f"Script {scriptname} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Exiting after first failure.")

    # If KEEP_TRY is set to "True", continue retrying
    while os.getenv('KEEP_TRY') == 'True':
        print("KEEP_TRY is set. Retrying...")
        try:
            # Perform git pull to update
            subprocess.run(['git', 'pull'], check=True)
            print("Git pull successful.")
            
            # Run the specified script
            subprocess.run(['python', scriptname], check=True)
            print(f"Script {scriptname} executed successfully.")
            break  # Exit the loop if script runs successfully
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    else:
        print("KEEP_TRY environment variable not set to 'True'. Exiting.")

scriptname  = 'keep_alive.py'
update_run_keep_try(scriptname)
