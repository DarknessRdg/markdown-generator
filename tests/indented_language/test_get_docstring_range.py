import pytest

from indented_language import get_docstring_range


FILE = '''
def function():
    """
    pass
    pass
    """
    pass

def inline_docs():
    """docs"""
    pass

def ugly_docs():
    """docs
    ends
    here"""

def non_docs():
    pass

def other():
    pass


def multiple_lines(
    args1: int,
arg2=Empty(),
        arg2
):
    """docs multiple line"""
'''


FUNCTION = 0
INLINE_DOCS = 7
UGLY_DOCS = 11
NON_DOCS = 16
MULTIPLE_LINES = 23


@pytest.fixture(scope='module')
def file():
    split = FILE.split('\n')
    split.pop(0)

    return split


def test_multiple_lines_range(file):
    start, end = 1, 4

    docs_range = get_docstring_range(file, FUNCTION)
    expected_range = range(start, end+1)

    assert docs_range.start == expected_range.start
    assert docs_range.stop == expected_range.stop


def test_inline_range(file):
    start = INLINE_DOCS + 1

    docs_range = get_docstring_range(file, INLINE_DOCS)
    expected_range = range(start, start+1)

    assert docs_range.start == expected_range.start
    assert docs_range.stop == expected_range.stop


def test_non_standardized_docs(file):
    start = UGLY_DOCS + 1
    end = UGLY_DOCS + 3

    docs_range = get_docstring_range(file, UGLY_DOCS)
    expected_range = range(start, end+1)

    assert docs_range.start == expected_range.start
    assert docs_range.stop == expected_range.stop


def test_non_docs(file):
    docs_range = get_docstring_range(file, NON_DOCS)
    expected_range = range(0)

    assert docs_range.start == expected_range.start
    assert docs_range.stop == expected_range.stop


def test_function_with_multiple_args(file):
    start = MULTIPLE_LINES + 5

    docs_range = get_docstring_range(file, MULTIPLE_LINES)
    expected_range = range(start, start+1)

    assert docs_range.start == expected_range.start
    assert docs_range.stop == expected_range.stop
