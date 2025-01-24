    
import subprocess
from rich_console import Rich_Console

# Create an instance of Rich_Console
rich_console = Rich_Console()
rich_console.info("Starting the script.")


def run(scriptname):
    # Run the specified script
    rich_console.info(f"Running {scriptname}...")
    subprocess.run(['python3', scriptname], check=True)
    rich_console.info(f"Script {scriptname} executed successfully.")

def main():    
    scriptname = 'hello_handler.py'
    run(scriptname)

if __name__ == "__main__":
    main()
