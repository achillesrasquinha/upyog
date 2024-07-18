def test_base_object():
    import upyog as upy

    class Foo(upy.BaseObject):
        _REPR_ATTRS = ["foo"]

        def __init__(self, foo = "bar", **kwargs):
            super_ = super(Foo, self)
            super_.__init__(foo = foo, **kwargs)

    instance = Foo()
    assert instance.class_name == "Foo"
    assert instance.foo        == "bar"
    
    assert repr(instance) == "<Foo foo='bar'>"