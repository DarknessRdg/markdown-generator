import pytest

from indented_language import get_docstring_objects, Object
from tests.indented_language.utils import get_file

FILE = '''
class MyClass:
    """class"""

    class Meta:
        pass

    def method(self):
        """method"""

        def function():
            """function"""

    def method_2(self):
        """method 2"""
def other_fun():
    """function"""
'''


@pytest.fixture
def file():
    return get_file(FILE)


@pytest.fixture
def clazz():
    return Object('class MyClass:', 'class')


@pytest.fixture
def clazz_meta(clazz):
    return Object('class Meta:', '', clazz)


@pytest.fixture
def method(clazz):
    return Object('def method(self):', 'method', clazz)


@pytest.fixture
def method_2(clazz):
    return Object('def method_2(self):', 'method 2', clazz)


@pytest.fixture
def function(method):
    return Object('def function():', 'function', method)


@pytest.fixture
def other_function():
    return Object('def other_fun():', 'function')


def test_single_function():
    file = ['def function():', '"""docs"""']
    assert get_docstring_objects(file, 0)[0] == [
        Object('def function()', 'docs')
    ]


def test_many_functions():
    file = ['def function():', '"""docs"""', ''] * 3
    objects = [Object('def function()', 'docs')] * 3

    assert get_docstring_objects(file, 0)[0] == objects


def test_nested_functions(file, clazz, clazz_meta, method, function,
                          other_function, method_2):
    assert get_docstring_objects(file, 0)[0] == [
        clazz, clazz_meta, method, function, method_2, other_function
    ]


FUNCTION_MANY_ARGS = '''
def function(
    arg1: Int,
    arg2: Empty = Empty(), 
    arg3
):
    """
    here is my docs
    """
'''


def test_get_function_that_has_more_than_one_line_parameters():
    file = get_file(FUNCTION_MANY_ARGS)

    doc_object, index = get_docstring_objects(file, 0)

    assert index == len(file)
    assert doc_object == [
        Object(
            'def function(arg1: Int, arg2: Empty = Empty(), arg3 ):',
            'here is my docs'
        )
    ]


METHODS_WITH_MANY_ARGS = '''
class MyClass:
   def method_1(arg1, args2, arg2) -> str:
        """Here is my docs"""
        pass

    def method_2(
            self) -> None:
        """Here is my docs 2"""
        pass
'''


def test_methods_with_may_args():
    file = get_file(METHODS_WITH_MANY_ARGS)

    doc_object, _ = get_docstring_objects(file, 0)

    clazz = Object('class MyClass:', '')

    assert len(doc_object) == 3
    assert doc_object[-1].parent == clazz
    assert doc_object[-2].parent == clazz
