# Rotating logger

import logging
import os
import platform
import datetime
from logging.handlers import RotatingFileHandler

pid = str(os.getpid())
date = datetime.datetime.now().strftime("%Y-%m-%d")


def log_handler(program_name, log_level, enable_console, log_file_path, log_file_max_bytes, backup_count):
    log_file_name = program_name + '.log'
    os_system = platform.system()

    # Check if OS = Windows and set log file path / file name
    if os_system == 'Windows':
        log_file_name = log_file_path + log_file_name
    else:
        print('Unknown OS: ' + os_system)
        exit(30)

    # Logging ---START---

    # create the logging instance for logging to file only
    logger = logging.getLogger('Smartfile')

    # create rotating handler
    file_logger = RotatingFileHandler(log_file_name, maxBytes=log_file_max_bytes, backupCount=backup_count)
    new_format = '[%(asctime)s] - ' + pid + ' - [%(levelname)s] - %(message)s'
    file_logger_format = logging.Formatter(new_format)

    # tell the handler to use the above format
    file_logger.setFormatter(file_logger_format)

    # finally, add the handler to the base logger
    logger.addHandler(file_logger)

    # Console messages
    if enable_console == 'YES':
        console = logging.StreamHandler()
        logging.getLogger('Smartfile').addHandler(console)
        # Set log level
        if log_level == 'INFO':
            logger.setLevel(logging.INFO)
            console.setLevel(logging.INFO)
        if log_level == 'DEBUG':
            logger.setLevel(logging.DEBUG)
            console.setLevel(logging.DEBUG)
        if log_level == 'ERROR':
            logger.setLevel(logging.ERROR)
            console.setLevel(logging.ERROR)

    elif enable_console == 'NO':
        if log_level == 'INFO':
            logger.setLevel(logging.INFO)
        if log_level == 'DEBUG':
            logger.setLevel(logging.DEBUG)
        if log_level == 'ERROR':
            logger.setLevel(logging.ERROR)
    else:
        print('Error while initialising logger. Unknown option for "enableConsole" in property file')

    info_log = logger.info
    debug_log = logger.debug
    error_log = logger.error
    warning_log = logger.warning
    critical_log = logger.critical

    return info_log, error_log, debug_log, warning_log, critical_log, log_file_name

    # Logging ---END---

