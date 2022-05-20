import pytest

from bpyutils.api.base import (
  _path_to_method_name,
  BaseAPI
)

def _assert_response_ok(response):
	assert response.ok

@pytest.fixture
def httpbin():
	api = BaseAPI(url = "https://httpbin.org")
	return api

def test__path_to_method_name():
	assert _path_to_method_name("api/user/me") 	== "api_user_me"
	assert _path_to_method_name("api")		   	== "api"
	assert _path_to_method_name("api/user") 	== "api_user"
	# assert _path_to_method_name("Api/User")		== "api_user" # TODO: fix
	# assert _path_to_method_name("api/user/:id") 	== "api_user" # TODO: implement

def test_base_api():
	raise NotImplementedError

def test_base_api___init__():
	raise NotImplementedError

def test_base_api__create_api_function():
	raise NotImplementedError

def test_base_api__build_api():
	raise NotImplementedError

def test_base_api__build_url():
	raise NotImplementedError

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