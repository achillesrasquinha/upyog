import upyog as upy
import time

LOG = upy.get_logger(__name__)

def retry(n, every = 1):
    """
    Decorator to retry a function n times.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(every)
                    LOG.warning("Error: %s occured. Retrying %s/%s", e, i + 1, n)
                    if i == n - 1:
                        raise e
        return wrapper
    return decorator