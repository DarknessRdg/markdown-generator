import pytest

from indented_language import get_docstring


FILE = '''
def function():
    """
    Returns:
        - `None`: ...
    """

def test_docs_with_many_blank_spaces():
    """
            This is my cods
    """
'''

FUNCTION = 0
FUNCTION_WITH_MANY_BLANK_SPACES = 6


@pytest.fixture
def file(mocker):
    def mock_fun(line):
        return line
    mocker.patch('indented_language.clear_docstring_keywords', mock_fun)

    split = FILE.split('\n')
    split.pop(0)
    return split


def test_returns_docs_without_white_space(file):
    docs = get_docstring(file, FUNCTION)
    assert docs == '''Returns:\n    - `None`: ...\n'''


def test_do_not_remove_extra_spaces(file):
    expected = '        This is my cods\n'
    assert get_docstring(file, FUNCTION_WITH_MANY_BLANK_SPACES) == expected
