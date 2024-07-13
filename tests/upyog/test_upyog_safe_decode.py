def test_upyog_safe_decode():
    import pytest
    import upyog as upy

    assert upy.safe_decode(b'hello') == 'hello'
    assert upy.safe_decode('hello')  == 'hello'
    assert upy.safe_decode(u'hello') == 'hello'
    
    assert upy.safe_decode(1) == 1