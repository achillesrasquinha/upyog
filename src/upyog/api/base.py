# imports - standard imports
import os, random
import re
import string
import json

from upyog.model.base           import BaseObject
from upyog.util.imports         import import_or_raise
from upyog._compat              import (
    urlencode, iteritems, urlparse,
    Mapping
)
from upyog.util.array           import (
    sequencify,
)
from upyog.log                  import get_logger
from upyog.util.request         import (
    download_file
)

logger = get_logger()

def _path_to_method_name(path):
    # strip leading and trailing "/"
    formatted = path.strip("/")
    # replace all "/" with "_"
    formatted = formatted.replace("/", "_")
    # insert "_" before every capital letter.
    formatted = re.sub(r"(\w)([A-Z])", r"\1_\2", formatted)
    # convert to lowercase
    formatted = formatted.lower()

    method_name = formatted

    return method_name

class BaseAPI(BaseObject):
    _REPR_ATTRS = ("url",)

    """
    :param url: A base URL to use.
    :param proxies: A dictionary/list of proxies to use. If a list is passed,
        each element in the list should be a dictionary of the format 
        ``{ protocol: ip }``.
    :param test: Attempt to test the connection to the base url.
    """
    def __init__(self, url = None, proxies = [ ], test = False, token = None,
                 verbose = False, rate = None, auth = None, session = None, async_ = False,
                 retries = 1, on_error = None, **kwargs):
        super_ = super(BaseAPI, self)
        super_.__init__(**kwargs)

        self._url = self._format_uri_path(url or getattr(self, "url"),
            **kwargs)

        if async_:
            self._async   = True
            self._session = None
        else:
            self._requests = import_or_raise("requests")
            self._session  = session or self._requests.Session()

        if proxies and \
            not isinstance(proxies, (Mapping, list, tuple)):
            raise TypeError((
                "proxies %s are not of valid type. You must "
                "either a dictionary of a list of dictionaries of the "
                "following format { protocol: ip }."))

        if isinstance(proxies, Mapping):
            proxies = [proxies]

        self.token = token

        self._auth  = auth

        self._proxies = proxies
        self._rate    = rate

        self._retries  = retries

        self._build_api()

        if test:
            self.ping()

    def _format_uri_path(self, url, **kwargs):
        formatter = string.Formatter()
        str_args  = formatter.parse(url)
        uri_keys  = [arg[1] for arg in str_args if arg[1]]

        variables = getattr(self, "variables", {})
        variables.update(kwargs.get("variables", {}))

        to_format = { }

        for key in uri_keys:
            key_config = variables.get(key, None)
            if not key_config:
                if not key in kwargs:
                    raise ValueError("Missing argument '%s' for URL." % key)
                else:
                    to_format[key] = kwargs[key]
            else:
                required = key_config.get("required", False)
                default  = key_config.get("default", None)

                if required and not key in kwargs:
                        raise ValueError("Missing argument '%s' for URL." % key)
                else:
                    to_format[key] = kwargs.get(key, default)

        formatted = url.format(**to_format)

        return formatted

    @property
    def auth(self):
        auth = getattr(self, "_auth", None)
        return auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def url(self):
        url = getattr(self, "_url", None)
        
        if url:
            return self._format_uri_path(url)

    def _create_api_function(self, api, base_config = {}):
        METHOD_CALLERS = {
               "GET": self.get,
              "POST": self.post,
               "PUT": self.put,
            "DELETE": self.delete,
        }

        doc = api.get("doc")

        def fn(*args, **kwargs):
            data = {}

            query = self._format_uri_path(api["path"], variables = api.get("variables", {}), **kwargs)

            params = api.get("params")
            method = api.get("method", "GET")
            auth_required = api.get("auth", False)
            stream = api.get("stream", False)

            if params:
                parameters = []

                if isinstance(params, Mapping):
                    for param, info in iteritems(params):
                        type_    = info.get("type", "param")
                        required = info.get("required")
                        argument = info.get("argument", param)
                        default  = info.get("default")

                        if (type_ == "path" or required) and argument not in kwargs:
                            raise ValueError("Argument %s is not passed." % argument)

                        if type_ == "path":
                            value = kwargs.get(argument)
                            query = query.replace(":%s" % param, str(value))
                        else:
                            if callable(default):
                                default = default(*args, **kwargs)

                            kwargs[param] = kwargs.get(argument, default)
                            parameters.append(param)

                parameters = sequencify(parameters)
                for parameter in parameters:
                    if parameter in kwargs:
                        value = kwargs.get(parameter)
                        data[parameter] = value

            if method == "POST":
                if "json" in kwargs:
                    args = {
                        "data": json.dumps(kwargs["json"]),
                        "headers": {"Content-Type": "application/json"}
                    }
                else:
                    args = {"data": data}
            else:
                args = {"params": data}

            if auth_required:
                if self.auth:
                    args.update({"auth": self.auth})

            after_request = None

            if stream:
                args.update({"stream": True})
                target = kwargs.get("target", None)
                if target:
                    after_request = lambda response, **kwargs: download_file(response, target)

            method_caller = METHOD_CALLERS.get(method, self.get)

            if "mock_response" in api:
                response = api["mock_response"](query, **args)
            else:
                response = method_caller(query, **args)

            after_request = api.get("after_request", base_config.get("after_request", None)) \
                or after_request

            if after_request:
                response = after_request(response, req_args = args)
            
            return response

        if doc:
            fn.__doc__ = doc

        return fn
        
    def _build_api(self):
        api_config = getattr(self, "api", {})
        if api_config:
            if "paths" in api_config:
                for api in api_config["paths"]:
                    if isinstance(api, str):
                        api = dict(path = api)
                    elif isinstance(api, (list, tuple)):
                        api = dict(path = api[0], method_name = api[1])

                    query = api["path"]

                    fn = self._create_api_function(api, base_config = api_config)

                    method_name = api.get("method_name", _path_to_method_name(query))

                    setattr(self, method_name, fn)

    def _build_url(self, *args, **kwargs):
        params  = kwargs.pop("params", None) 
        prefix  = kwargs.get("prefix", True)
        
        parts   = []

        if prefix:
            parts.append(self._url)

        url = "/".join(map(str, sequencify(parts) + sequencify(args)))

        if params:
            encoded  = urlencode(params)
            url     += "?%s" % encoded

        api = kwargs.get("api", {})
        url = self._format_uri_path(url, variables = api.get("variables", {}), **kwargs)

        return url

    def request(self, method, path = None, *args, **kwargs):
        req_args = self._get_req_args(method, path, *args, **kwargs)
        self._session.verify = req_args["verify"]

        response = self._session.request(method, req_args["url"],
            headers = req_args["headers"],
            *req_args["args"],
            **req_args["kwargs"]
        )

        return response # TODO: ?

    def _get_req_args(self, method, path = None, *args, **kwargs):
        raise_error = kwargs.pop("raise_error", True)
        token       = kwargs.pop("token",       self.token)

        headers     = getattr(self, "headers", {})
        headers.update(kwargs.pop("headers", {}))

        proxies     = kwargs.pop("proxies", self._proxies)
        data        = kwargs.get("params",  kwargs.get("data"))
        prefix       = kwargs.get("prefix",    True)
        async_      = kwargs.pop("async_",  False)

        verify      = kwargs.get("verify", 
            os.environ.get("REQUESTS_CA_BUNDLE", "/etc/ssl/certs/ca-certificates.crt")                             
        )

        if token:
            headers.update({
                "Authorization": "Bearer %s" % token,
            })

        if self._auth:
            kwargs.update({"auth": self._auth})

        if proxies:
            proxies = random.choice(proxies)
            logger.info("Using proxy %s to dispatch request." % proxies)

        url = self._build_url(path, prefix = prefix)

        parsed = urlparse(url)
        logger.info("%s %s %s" % (parsed.netloc, method, parsed.path))

        return {
            "url": url,
            "headers": headers,
            "proxies": proxies,
            "data": data,
            "prefix": prefix,
            "async_": async_,
            "raise_error": raise_error,
            "verify": verify,
            "args": args,
            "kwargs": kwargs
        }

    async def arequest(self, method, path = None, *args, **kwargs):
        req_args = self._get_req_args(method, path, *args, **kwargs)

        async with self:
            verify = req_args.pop("verify", None)
            httpx  = import_or_raise("httpx")

            transport = httpx.AsyncHTTPTransport(retries = self._retries)
            self._session = httpx.AsyncClient(transport = transport, verify = verify)
            async with self._session as session:
                response = await session.request(method, req_args["url"],
                    headers = req_args["headers"],
                    *req_args["args"], **req_args["kwargs"])
                return response

    def get(self, url, *args, **kwargs):
        """
        Dispatch a PUT request to the server.
        """
        return self.request("GET", url, *args, **kwargs)

    async def aget(self, url, *args, **kwargs):
        """
        Dispatch a PUT request to the server.
        """
        return await self.arequest("GET", url, *args, **kwargs)

    def post(self, url = None, *args, **kwargs):
        """
        Dispatch a POST request to the server.

        :param url: URL part (does not include the base URL).
        :param args: Arguments provided to ``api.request``
        :param kwargs: Keyword Arguments provided to ``api.request``
        """
        return self.request("POST", url, *args, **kwargs)
    
    async def apost(self, url = None, *args, **kwargs):
        """
        Dispatch a POST request to the server.

        :param url: URL part (does not include the base URL).
        :param args: Arguments provided to ``api.request``
        :param kwargs: Keyword Arguments provided to ``api.request``
        """
        return await self.arequest("POST", url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        """
        Dispatch a PUT request to the server.
        """
        response = self.request("PUT", url, *args, **kwargs)
        return response

    async def aput(self, url, *args, **kwargs):
        """
        Dispatch a PUT request to the server.
        """
        response = await self.arequest("PUT", url, *args, **kwargs)
        return response

    def delete(self, url, *args, **kwargs):
        """
        Dispatch a DELETE request to the server.
        """
        response = self.request("DELETE", url, *args, **kwargs)
        return response

    async def adelete(self, url, *args, **kwargs):
        """
        Dispatch a DELETE request to the server.
        """
        response = await self.arequest("DELETE", url, *args, **kwargs)
        return response

    def ping(self):
        """
        Check if the URL is alive.

        Example::

            >>> import upyog
            >>> client = upyog.Client()
            >>> client.ping()
            'pong'
        """
        self.request("HEAD", "")
        return "pong"
    
    async def aping(self):
        """
        Check if the URL is alive.

        Example::

            >>> import upyog
            >>> client = upyog.Client()
            >>> client.ping()
            'pong'
        """
        await self.arequest("HEAD", "")
        return "pong"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return await self.aclose()

    async def aclose(self):
        if self._session:
            return await self._session.aclose()