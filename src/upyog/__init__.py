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
from upyog.api.base    import BaseAPI
from upyog.util._dict  import (
    merge_dict,
    merge_deep,
    dict_from_list,
    autodict,
    lkeys,
    lvalues,
    check_struct as check_dict_struct
)
from upyog.util._json import (
    load_json,
    dump_json,
    JSONLogger
)
from upyog._compat import (
    iteritems,
    iterkeys,
    itervalues
)
from upyog.util.array  import (
    compact,
    squash,
    flatten,
    sequencify,
    chunkify,
    normalize
)
from upyog.util.string import (
    lower,
    upper,
    strip,
    get_random_str,
    pluralize,
    labelize
)
from upyog.util.datetime import (
    check_datetime_format,
    get_timestamp_str,
    auto_datetime,
    now
)
from upyog.util.types    import (
    get_function_arguments,
    auto_typecast,
    build_fn,
    classname
)
from upyog.util.system import (
    get_files,
    popen,
    make_temp_dir,
    make_temp_file,
    unzip,
    makedirs,
    split_path,
    extract_all,
    check_path,
    abslistdir,
    sha256sum,
    pardir,
    which,
    remove,
    walk,
    read,
    write
)
from upyog.util.environ import (
    getenv,
)
from upyog.db import (
    get_connection as get_db_connection,
)
from upyog.util.request import (
    download_file,
    TokenAuth
)
from upyog.util.mixin import (
    create_obj_registerer
)
from upyog.util.imports import (
    import_handler
)
from upyog.config import (
    get_config_path
)
from upyog.util.progress import (
    progress
)
from upyog.exception import PopenError
from upyog.i18n import _
from upyog.model import BaseObject
from upyog.log import get_logger
from upyog.limits import (
    MAX_UNSIGNED_SHORT
)

settings = Settings()

def get_version_str():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version