import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='logs/application_errors.log'):
    """
    Configures the logger with specified log file and log level.
    """
    # Create logger
    logger = logging.getLogger()
    
    # Determine log level based on the environment
    log_level = logging.DEBUG if os.getenv('ENV') == 'dev' else logging.INFO
    logger.setLevel(log_level)

    # Create rotating file handler and set level to log_level
    rf_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3)
    rf_handler.setLevel(log_level)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    rf_handler.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(rf_handler)
    logger.addHandler(ch)
