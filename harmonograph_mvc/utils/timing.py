import time


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        return elapsed_time
    return wrapper


def timed_passthrough(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        returns = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        return returns, elapsed_time
    return wrapper
