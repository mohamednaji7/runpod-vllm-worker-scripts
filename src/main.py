    
import subprocess

def run(scriptname):
    # Run the specified script
    print(f"Running {scriptname}...")
    subprocess.run(['python3', scriptname], check=True)
    print(f"Script {scriptname} executed successfully.")

def main():    
    scriptname = 'keep_alive.py'
    run(scriptname)

if __name__ == "__main__":
    main()
