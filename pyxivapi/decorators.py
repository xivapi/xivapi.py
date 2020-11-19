import logging
from functools import wraps
from time import time

__log__ = logging.getLogger(__name__)


def timed(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        __log__.info("%s executed in %ds", func.__name__, round(time() - start, 2))
        return result
    return wrapper
