def test_upyog_get_aws_credentials():
    import upyog as upy
    from unittest.mock import patch

    class MockCredentials:
        def __init__(self):
            self.access_key = "test_access_key"
            self.secret_key = "test_secret_key"
            self.token      = "test_token"

    with patch('boto3.Session') as mock_session:
        mock_session.return_value.get_credentials.return_value = MockCredentials()

        creds = upy.get_aws_credentials()
        assert "default" in creds
        assert "aws_access_key_id"     in creds["default"]
        assert "aws_secret_access_key" in creds["default"]
        assert "aws_session_token"     in creds["default"]