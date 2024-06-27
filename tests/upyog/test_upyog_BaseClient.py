import pytest
import upyog as upy

class HTTPBinMixin:
    servers = {
        "default": {
            "url": "https://httpbin.org"
        }
    }

class HTTPBin(upy.BaseClient, HTTPBinMixin):
    pass

class AsyncHTTPBin(upy.AsyncBaseClient, HTTPBinMixin):
    pass

@pytest.fixture
def httpbin():
    httpbin = HTTPBin()
    return httpbin

@pytest.fixture
def async_httpbin():
    httpbin = AsyncHTTPBin()
    return httpbin

@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
@pytest.mark.parametrize("async_", [False, True])
async def test_upyog_base_client(method, async_, httpbin, async_httpbin):
    import upyog as upy
    client   = async_httpbin if async_ else httpbin

    name     = upy.lower(method)

    method   = getattr(client, f"a{name}" if async_ else name)
    response = await method(name) if async_ else method(name)

    assert response.status_code == 200
    
    data = response.json()
    assert data["url"] == async_httpbin.resurl(name)

@pytest.mark.asyncio
@pytest.mark.parametrize("async_", [False, True])
async def test_upyog_base_client_ping(async_, httpbin, async_httpbin):
    client   = async_httpbin if async_ else httpbin
    response = await client.aping() if async_ else client.ping()
    assert response == "pong"