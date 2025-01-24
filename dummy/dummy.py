from dummy_module import dummy_module_fn
import os

if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    # Configure logging to output plain text to stdout
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging

else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()


rich_console.info("This is an info message.")
rich_console.warning("This is a warning message.")
rich_console.error("This is an error message.")

def dummy():
    rich_console.debug("hello RunPod! `dummy` script is here.")

def main():
    try:
        dummy()
        dummy_module_fn()
    except Exception as e:
        rich_console.error(f"ERROR in `dummy.py`: {e}")

if __name__ == "__main__":
    main()
