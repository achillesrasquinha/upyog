def test_where():
    from upyog.util.query import where

    records = [{
        "name": "foo",
         "age": 20,
    }, {
        "name": "bar",
         "age": 30,
    }, {
        "name": "baz",
         "age": 10,
    }]

    assert where(records, { "name": "foo" }) == [{ "name": "foo", "age": 20 }]
    assert where(records, { "name": "bar" }) == [{ "name": "bar", "age": 30 }]
    assert where(records, { "name": "boo" }) == []

    assert where(records, { "age": 20 }) == [{ "name": "foo", "age": 20 }]

    assert where(records, { "age": { ">=": 20 } }) == records[:-1]

    assert where(records, { "age": { "<": 20 } }) == records[-1:]

    clause = {
        "$or": {
            "name": { "==": "foo" },
             "age": { ">": 20 }
        }
    }
    assert where(records, clause) == records[:-1]