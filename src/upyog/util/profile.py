import asyncio
from upyog._compat import StringIO
from upyog.util.system import write
from upyog.util.eject import ejectable

@ejectable()
def aprofile(output = None, sort = 'cumulative'):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            import cProfile, pstats

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