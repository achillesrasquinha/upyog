import csv

from upyog.util._dict import dict_from_list, lkeys, lvalues
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

def write(path, rows, mode = "w", *args, **kwargs):
    if len(rows) != 0:
        if isinstance(rows[0], dict):
            header = lkeys(rows[0])
            rows   = lmap(lvalues, rows)
            rows.insert(0, header)

    with open(path, mode = mode) as f:
        writer = csv.writer(f, *args, **kwargs)
        for row in rows:
            writer.writerow(row)

def rows_to_dicts(rows, header = None, auto_cast = True):
    if header is None:
        header = rows[0]
        rows   = rows[1:]

    autotype = auto_typecast if auto_cast else lambda x: x
    return lmap(lambda x: dict_from_list(header, lmap(autotype, x)), rows)