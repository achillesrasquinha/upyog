def test_upyog_get_timestamp_str():
    import upyog as upy
    import datetime as dt

    dtobj = dt.datetime(2021, 9, 15, 14, 24, 11)

    assert upy.get_timestamp_str(dtobj=dtobj) == "2021-09-15 14:24:11"
    assert upy.get_timestamp_str(format_="%d/%m/%Y", dtobj=dtobj) == "15/09/2021"