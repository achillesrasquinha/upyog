from upyog.util.types import build_fn
import upyog as upy
from upyog.util.eject import ejectable
from upyog.util.eject import ejectable

@ejectable()
def asyncify(func, loop=None, executor=None):
    import asyncio

    loop = loop or asyncio.get_event_loop()

    async def async_func(*args, **kwargs):
        fn = build_fn(func, *args, **kwargs)
        return await loop.run_in_executor(executor, fn)

    return async_func

@ejectable()
async def aenumerate(aiterable, start=0):
    i = start
    async for x in aiterable:
        yield i, x
        i += 1

async def acombine(*aiterables):
    """
        Merge multiple async iterables into one.
    """
    aiterators = [aiterable.__aiter__() for aiterable in aiterables]
    while aiterators:
        for i, aiterator in enumerate(aiterators):
            try:
                yield await aiterator.__anext__()
            except StopAsyncIteration:
                del aiterators[i]
                break

@ejectable()
async def aiterable(iterable):
    for x in iterable:
        yield x