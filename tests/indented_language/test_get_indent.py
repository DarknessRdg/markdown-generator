import logging

import pytest

from indented_language import get_indent


FILE_TEXT = '''
def function():
    pass


def function_nested():

    def function_nested_child():
        pass
    pass


def function_with_docs_space():

    pass


class MyClass:

    class Meta:
        model = MyModel

    def method_1(self):
        pass

    def get_method_nested(self):
        def get_method_nested_child():
            pass

'''

# Functions index in file
FUNCTION = 0
FUNCTION_NESTED = 4
FUNCTION_NESTED_CHILD = 6
FUNCTION_WITH_DOCS_SPACE = 11

CLASS = 16
CLASS_META = 18
CLASS_METHOD_1 = 21
CLASS_METHOD_NESTED = 24
CLASS_METHOD_NESTED_CHILD = 25


@pytest.fixture()
def file():
    split = FILE_TEXT.split('\n')
    split.pop(0)

    return split


def test_happy_function(file):
    assert get_indent(file, FUNCTION) == 0


def test_nested_function(file):
    assert get_indent(file, FUNCTION_NESTED) == 0
    assert get_indent(file, FUNCTION_NESTED_CHILD) == 1


def test_when_function_has_empty_spaces_before_starts_the_code(file):
    assert get_indent(file, FUNCTION_WITH_DOCS_SPACE) == 0


def test_class_indent(file):
    assert get_indent(file, CLASS) == 0
    assert get_indent(file, CLASS_META) == 1


def test_class_method(file):
    assert get_indent(file, CLASS_METHOD_1) == 1


def test_class_method_with_nested_function(file):
    assert get_indent(file, CLASS_METHOD_NESTED) == 1
    assert get_indent(file, CLASS_METHOD_NESTED_CHILD) == 2


def test_get_ident_with_non_default_ident_size(file):
    assert get_indent(file, FUNCTION, indent=1) == 3
