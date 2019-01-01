# -*- coding: utf-8 -*-

"""
Python logging module wrapper configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
    >>> import logger
    >>> logger.info('info message')
    2019-01-01 15:14:56,738 - <stdin> - INFO - info message

:copyright: (c) 2018 - 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import io
import logging
import logging.config
import os
import sys


logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(module)s - %(levelname)s - %(message)s',
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
            'filename': 'logger.log'
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


def _DummyFn(*args, **kwargs):
    """Placeholder function.

    Raises:
        NotImplementedError
    """
    _, _ = args, kwargs
    raise NotImplementedError()


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


#
# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame, by skipping frames whose filename is that of this
# module's source. It therefore should contain the filename of this module's
# source file.
#
# Ordinarily we would use __file__ for this, but frozen modules don't always
# have __file__ set, for some reason (see Issue #21736). Thus, we get the
# filename from a handy code object from a function defined in this module.
# (There's no particular reason for picking addLevelName.)
#

_srcfile = os.path.normcase(_DummyFn.__code__.co_filename)

# _srcfile is only used in conjunction with sys._getframe().
# To provide compatibility with older versions of Python, set _srcfile
# to None if _getframe() is not available; this value will prevent
# findCaller() from being called. You can also do this if you want to avoid
# the overhead of fetching caller information, even when _getframe() is
# available.
#if not hasattr(sys, '_getframe'):
#    _srcfile = None


class WrappedLogger(logging.Logger):
    """Report context of the caller of the function that issues a logging call.

    That is, if

        A() -> B() -> logging.info()

    Then references to "%(funcName)s", for example, will use A's context
    rather than B's context.

    Usage:
        logging.setLoggerClass(WrappedLogger)
        wrapped_logger = logging.getLogger("wrapped_logger")
    """
    def findCaller(self, stack_info=False, stacklevel=1):
        """Return the context of the caller's parent.

        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.

        This is based on the standard python 3.4 Logger.findCaller method.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


logging.setLoggerClass(WrappedLogger)
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
