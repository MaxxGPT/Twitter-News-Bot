import logging

def setup_logger(log_file='application_errors.log', log_level=logging.INFO):
    """
    Configures the logger with specified log file and log level.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create file handler and set level to log_level
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
