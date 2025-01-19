import logging
import os

# todo: add a global log level

def setup_logger(name, log_level=logging.NOTSET, log_file = None):
    """
    Sets up a logger with the specified name, level, and optional file handler.

    :param name: Name of the logger.
    :param log_level: Logging level (default: logging.INFO).
    :param log_file: Optional file export_path to write logs to (default: None).
    :return: Configured logger.
    """

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)

    #console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logging_config():
    pass