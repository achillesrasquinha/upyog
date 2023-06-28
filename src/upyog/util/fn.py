import upyog as upy

def pop(x, *keys):
    x = x.copy()

    values = []

    for key in keys:
        values.append(x[key])
        del x[key]

    return x, upy.squash(values)