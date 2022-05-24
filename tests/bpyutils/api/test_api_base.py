import pytest

from bpyutils.api.base import (
  _path_to_method_name,
  BaseAPI
)

URL_HTTPBIN = "https://httpbin.org"

class HttpBin(BaseAPI):
	url = URL_HTTPBIN
	api = {
		"paths": [{
			"path": "status/:codes",
			"fn_name": "status",
			"doc": "This is the status api",
			"params": {
				"codes": {
					"type": "path",
					"required": True
				}
			}
		}, {
			"path": "json"
		}]
	}

def _assert_response_ok(response):
	assert response.ok

@pytest.fixture
def httpbin():
	api = HttpBin(url = URL_HTTPBIN)
	return api

def test__path_to_method_name():
	assert _path_to_method_name("api/user/me") 	== "api_user_me"
	assert _path_to_method_name("api")		   	== "api"
	assert _path_to_method_name("api/user") 	== "api_user"
	# assert _path_to_method_name("Api/User")		== "api_user" # TODO: fix
	# assert _path_to_method_name("api/user/:id") 	== "api_user" # TODO: implement

def test_base_api():
	with pytest.raises(TypeError):
		BaseAPI(proxies = 1)

def test_base_api__create_api_function(httpbin):
	_assert_response_ok(httpbin.json())
	_assert_response_ok(httpbin.status(codes = 200))

	assert httpbin.status.__doc__ == "This is the status api"

# TODO: Doesn't affect coverage but needs implementation.
# def test_base_api__build_api():
# 	raise NotImplementedError

def test_base_api__build_url(httpbin):
	assert httpbin._build_url("api/user") == "%s/api/user" % URL_HTTPBIN
	assert httpbin._build_url("api/user", params = { "id": 2 }) == "%s/api/user?id=2" % URL_HTTPBIN
	assert httpbin._build_url("api/user", prefix = False) == "api/user"

# TODO: check status codes?
def test_base_api_request(httpbin):
	_assert_response_ok(httpbin.request("get", "ip"))

def test_base_api_post(httpbin):
	_assert_response_ok(httpbin.post("post"))

def test_base_api_put(httpbin):
	_assert_response_ok(httpbin.put("put"))

def test_base_api_get(httpbin):
	_assert_response_ok(httpbin.get("get"))

def test_base_api_delete(httpbin):
	_assert_response_ok(httpbin.delete("delete"))

def test_base_api_ping(httpbin):
	assert httpbin.ping() == "pong"