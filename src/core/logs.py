""" Logs
This module configures the application's logging behavior.

configure_logging():
    Sets up the logging configuration based on the provided 
    log level. Defaults to ERROR if the input is invalid.
"""
import logging
from enum import StrEnum

# Defines a detailed log format used for debugging
LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

# An enumeration of valid log levels
class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging(log_level: str = LogLevels.error):
    
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)