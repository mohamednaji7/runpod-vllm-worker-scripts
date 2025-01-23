import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

# Set up rich console
console = Console()

def install_requirements(requirements_file="requirements.txt", verbose=False):
    """
    Installs the Python packages listed in the given requirements file.
    
    Args:
        requirements_file (str): Path to the requirements.txt file. Default is 'requirements.txt'.
        verbose (bool): If True, enables verbose output during installation.
    """
    req_file_path = Path(requirements_file)

    # Check if the requirements file exists
    if not req_file_path.is_file():
        console.print(f"[bold red]Error:[/bold red] {requirements_file} does not exist.")
        return

    console.print(f"[bold blue]Starting installation from[/bold blue] [yellow]{requirements_file}[/yellow]...")

    try:
        # Read the contents of the requirements.txt file
        with open(requirements_file, "r") as file:
            packages = file.readlines()

        # Remove any empty lines or comments
        packages = [pkg.strip() for pkg in packages if pkg.strip() and not pkg.startswith("#")]

        # Display a progress bar during installation
        with Progress(console=console) as progress:
            task = progress.add_task("[green]Installing dependencies...", total=len(packages))

            # Prepare the pip install command
            command = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
            if verbose:
                command.append("--verbose")

            # Run the installation command
            for package in packages:
                console.print(f"[yellow]Installing package:[/yellow] {package}")
                result = subprocess.run([sys.executable, "-m", "pip", "install", package], text=True, capture_output=not verbose)
                
                # Update progress and handle results for each package
                progress.update(task, advance=1)
                
                if result.returncode == 0:
                    console.print(f"[bold green]Successfully installed:[/bold green] {package}")
                else:
                    console.print(f"[bold red]Error installing:[/bold red] {package}\n{result.stderr if not verbose else ''}")

            console.print("[bold green]All packages installed successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
