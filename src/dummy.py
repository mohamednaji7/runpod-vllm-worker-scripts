import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def dummy():
    logging.info("hello RunPod! `dummy` script is here.")

def main():
    try:
        dummy()
    except Exception as e:
        logging.error(f'ERROR in `dummy.py` {e}')
  
if __name__ == "__main__":
    main()
