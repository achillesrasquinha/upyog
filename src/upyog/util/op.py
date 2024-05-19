from upyog.util.array import is_list_like, sequencify, is_sequence_like
from upyog.util._dict import lvalues
from upyog.util.types import lmap
from upyog.util.eject import ejectable
from functools import reduce

O = {
    "EQUALS_STRING": "eq",
    "EQUALS_OPERATOR_1": "==",
    "EQUALS_OPERATOR_2": "=",
    "NOT_EQUALS_STRING": "ne",
    "NOT_EQUALS_OPERATOR": "!=",
    "LESS_THAN_STRING": "lt",
    "LESS_THAN_OPERATOR": "<",
    "LESS_THAN_OR_EQUALS_STRING": "lte",
    "LESS_THAN_OR_EQUALS_OPERATOR": "<=",
    "GREATER_THAN_STRING": "gt",
    "GREATER_THAN_OPERATOR": ">",
    "GREATER_THAN_OR_EQUALS_STRING": "gte",
    "GREATER_THAN_OR_EQUALS_OPERATOR": ">=",
    "CONTAINS_STRING": "contains",
    "STARTS_WITH_STRING": "startswith",
    "ENDS_WITH_STRING": "endswith",
    "IN_STRING": "in",
    "NOT_IN_STRING": "notin"
}

@ejectable(deps = ["is_sequence_like"])
def _check_in(x, y, op):
    x = sequencify(x)

    output = False

    if op == "in":
        for i in x:
            if (is_sequence_like(i) and i in y) or i == y:
                output = True
                break
    else:
        for i in x:
            output = output and (is_sequence_like(i) and i not in y) or i != y

    return output

@ejectable(globals_ = { "O": O }, deps = ["_check_in"])
def op(t):
    if t in (O["EQUALS_STRING"], O["EQUALS_OPERATOR_1"], O["EQUALS_OPERATOR_2"]):
        return lambda x, y: x == y
    elif t in (O["NOT_EQUALS_STRING"], O["NOT_EQUALS_OPERATOR"]):
        return lambda x, y: x != y
    elif t in (O["LESS_THAN_STRING"], O["LESS_THAN_OPERATOR"]):
        return lambda x, y: x < y
    elif t in (O["LESS_THAN_OR_EQUALS_STRING"], O["LESS_THAN_OR_EQUALS_OPERATOR"]):
        return lambda x, y: x <= y
    elif t in (O["GREATER_THAN_STRING"], O["GREATER_THAN_OPERATOR"]):
        return lambda x, y: x > y
    elif t in (O["GREATER_THAN_OR_EQUALS_STRING"], O["GREATER_THAN_OR_EQUALS_OPERATOR"]):
        return lambda x, y: x >= y
    elif t in (O["STARTS_WITH_STRING"], O["ENDS_WITH_STRING"]):
        return lambda x, y: getattr(x, t)(y)
    elif t in (O["CONTAINS_STRING"], O["IN_STRING"]):
        return lambda x, y: _check_in(x, y, "in")
    elif t == O["NOT_IN_STRING"]:
        return lambda x, y: _check_in(x, y, "notin")
    else:
        raise ValueError(f"Invalid operator: {t}")

Op = reduce(lambda a, b: a.update({b: op(b)}) or a, lvalues(O), {})