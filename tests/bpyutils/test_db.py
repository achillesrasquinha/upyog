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

from bpyutils.db import (
  _get_queries,
  DB
)

def test__get_queries():
	raise NotImplementedError

def test_db():
	raise NotImplementedError

def test_db___init__():
	raise NotImplementedError

def test_db_connected():
	raise NotImplementedError

def test_db_connect():
	raise NotImplementedError

def test_db_query():
	raise NotImplementedError

def test_db_from_file():
	raise NotImplementedError



