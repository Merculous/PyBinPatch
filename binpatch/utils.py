
from time import perf_counter


def timer(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func_ret = func(*args, **kwargs)
        end = perf_counter() - start
        print(f'{func.__name__} took {end:.6f} seconds.')
        return func_ret
    return wrapper
