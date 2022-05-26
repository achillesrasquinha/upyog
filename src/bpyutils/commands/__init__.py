# imports - compatibility imports
from __future__ import absolute_import
import sys
import os.path as osp

from bpyutils.commands.util 	import cli_format
from bpyutils.util._dict        import merge_dict
from bpyutils.util.types        import lmap, auto_typecast
from bpyutils.util.string       import strip
from bpyutils.util.imports      import import_handler
from bpyutils.util.system       import touch
from bpyutils.util.error        import pretty_print_error
from bpyutils.util.test         import generate_tests
from bpyutils.util.doc          import generate_docs
from bpyutils.db                import run_db_shell
from bpyutils 		      	    import (cli, log, parallel)
from bpyutils._compat		    import iteritems, Mapping
from bpyutils.config            import environment, get_config_path
from bpyutils.__attr__      	import __name__ as NAME
from bpyutils.exception         import DependencyNotFoundError

logger    = log.get_logger(level = log.DEBUG)

ARGUMENTS = dict(
    run_job                     = None,
    params                      = None,
    jobs						= 1,
    check		 				= False,
    interactive  				= False,
    yes			 				= False,
    no_cache		            = False,
    no_color 	 				= True,
    output						= None,
    ignore_error				= False,
    force						= False,
    generate_tests              = None,
    output_dir                  = None,
    verbose		 				= False
)

@cli.command
def command(**ARGUMENTS):
    try:
        return _command(**ARGUMENTS)
    except Exception as e:
        if not isinstance(e, DependencyNotFoundError):
            cli.echo()

            pretty_print_error(e)

            cli.echo(cli_format("""\
An error occured while performing the above command. This could be an issue with
"bpyutils". Kindly post an issue at https://github.com/achillesrasquinha/bpyutils/issues
""", cli.RED))
        else:
            raise e

def to_params(kwargs):
    class O(object):
        pass

    params = O()

    kwargs = merge_dict(ARGUMENTS, kwargs)

    for k, v in iteritems(kwargs):
        setattr(params, k, v)

    return params

def format_params(params):
    params = params or []
    params = lmap(lambda x: lmap(strip, x.split(";")), params)
    
    args   = {}
    
    for param in params:
        for p in param:
            key, value = p.split("=")
            args[key]  = auto_typecast(value)

    return args
            
def _command(*args, **kwargs):
    a = to_params(kwargs)

    if not a.verbose:
        logger.setLevel(log.NOTSET)

    logger.info("Environment: %s" % environment())
    logger.info("Arguments Passed: %s" % locals())

    file_ = a.output

    if file_:
        logger.info("Writing to output file %s..." % file_)
        touch(file_)
    
    logger.info("Using %s jobs..." % a.jobs)

    if a.dbshell:
        path_config = get_config_path(name = a.dbshell or NAME)
        path_db = osp.join(path_config, "db.db")
        run_db_shell(path_db)

    if a.run_jobs:
        logger.info("Running module %s" % a.run_jobs)

        for module in a.run_jobs:
            jobs = import_handler("%s.jobs" % module)
            args = format_params(a.param)

            for job in jobs:
                name = job

                if isinstance(job, Mapping):
                    name = job["name"]
                
                job_module_runner = import_handler("%s.%s.run" % (module, name))

                try:
                    job_module_runner(**args)
                except Exception as e:
                    pretty_print_error(e)
                    sys.exit(1)
    else:
        if a.run_job:
            for job in a.run_job:
                logger.info("Running a specific job %s" % job)

                job_module_runner = import_handler("%s.run" % job)
                args = format_params(a.param)
                
                try:
                    job_module_runner(**args)
                except Exception as e:
                    pretty_print_error(e)
                    sys.exit(1)

    if a.method:
        for method in a.method:
            args = format_params(a.param)

            callable = import_handler(method)
            callable(**args)

    if a.run_ml:
        args = format_params(a.param)
        pipelines = [
            "data.get_data",
            "data.preprocess_data",
            "pipelines.train"
        ]
        
        args = format_params(a.param)
        callables = []

        for pipeline in pipelines:
            callable = import_handler("%s.%s" % (a.run_ml, pipeline))
            callables.append(callable)

        if a.online:
            with parallel.pool(processes = a.jobs) as pool:
                pool.map(callable)
        else:
            for callable in callables:
                callable(**args)

    if a.generate_tests:
        generate_tests(a.generate_tests, check = a.check, target_dir = a.output_dir)
        
    if a.generate_docs:
        generate_docs(a.generate_docs, check = a.check, target_dir = a.output_dir)