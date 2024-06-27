def test_upyog_auto_datetime():
    import pytest
    import upyog as upy
    
    from datetime import datetime as dt, timezone

    assert upy.auto_datetime(dt(2018, 1, 1, 0, 0, 0, 0))     == dt(2018, 1, 1, 0, 0, 0, 0)
    assert upy.auto_datetime(1718834812)                     == dt(2024, 6, 19, 22, 6, 52, tzinfo=timezone.utc)

    assert upy.auto_datetime("2018-01-01 00:00:00.000000")   == dt(2018, 1, 1, 0, 0, 0, 0)
    assert upy.auto_datetime("2018-01-01 00:00:00")          == dt(2018, 1, 1, 0, 0, 0)
    assert upy.auto_datetime("2018-01-01 00:00")             == dt(2018, 1, 1, 0, 0)
    assert upy.auto_datetime("2018-01-01")                   == dt(2018, 1, 1)

    assert upy.auto_datetime("01-01-2018 00:00:00.000000")   == dt(2018, 1, 1, 0, 0, 0, 0)
    assert upy.auto_datetime("01-01-2018 00:00:00")          == dt(2018, 1, 1, 0, 0, 0)
    assert upy.auto_datetime("01-01-2018 00:00")             == dt(2018, 1, 1, 0, 0)
    assert upy.auto_datetime("01-01-2018")                   == dt(2018, 1, 1)
    assert upy.auto_datetime("00:00:00.000000")              == dt(1900, 1, 1, 0, 0, 0, 0)
    assert upy.auto_datetime("00:00:00")                     == dt(1900, 1, 1, 0, 0, 0)
    assert upy.auto_datetime("00:00")                        == dt(1900, 1, 1, 0, 0)
    assert upy.auto_datetime("00")                           == dt(1900, 1, 1, 0)

    with pytest.raises(ValueError):
        upy.auto_datetime("2018-01")

    with pytest.raises(ValueError):
        upy.auto_datetime("2018")