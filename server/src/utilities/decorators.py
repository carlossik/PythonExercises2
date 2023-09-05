from functools import wraps
from time import sleep as count
from random import randrange


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        count(randrange(0, 40) / 100)

        return func(*args, **kwargs)
    return wrapper
