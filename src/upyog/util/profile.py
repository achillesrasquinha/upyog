import asyncio, os.path as osp
from upyog._compat import StringIO
from upyog.util.system import write
from upyog.util.eject import ejectable
from upyog.util.datetime import get_timestamp_str

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

            output_file = None

            if output_dir:
                output_file = osp.join(output_dir, "profile",
                    "%s.prof" % get_timestamp_str("%Y%m%d%H%M%S")
                )
            elif output:
                output_file = output

            if output_file:
                write(output, s.getvalue(), force = True)

            return result
        return wrapper
    return decorator