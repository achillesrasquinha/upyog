import re
import os.path as osp

# from fake_useragent import UserAgent

from upyog.db import get_connection
from upyog.util.proxy     import get_random_requests_proxies
from upyog.util._dict     import merge_dict
from upyog.util.imports   import import_or_raise
from upyog.util.string    import get_random_str
from upyog.util.system    import makepath
from upyog.util.imports   import import_handler
from upyog import request as req
from upyog._compat import urlparse, quote as urlquote
from upyog.log import get_logger

import upyog as upy

# user_agent = UserAgent(verify_ssl = False)

LOG = get_logger(__name__)

# https://git.io/JsnSI
_REGEX_URL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def joinurl(*args):
    return "/".join([str(arg).strip("/") for arg in args])

def proxy_request(*args, **kwargs):
    fallback = kwargs.pop("fallback", False)

    session  = requests.Session()

    proxies  = get_random_requests_proxies()
    # session.headers.update({ "User-Agent": user_agent.random })
    session.proxies.update(proxies)

    try:
        kwargs["timeout"] = 5
        response = session.request(*args, **kwargs)
    except requests.exceptions.ConnectionError as e:
        if fallback:
            session.headers = kwargs.get("headers", {})
            session.proxies = kwargs.get("proxies", {})
            response = session.request(*args, **kwargs)
        else:
            raise e

    return response

def proxy_grequest(*args, **kwargs):
    proxies = get_random_requests_proxies()
    
    # kwargs["headers"] = merge_dict(kwargs.get("headers", {}), {
    #     "User-Agent": user_agent.random })
    kwargs["proxies"] = merge_dict(kwargs.get("proxies", {}), proxies)
    grequests         = import_or_raise("grequests")

    return grequests.request(*args, **kwargs)

def check_url(url, raise_err = True):
    if not re.match(_REGEX_URL, url):
        if raise_err:
            raise ValueError("Invalid URL: %s" % url)
        
        return False
    
    return True

def download_file(url, target = None, chunk_size = None, req_kwargs = {}):
    chunk_size  = chunk_size or upy.settings.get("max_chunk_download_bytes")

    if not isinstance(url, requests.Response):
        response = req.get(url, stream = True, **req_kwargs)
    else:
        response = url

    response.raise_for_status()

    headers     = response.headers

    size_total  = int(headers.get('content-length', 0))

    tqdm = None
    try:
        tqdm = import_handler("tqdm.tqdm")
    except ImportError:
        pass
    
    progress_bar = None

    if tqdm:
        progress_bar = tqdm(total = size_total, unit = 'iB', unit_scale = True)

    if not target:
        header = headers.get("content-disposition")

        if header:
            name    = re.findall("filename=(.+)", header)[0]
            target  = osp.abspath(name)
        else:
            target  = get_random_str()

    is_fhandler = hasattr(target, "write")

    if not is_fhandler:
        makepath(target)

    target = open(target, "wb") if not is_fhandler else target

    with target as f:
        for content in response.iter_content(chunk_size = chunk_size):
            if progress_bar:
                progress_bar.update(len(content))

            if content:
                f.write(content)

    if progress_bar:
        progress_bar.close()

        if size_total != 0 and progress_bar.n != size_total:
            raise ValueError("Unable to read downloaded file into path %s." % target)

    return target

try:
    import requests
    from requests.auth import AuthBase

    class TokenAuth(AuthBase):
        def __init__(self, token):
            self._token = token

        @property
        def token(self):
            return self._token

        def __call__(self, r):
            r.headers["Authorization"] = "Bearer %s" % self._token
            return r
except ImportError:
    LOG.warning("Unable to import requests. Some functions will not work.")