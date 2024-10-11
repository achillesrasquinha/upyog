def test_upyog_classname():
    class Foo:
        pass

    import upyog as upy

    assert upy.classname(Foo()) == "Foo"