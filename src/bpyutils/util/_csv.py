import csv

from bpyutils.util._dict import dict_from_list
from bpyutils.util.types import lmap, auto_typecast

def read(path):
    data = []
    
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader, None)

        data = lmap(lambda x: dict_from_list(header, lmap(auto_typecast, x)), reader)

    return data