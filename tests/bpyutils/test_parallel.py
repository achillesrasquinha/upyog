# imports - module imports
from bpyutils import parallel

def test_pool():
    def _assert(pool):
        results = pool.map(sum, [(1, 2), (3, 4)])
        results = list(results)

        assert results[0] == 3
        assert results[1] == 7

    with parallel.pool() as pool:
        _assert(pool)

    with parallel.pool(class_ = parallel.NoDaemonPool) as pool:
        _assert(pool)

    # with parallel.no_daemon_pool() as pool:
    #     _assert(pool)

    #     process = pool.Process()
    #     assert process.daemon == False

import pytest

from bpyutils.parallel import (
  PoolMixin,
  BasePool,
  NoDaemonPool,
#   NonDaemonProcess,
  NoDaemonPool,
  no_daemon_pool
)

def test_pool_mixin():
	raise NotImplementedError

def test_pool_mixin_lmap():
	raise NotImplementedError

def test_base_pool():
	raise NotImplementedError

def test_no_daemon_pool():
	raise NotImplementedError

def test_no_daemon_pool___init__():
	raise NotImplementedError

def test_no_daemon_pool_imap():
	raise NotImplementedError

def test_no_daemon_pool_imap_unordered():
	raise NotImplementedError

def test_no_daemon_pool__shutdown():
	raise NotImplementedError

def test_no_daemon_pool_terminate():
	raise NotImplementedError

def test_no_daemon_pool_close():
	raise NotImplementedError

def test_no_daemon_pool_join():
	raise NotImplementedError

def test_non_daemon_process():
	raise NotImplementedError

def test_non_daemon_process_daemon():
	raise NotImplementedError

def test_non_daemon_process_daemon():
	raise NotImplementedError

def test_no_daemon_pool():
	raise NotImplementedError

def test_no_daemon_pool___init__():
	raise NotImplementedError

def test_no_daemon_pool_Process():
	raise NotImplementedError

def test_no_daemon_pool():
	raise NotImplementedError