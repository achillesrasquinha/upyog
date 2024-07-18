import upyog as upy
from upyog.util.array import squash
from upyog.util.eject import ejectable

@ejectable()
def cmp(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

@ejectable()
def select(x, *keys):
    x = x.copy()
    y = {}

    for key in keys:
        y[key] = x[key]

    return y

@ejectable()
def noop(*args, **kwargs):
    pass

@ejectable()
async def anoop(*args, **kwargs):
    pass