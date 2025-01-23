import os
import sys
from rich.console import Console
from dummy_module import dummy_module_fn

# Check if the terminal is capable of color
print(f"Terminal capable of color: {sys.stdout.isatty()}")

# Force terminal environment variable for subprocess compatibility
os.environ['TERM'] = 'xterm-256color'

# Instantiate Console with force_terminal=True to ensure color output
console = Console(force_terminal=True)

# Print styled text
console.print("[bold magenta]Hello, world![/bold magenta] [green]Welcome to Rich Console![/green]")

# Example colorized console output
console.print("[blue]INFO:[/blue] [green]This is an info message with Rich formatting[/green]")
console.print("[yellow]DEBUG:[/yellow] [bright_yellow]Debug information looks more colorful[/bright_yellow]")
console.print("[orange]WARNING:[/orange] [yellow]Warnings stand out[/yellow]")
console.print("[red]ERROR:[/red] [bold red]Error messages are highlighted[/bold red]")

def dummy():
    console.print("[cyan]DEBUG:[/cyan] hello RunPod! `dummy` script is here.", style="cyan")

def main():
    try:
        dummy()
        dummy_module_fn()

    except Exception as e:
        console.print(f"[bold red]ERROR in `dummy.py`[/bold red]: {e}", style="bold red")

if __name__ == "__main__":
    main()
