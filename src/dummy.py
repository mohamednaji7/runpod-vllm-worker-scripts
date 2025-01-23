import logging
from dummy_module import dummy_module_fn

# Set logging level to DEBUG to see all messages
logging.basicConfig(level=logging.DEBUG)


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
