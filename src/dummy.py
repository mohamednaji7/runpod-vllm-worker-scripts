import logging
import sys

# Configure logging to output plain text to stdout
logging.basicConfig(
    # level=logging.INFO,       # Set the minimum logging level
    # format="%(message)s",     # Text-only format
    stream=sys.stdout,        # Redirect all logs to stdout
)

def dummy():
    logging.info("hello RunPod! `dummy` script is here.")

def main():
    try:
        dummy()
    except Exception as e:
        logging.error(f'ERROR in `dummy.py` {e}')
  
if __name__ == "__main__":
    main()
