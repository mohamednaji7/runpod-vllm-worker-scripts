    
import subprocess
from install import  install_requirements 


def run(scriptname):
    # Run the specified script
    print(f"Running {scriptname}...")
    subprocess.run(['python3', scriptname], check=True)
    print(f"Script {scriptname} executed successfully.")

def main():    
    scriptname = 'keep_alive.py'
    install_requirements("requirements.txt", verbose=True)
    run(scriptname)

if __name__ == "__main__":
    main()
