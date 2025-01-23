import logging
from dummy_module import dummy_module_fn

def dummy():
    logging.debug("hello RunPod! `dummy` script is here.")

def main():
    try:
        dummy()
    except Exception as e:
        logging.debug(f'ERROR in `dummy.py` {e}')
  
if __name__ == "__main__":
    main()
