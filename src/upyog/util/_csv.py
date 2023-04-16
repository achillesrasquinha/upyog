import csv

from upyog.util._dict import dict_from_list
from upyog.util.types import lmap, auto_typecast
from upyog.util.string import strip

def read(path, *args, **kwargs):
    data  = []
    type_ = kwargs.pop("type", "dict")
    auto_cast = kwargs.pop("auto_cast", True)
    
    with open(path) as f:
        reader = csv.reader(f, *args, **kwargs)
        header = next(reader, None)

        autotype = auto_typecast if auto_cast else lambda x: x

        if type_ == "dict":
            data = lmap(lambda x: dict_from_list(header, lmap(autotype, x)), reader)
        else:
            data  = []
            data.append(header)
            data += lmap(lambda x: lmap(autotype, x), reader)

    return data

def write(path, row, mode = "w", *args, **kwargs):
    with open(path, mode = mode) as f:
        writer = csv.writer(f, *args, **kwargs)
        writer.writerow(row)