# -*- coding: utf-8 -*-

import logging
import logging.config


logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmr': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'stream': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'app.log'
        },
    },
    'loggers': {
        'logger': {
            'handlers': ['stream', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


logging.config.dictConfig(logging_config)
logger = logging.getLogger('logger')


def critical(msg, *args, **kwargs):
    """Log a message with severity 'CRITICAL' on the root logger."""
    logger.critical(msg, *args, **kwargs)


fatal = critical


def error(msg, *args, **kwargs):
    """Log a message with severity 'ERROR' on the root logger. """
    logger.error(msg, *args, **kwargs)


def exception(msg, *args, exc_info=True, **kwargs):
    """Log a message with severity 'ERROR' on the root logger, with exception
    information.
    """
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg, *args, **kwargs):
    """Log a message with severity 'WARNING' on the root logger."""
    logger.warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """Log a message with severity 'INFO' on the root logger."""
    logger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """Log a message with severity 'DEBUG' on the root logger."""
    logger.debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """Log 'msg % args' with the integer severity 'level' on the root logger."""
    logger.log(level, msg, *args, **kwargs)


def disable(level=logging.CRITICAL):
    """Disable all logging calls of severity 'level' and below."""
    logger.manager.disable = level
    logger.manager._clear_cache()
