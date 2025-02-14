import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger("FlaskMVCProject")  # create logger instance

    if logger.hasHandlers():  # check if any handlers exists
        logger.handlers.clear()  # if exists clear it
    logger.setLevel(logging.DEBUG)  # logs from debug level

    file_handler = RotatingFileHandler("app.log")  # store logs in app.log

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(name)s -  %(funcName)s - %(levelname)s - %(message)s\n")

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Prevent duplicate logs  in case other module import this logger
    logger.propagate = False

    return logger
