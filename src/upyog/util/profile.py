import asyncio, os.path as osp
from upyog._compat import StringIO
from upyog.util.system import write
from upyog.util.eject import ejectable
from upyog.util.datetime import get_timestamp_str
from upyog.config import PATH

@ejectable()
def aprofile(output = None, output_dir = None, sort = 'cumulative'):
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

            output_file = osp.join(
                output_dir if output_dir else PATH["CACHE"], 
                "profile", 
                get_timestamp_str() + ".prof"
            )

            write(output_file, s.getvalue(), force = True)

            return result
        return wrapper
    return decorator