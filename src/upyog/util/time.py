import upyog as upy
from upyog.util.eject import ejectable

LOG = upy.get_logger(__name__)

@ejectable()
def atimeit():
    def decorator(fn):
        async def wrapper(*args, **kwargs):
            start  = upy.now()
            result = await fn(*args, **kwargs)
            end    = upy.now()

            name   = fn.__name__

            mdiff  = round((end - start).total_seconds() / 60, 2)

            LOG.info(f"Time Taken ({name}): {mdiff} minutes.")

            return result
        return wrapper
    return decorator

@ejectable()
def timeit():
    def decorator(fn):
        def wrapper(*args, **kwargs):
            start  = upy.now()
            result = fn(*args, **kwargs)
            end    = upy.now()

            name   = fn.__name__

            mdiff  = round((end - start).total_seconds() / 60, 2)

            LOG.info(f"Time Taken ({name}): {mdiff} minutes.")

            return result
        return wrapper
    return decorator