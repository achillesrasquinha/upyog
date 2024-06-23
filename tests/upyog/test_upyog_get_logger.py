def test_upyog_get_logger():
    import upyog as upy

    logger = upy.get_logger("test")
    assert logger.name  == "test"