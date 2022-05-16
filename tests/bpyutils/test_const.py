import multiprocessing as mp

from bpyutils.const import CPU_COUNT

def test_cpu_count():
    assert CPU_COUNT == mp.cpu_count()