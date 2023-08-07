import upyog as upy

@upy.ejectable()
def where(data, clause, other = False):
    import upyog as upy

    arraify = upy.is_list_like(data)
    data    = upy.sequencify(data)

    results = []
    others  = []

    for record in data:
        add = True

        if callable(clause):
            if not clause(record):
                add = False
                break
        elif isinstance(clause, upy._compat.Mapping):
            for key, value in upy.iteritems(clause):
                if key in record:
                    if isinstance(value, upy.Mapping):
                        for op, val in upy.iteritems(value):
                            constraint = upy.Op[op]

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
        else:
            raise TypeError(f"Invalid clause type: {type(clause)}")

        if add:
            results.append(record)
        else:
            others.append(record)

    if other:
        if arraify:
            return results, others
        else:
            return upy.squash(results), upy.squash(others)

    return results if arraify else upy.squash(results)