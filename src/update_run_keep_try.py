import os
import subprocess
import time

def update_run_keep_try(scriptname):
    # Try to run the first time regardless of KEEP_TRY or KEEP_RUN
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        print("Git pull successful.")
        
        # Run the specified script
        subprocess.run(['python3', scriptname], check=True)
        print(f"Script {scriptname} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Exiting after first failure.")

    # If KEEP_TRY is set to "True", continue retrying
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':
        if os.getenv('KEEP_TRY') == 'True':
            print("KEEP_TRY is set. Retrying...")
        elif os.getenv('KEEP_RUN') == 'True':
            print("KEEP_RUN is set. Continuing execution...")

        try:
            # Perform git pull to update
            subprocess.run(['git', 'pull'], check=True)
            print("Git pull successful.")
            
            # Run the specified script
            subprocess.run(['python3', scriptname], check=True)
            print(f"Script {scriptname} executed successfully.")
            
            # If KEEP_RUN is not set, break out of the loop
            if os.getenv('KEEP_RUN') != 'True':
                break  # Exit the loop if script runs successfully and KEEP_RUN is not set
            
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    
    else:
        if os.getenv('KEEP_TRY') != 'True' and os.getenv('KEEP_RUN') != 'True':
            print("Neither KEEP_TRY nor KEEP_RUN environment variables are set. Exiting.")
        else:
            print("Exiting after reaching exit condition for KEEP_RUN.")

scriptname  = 'main.py'
update_run_keep_try(scriptname)
