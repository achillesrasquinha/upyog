from io import BytesIO

from unittest.mock import MagicMock

class MockCredentials(MagicMock):
    access_key = "access_key"
    secret_key = "secret_key"
    token      = "token"
    service    = "service"
    region     = "region"

class MockRequest(MagicMock):
    url     = "https://example.com"
    method  = "GET"
    content = BytesIO(b"foobar")
    headers = {
        "header1": "value1",
        "header2": "value2",
    }


def test_upyog_AWSSigV4Auth():
    import upyog as upy

    mock_credentials = MockCredentials()

    auth = upy.AWSSigV4Auth(
        access_key=mock_credentials.access_key,
        secret_key=mock_credentials.secret_key,
        token=mock_credentials.token,
        service=mock_credentials.service,
        region=mock_credentials.region,
    )

    r = MockRequest()

    r = upy.squash(list(auth.auth_flow(r)))

    for header in ["Authorization", "X-Amz-Security-Token", "X-Amz-Date"]:
        assert header in r.headers