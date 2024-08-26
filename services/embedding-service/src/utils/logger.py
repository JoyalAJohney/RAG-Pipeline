import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('processing-service')

logger = setup_logger()