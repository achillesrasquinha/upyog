from __future__ import absolute_import

try:
    import os

    if os.environ.get("upyog_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = False, select = False)
except ImportError:
    pass

# imports - module imports
from upyog.__attr__ import (
    __name__,
    __version__,
    __description__,
    __author__
)
from upyog import cli
from upyog.__main__    import main
from upyog.config      import Settings
from upyog.util.jobs   import run_all as run_all_jobs, run_job
from upyog.util._dict  import (
    merge_dict,
    dict_from_list,
    autodict,
    lkeys,
    lvalues
)
from upyog.util._json import (
    load_json,
    dump_json
)
from upyog._compat import (
    iteritems,
    iterkeys
)
from upyog.util.array  import (
    compact,
    squash,
    flatten,
    sequencify,
    chunkify,
    normalize
)
from upyog.util.datetime import (
    check_datetime_format,
    get_timestamp_str
)
from upyog.util.types    import (
    get_function_arguments,
    auto_typecast
)
from upyog.util.system import (
    get_files,
    popen,
    make_temp_dir,
    unzip,
    makedirs,
    split_path,
    extract_all
)
from upyog.i18n import _
from upyog.model import BaseObject
from upyog.log import get_logger

settings = Settings()

def get_version_str():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version