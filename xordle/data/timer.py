import time


timer_stats = dict()


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        if func.__name__ not in timer_stats:
            timer_stats[func.__name__] = 0
        timer_stats[func.__name__] += (end_time - start_time)

        return result
    return wrapper


def get_timer():
    return timer_stats
