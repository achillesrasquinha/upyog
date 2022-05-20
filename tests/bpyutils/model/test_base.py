import pytest

from bpyutils.model.base import (
  BaseObject
)

class MockObject(BaseObject):
	_REPR_ATTRS = ("prop",)

	@property
	def prop(self):
		return "value"

def test_base_object():
	o = BaseObject(name = "foo")
	assert o.name == "foo"

def test_base_object___repr__():
	o = MockObject()
	assert repr(o) == "<MockObject prop='value'>"