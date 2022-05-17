import pytest

from bpyutils.db import (
    get_connection,
    run_db_shell
)

def test_get_connection():
    db  = get_connection(log = True)
    res = db.query("select 1+1 as result")
    assert res == { "result": 2 }

def test_run_db_shell():
    db = get_connection()

    with pytest.raises(SystemExit):
        run_db_shell(db.path)