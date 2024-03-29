# imports - compatibility imports
from upyog._compat import (
    urlopen,
    Request,
    urlencode,
    HTTPError,
    ModuleNotFoundError
)

# imports - standard imports
import json

# imports - module imports
from upyog.request.response import Response
from upyog.util.string      import safe_encode
from upyog.log              import get_logger
from upyog._compat          import Queue

logger = get_logger()

# YAGNI: This patched "requests" works only for upyog's use-cases.

def get(*args, **kwargs):
    logger.info("Dispatching GET request with arguments %s and parameters %s." % (
        args, kwargs
    ))

    try:
        import requests as req
        return req.get(*args, **kwargs) # pragma: no cover
    except (ImportError, ModuleNotFoundError):
        url      = args[0]
        response = Response()

        try:
            http_response    = urlopen(url)
            status_code      = http_response.getcode()

            response.content = http_response.read()

            http_response.close()
        except HTTPError as e:
            status_code      = e.getcode()

        response.url         = url
        response.status_code = status_code

        return response

def post(*args, **kwargs):
    logger.info("Dispatching POST request with arguments %s and parameters %s." % (
        args, kwargs
    ))

    try:
        import requests as req
        return req.post(*args, **kwargs) # pragma: no cover
    except (ImportError, ModuleNotFoundError):
        url      = args[0]
        data     = kwargs.get("data",    { })
        headers  = kwargs.get("headers", { })

        response = Response()
        
        try:
            data             = safe_encode(urlencode(data))
            request          = Request(url, data = data, headers = headers)
            http_response    = urlopen(request)
            status_code      = http_response.getcode()

            response.content = http_response.read()

            http_response.close()
        except HTTPError as e:
            status_code      = e.getcode()

        response.url         = url
        response.status_code = status_code

        return response