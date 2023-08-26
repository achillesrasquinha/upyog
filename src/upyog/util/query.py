import upyog as upy
from upyog._compat import Mapping, iteritems
from upyog.util.array import is_list_like, sequencify, squash
from upyog.util._dict import hasattr2, getattr2
from upyog.util.op import op

@upy.ejectable(deps = ["is_list_like", "sequencify", "squash", "hasattr2", "getattr2", "op"], sources = ["upyog._compat"])
def where(data, clause, other = False, clauses = False):
    arraify  = is_list_like(data)
    data     = sequencify(data)

    results  = []
    others   = []

    triggers = {}

    force    = True

    if isinstance(clause, Mapping):
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
        elif isinstance(clause, Mapping):
            for key, value in iteritems(clause):
                ref = key

                key = key.split("$")
                if len(key) > 1:
                    key = key[0]
                else:
                    key = key[0]

                added = False

                if hasattr2(record, key):
                    if isinstance(value, Mapping):
                        for op_, val in iteritems(value):
                            if callable(op_):
                                constraint = op_
                            else:
                                constraint = op(op_)

                            op1 = getattr2(record, key)
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
                        if not value(getattr2(record, key)):
                            add.append(False)
                            added = True
                            
                            if force:
                                break
                    else:
                        # TODO: callable for value?
                        if getattr2(record, key) != value:
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
            output = squash(results), squash(others)

    output = output or (results if arraify else squash(results))

    if clauses:
        output = output, triggers

    return output