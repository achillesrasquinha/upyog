import upyog as upy

LOG = upy.get_logger(__name__)

def retry(n):
    """
    Decorator to retry a function n times.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    LOG.warning("Error: %s occured. Retrying %s/%s", e, i + 1, n)
                    if i == n - 1:
                        raise e
        return wrapper
    return decorator