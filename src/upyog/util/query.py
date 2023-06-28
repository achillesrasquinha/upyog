import upyog as upy
from collections.abc import Mapping
from upyog.util.op import Op

def where(data, clause):
    arraify = upy.is_list_like(data)
    data    = upy.sequencify(data)

    results = []

    for record in data:
        add = True

        for key, value in upy.iteritems(clause):
            if key in record:
                if isinstance(value, Mapping):
                    for op, val in upy.iteritems(value):
                        constraint = Op[op]

                        op1 = record[key]
                        op2 = val
                        
                        try:
                            if not constraint(op1, op2):
                                add = False
                                break
                        except TypeError:
                            add = False
                            break
                elif callable(value):
                    if not value(record[key]):
                        add = False
                        break
                else:
                    # TODO: callable for value?
                    if record[key] != value:
                        add = False
                        break

        if add:
            results.append(record)

    return results if arraify else upy.squash(results)
