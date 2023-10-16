import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='logs/application_errors.log'):
    """
    Configures the logger with specified log file and log level.
    """
    # Create logger
    logger = logging.getLogger()
    
    # Determine log level and environment
    env = os.getenv('ENV', 'local')
    log_level = logging.DEBUG if env == 'dev' else logging.INFO
    
    logger.setLevel(log_level)

    # Create rotating file handler and set level to log_level
    rf_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3)
    rf_handler.setLevel(log_level)

    # Create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)  # Directing to stdout
    ch.setLevel(logging.ERROR)

    # Adjust handlers based on the environment
    if env == 'local':
        ch.setLevel(logging.CRITICAL)  # Only critical errors will be printed to console in local
    elif env in ['dev', 'prod']:
        ch.setLevel(logging.INFO)  # In dev and prod, informational messages and above will go to stdout

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    rf_handler.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(rf_handler)
    logger.addHandler(ch)
