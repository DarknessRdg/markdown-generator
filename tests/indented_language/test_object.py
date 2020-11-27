import pytest

from indented_language import Object, TypeOfObject


@pytest.fixture
def instance_with_parent():
    grandparent = Object('class GrandParent:', '')
    parent = Object('def parent(self):', '', grandparent)
    return Object('def child():', '', parent)


@pytest.fixture
def instance():
    return Object('def function():', '')


def test_token(instance_with_parent):
    instance = instance_with_parent
    assert instance.token == 'def'

    instance = instance.parent
    assert instance.token == 'def'

    instance = instance.parent
    assert instance.token == 'class'


def test_type(instance, instance_with_parent):
    assert instance.type == TypeOfObject.FUNCTION

    child = instance_with_parent
    parent = child.parent
    grandparent = parent.parent

    assert child.type == TypeOfObject.METHOD
    assert parent.type == TypeOfObject.METHOD
    assert grandparent.type == TypeOfObject.CLASS


class TestPropertyName:
    def test_when_name_dont_have_parenthesis_or_double_dot(self):
        instance = Object('def function', '')
        assert instance.name == 'function'

    def test_without_parent(self, instance):
        assert instance.name == 'function()'

    def test_with_parent(self, instance_with_parent):
        expected = 'GrandParent.parent.child()'
        assert instance_with_parent.name == expected

    def test_name_not_include_self(self):
        clazz = Object('class MyClass:', '')
        args = '', clazz
        expected = 'MyClass.method(arg1, arg2)'

        instance = Object('def method(self)', *args)
        assert instance.name == 'MyClass.method()'

        instance = Object('def method(self, arg1, arg2)', *args)
        assert instance.name == expected

        instance = Object('def method(self , arg1, arg2)', *args)
        assert instance.name == expected

        instance = Object('def method(   self, arg1, arg2)', *args)
        assert instance.name == expected

        instance = Object('def method(   self  , arg1, arg2)', *args)
        assert instance.name == expected


class TestStr:
    def test_without_parent(self, instance):
        assert str(instance) == '### def function()'

    def test_with_parent(self, instance_with_parent):
        expected = '### def GrandParent.parent.child()'
        assert str(instance_with_parent) == expected
