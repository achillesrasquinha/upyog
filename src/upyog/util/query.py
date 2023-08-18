import upyog as upy

@upy.ejectable()
def where(data, clause, other = False, clauses = False):
    arraify  = upy.is_list_like(data)
    data     = upy.sequencify(data)

    results  = []
    others   = []

    triggers = {}

    force    = True

    if isinstance(clause, upy._compat.Mapping):
        if "$or" in clause:
            clause = clause["$or"]
            force  = False

    for record in data:
        add  = []

        if callable(clause):
            if not clause(record):
                add.append(False)

                if force:
                    break
        elif isinstance(clause, upy._compat.Mapping):
            for key, value in upy.iteritems(clause):
                ref = key

                key = key.split("$")
                if len(key) > 1:
                    key = key[0]
                else:
                    key = key[0]

                added = False

                if upy.hasattr2(record, key):
                    if isinstance(value, upy.Mapping):
                        for op, val in upy.iteritems(value):
                            if callable(op):
                                constraint = op
                            else:
                                constraint = upy.Op[op]

                            op1 = upy.getattr2(record, key)
                            op2 = val
                            
                            try:
                                if not constraint(op1, op2):
                                    add.append(False)
                                    added = True

                                    if force:
                                        break
                            except TypeError:
                                # TODO: warn here.
                                add.append(False)
                                added = True

                                if force:
                                    break
                    elif callable(value):
                        if not value(upy.getattr2(record, key)):
                            add.append(False)
                            added = True
                            
                            if force:
                                break
                    else:
                        # TODO: callable for value?
                        if upy.getattr2(record, key) != value:
                            add.append(False)
                            added = True

                            if force:
                                break

                if not force and not added:
                    add.append(True)
                    added = True

                    if clauses:
                        triggers[ref] = value
        else:
            raise TypeError(f"Invalid clause type: {type(clause)}")

        if force:
            add = all(add)
        else:
            add = any(add)

        if add:
            results.append(record)
        else:
            others.append(record)

    output = None

    if other:
        if arraify:
            output = results, others
        else:
            output = upy.squash(results), upy.squash(others)

    output = output or (results if arraify else upy.squash(results))

    if clauses:
        output = output, triggers

    return output