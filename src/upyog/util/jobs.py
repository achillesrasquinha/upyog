# imports - standard imports
import os, os.path as osp
from   functools import partial
import sys

# imports - module imports
from upyog.config          import PATH, Settings
from upyog.util.imports    import import_handler
from upyog.util.system     import popen
from upyog.util._dict      import merge_dict
from upyog.util.environ    import getenvvar, getenv
from upyog import parallel, log

settings = Settings()
logger   = log.get_logger()

JOBS = [
    
]

def run_job(module, name, variables = None):
    jobs = import_handler("%s.jobs" % module)
    job  = [job for job in jobs if job["name"] == name]

    if not job:
        raise ValueError("No job %s found." % name)
    else:
        job = job[0]

    variables = merge_dict(job.get("variables", {}), variables or {})

    popen("%s -c 'from upyog.util.imports import import_handler; import_handler(\"%s\")()'" %
        (sys.executable, "%s.%s.run" % (module, name)), env = variables)

def run_all(module):
    logger.info("Running all jobs...")

    jobs = import_handler("%s.jobs" % module)

    for job in jobs:
        if not job.get("beta") or getenv("JOBS_BETA"):
            run_job(module, job["name"], variables = job.get("variables"))