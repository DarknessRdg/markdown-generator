import pytest

from indented_language import get_file_docstring
from tests.indented_language.utils import get_file

FILE = '''
"""
Here is my file docstring
With many lines

And a list here:
    - item 1
    - item 2
"""
'''


FILE_WITH_INLINE_DOCSTRING = '''
"""Single line docstring"""
'''

FILE_WITH_UGLY_DOCSTRING = '''
"""Here it starts
Here it ends
"""
'''


@pytest.fixture
def file():
    return get_file(FILE)


@pytest.fixture
def file_with_inline_docstring():
    return get_file(FILE_WITH_INLINE_DOCSTRING)


@pytest.fixture
def file_with_ugly_docstring():
    return get_file(FILE_WITH_UGLY_DOCSTRING)


def test_should_not_should_not_remove_any_indent(file):
    docstring = get_file_docstring(file)
    assert docstring == (
        'Here is my file docstring\n'
        'With many lines\n'
        '\n'
        'And a list here:\n'
        '    - item 1\n'
        '    - item 2'
    )


def test_inline_docstring(file_with_inline_docstring):
    docstring = get_file_docstring(file_with_inline_docstring)
    assert docstring == 'Single line docstring'


def test_ugly_docstring(file_with_ugly_docstring):
    docstring = get_file_docstring(file_with_ugly_docstring)
    assert docstring == (
        'Here it starts\n'
        'Here it ends'
    )
