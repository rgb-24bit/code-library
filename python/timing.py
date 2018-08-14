# -*- coding: utf-8 -*-

"""
Utilities for timing code execution.
"""

import time


# If possible (Unix), use the resource module instead of time.clock()
try:
    import resource

    def clocku():
        """clocku() -> floating point number

        Return the USER CPU time in seconds since the start of the process.
        """
        return resource.getrusage(resource.RUSAGE_SELF)[0]

    def clocks():
        """clocks() -> floating point number

        Return the SYSTEM CPU time in seconds since the start of the process.
        """
        return resource.getrusage(resource.RUSAGE_SELF)[1]

    def clock():
        """clock() -> floating point number

        Return the TOTAL USER + SYSTEM CPU time in seconds since the start of
        the process.
        """
        return sum(resource.getrusage(resource.RUSAGE_SELF)[:2])

    def clock2():
        """clock2() -> (t_user, t_system)

        Similar to clock(), but return a tuple of user/system times.
        """
        return resource.getrusage(resource.RUSAGE_SELF)[:2]

except ImportError:
    # There is no distinction of user/system time under windows, so we just use
    # time.clock() for everything...
    clocku = clocks = clock = time.clock

    def clock2():
        """colock2() -> (time.clock(), 0.0)

        Return the time.clock() and zero.
        """
        return time.clock(), 0.0


def timings_out(reps, func, *args, **kw):
    """timings_out(reps, func, *args, **kw) -> (t_total, t_per_call, result)

    Args:
        reps: Function execution times.
        func: The function to be executed.
        *args, **kw: Function parameter.

    Return:
        Total execution time, average execution time,
        return value of the last execution of the function.
    """
    reps = int(reps)
    assert reps >= 1, 'reps must be >= 1'
    if reps == 1:
        start = clock()
        res = func(*args, **kw)
        tot_time = clock() - start
    else:
        rng = range(reps - 1)  # the last time is executed separately to store output
        start = clock()
        for dummy in rng: func(*args, **kw)
        res = func(*args, **kw)  # one last time
        tot_time = clock() - start
    av_time = tot_time / reps
    return tot_time, av_time, res


def timings(reps, func, *args, **kw):
    """timings(reps, func, *args, **kw) -> (t_total, t_per_call)

    Args:
        reps: Function execution times.
        func: The function to be executed.
        *args, **kw: Function parameter.

    Return:
        Total execution time, average execution time.
    """
    return timings_out(reps, func, *args, **kw)[0:2]


def timing(func, *args, **kw):
    """timing(func, *args, **kw) -> t_total

    Args:
        func: The function to be executed.
        *args, **kw: Function parameter.

    Return:
        Total execution time.
    """
    return timings_out(1, func, *args, **kw)[0]
