import cProfile, pstats, asyncio
from upyog._compat import StringIO
from upyog.util.system import write

def aprofile(output = None, sort = 'cumulative'):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            prof.enable()

            result = await func(*args, **kwargs)

            prof.disable()

            s = StringIO()
            
            stats = pstats.Stats(prof, stream = s).sort_stats(sort)
            stats.print_stats()

            if output:
                write(output, s.getvalue(), force = True)

            return result
        return wrapper
    return decorator