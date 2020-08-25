import logging
from logging import Logger

log: Logger = logging.getLogger(name="TRACE")


def trace(isclass=False):
    def outer_wrapper(function):
        def class_wrapper(self, *args, **kwargs):
            print(f"{function.__name__} called\
                 with args={args} and kwargs={kwargs}")
            return function(*args, **kwargs)

        def function_wrapper(*args, **kwargs):
            print(f"{function.__name__} called\
                 with args={args} and kwargs={kwargs}")
            return function(*args, **kwargs)

        if isclass:
            return class_wrapper
        else:
            return function_wrapper
    return outer_wrapper
