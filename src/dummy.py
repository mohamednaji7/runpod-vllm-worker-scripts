import logging
from dummy_module import dummy_module_fn
import sys

# Configure logging to output plain text to stdout
logging.basicConfig(
    level=logging.DEBUG,       # Set the minimum logging level
    format="%(message)s",     # Text-only format
    stream=sys.stdout,        # Redirect all logs to stdout
)

logging.debug("1. hello RunPod! `dummy` script is here.")

# Set logging level to DEBUG to see all messages
logging.basicConfig(
    level=logging.DEBUG,
    )
logging.debug("2. hello RunPod! `dummy` script is here.")

def dummy():
    logging.debug("hello RunPod! `dummy` script is here.")

def main():
    try:
        dummy()
        dummy_module_fn()

    except Exception as e:
        logging.debug(f'ERROR in `dummy.py` {e}')
  
if __name__ == "__main__":
    main()
