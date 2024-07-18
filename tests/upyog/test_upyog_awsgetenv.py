def test_upyog_awsgetenv():
    import upyog as upy
    import unittest.mock as mock

    with mock.patch('os.environ', {
        "AWS_ACCESS_KEY_ID":     "foobar",
        "AWS_SECRET_ACCESS_KEY": "barbaz"
    }):
        assert upy.awsgetenv("ACCESS_KEY_ID")     == "foobar"
        assert upy.awsgetenv("SECRET_ACCESS_KEY") == "barbaz"

        assert not upy.awsgetenv("PROFILE")