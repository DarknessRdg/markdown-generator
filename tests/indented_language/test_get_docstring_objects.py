import pytest

from indented_language import get_docstring_objects, Object
from tests.indented_language.utils import get_file

FILE = '''
class MyClass:
    """class"""

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


def test_nested_functions(file, clazz, method, function, other_function,
                          method_2):
    assert get_docstring_objects(file, 0)[0] == [
        clazz, method, function, method_2, other_function
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
