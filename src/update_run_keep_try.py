import os
import subprocess
import sys
from rich import print
from rich.console import Console

# Initialize the rich console for better visual output
console = Console()

# Import and install rich if necessary
try:
    import rich
except ImportError:
    console.print("[bold red]Rich library not found, installing...[/bold red]")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    import rich
    console.print("[bold green]Rich library installed successfully![/bold green]")

def update():
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        console.print("[bold green]Git pull successful.[/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Git pull failed: {e}[/bold red]")
        raise

def run(scriptname):
    try:
        # Run the specified script
        console.print(f"[bold yellow]Running {scriptname}...[/bold yellow]")
        subprocess.run(['python3', scriptname], check=True)
        console.print(f"[bold green]Script {scriptname} executed successfully.[/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error occurred while running {scriptname}: {e}[/bold red]")
        raise

def try_update_and_run(scriptname):
    try:
        update()
        run(scriptname)
    except Exception as e:
        console.print(f"[bold red]Error occurred: {e}[/bold red]")
        console.print("[bold red]Exiting after first failure.[/bold red]")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':   
        console.print(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        try_update_and_run(scriptname)

def main():
    scriptname = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
