from rich.console import Console

class Rich_Console:
    def __init__(self):
        # Instantiate Console with force_terminal=True to ensure color output
        self.console = Console(force_terminal=True)

        # Define styles for different log levels
        self.styles = {
            "info": "green",
            "warning": "blue",
            "error": "red",
            "debug": "yellow",
        }

    def info(self, msg):
        """Print an info message."""
        self.console.print(f"[INFO] {msg}", style=self.styles["info"])

    def warning(self, msg):
        """Print a warning message."""
        self.console.print(f"[WARNING] {msg}", style=self.styles["warning"])

    def error(self, msg):
        """Print an error message."""
        self.console.print(f"[ERROR] {msg}", style=self.styles["error"])

    def debug(self, msg):
        """Print a debug message."""
        self.console.print(f"[DEBUG] {msg}", style=self.styles["debug"])
