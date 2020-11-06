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
'''


FUNCTION = 0
INLINE_DOCS = 7
UGLY_DOCS = 11
NON_DOCS = 16


@pytest.fixture(scope='module')
def file():
    split = FILE.split('\n')
    split.pop(0)

    return split


def test_multiple_lines_range(file):
    start, end = 1, 4
    assert get_docstring_range(file, FUNCTION) == range(start, end+1)


def test_inline_range(file):
    start = INLINE_DOCS + 1
    assert get_docstring_range(file, INLINE_DOCS) == range(start, start+1)


def test_non_standardized_docs(file):
    start = UGLY_DOCS + 1
    end = UGLY_DOCS + 3
    assert get_docstring_range(file, UGLY_DOCS) == range(start, end+1)


def test_non_docs(file):
    assert get_docstring_range(file, NON_DOCS) == range(0)
