import asyncio
from upyog.util.types import build_fn

def asyncify(func, loop=None, executor=None):
    loop = loop or asyncio.get_event_loop()

    async def async_func(*args, **kwargs):
        fn = build_fn(func, *args, **kwargs)
        return await loop.run_in_executor(executor, fn)

    return async_func

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