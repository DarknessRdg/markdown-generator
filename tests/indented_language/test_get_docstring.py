import pytest

from indented_language import get_object_docstring
from tests.indented_language.utils import get_file

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


def test_returns_docs_without_white_space(file, mocker):
    mocker.patch('indented_language.must_backward_indent', return_value=False)
    docs = get_object_docstring(file, FUNCTION)
    assert docs == (
        'Returns:\n'
        '    - `None`: ...\n'
    )


def test_do_not_remove_extra_spaces(file):
    expected = '        This is my cods\n'
    actual = get_object_docstring(file, FUNCTION_WITH_MANY_BLANK_SPACES)
    assert actual == expected


def test_do_include_empty_lines():
    file = ['def function():', '"""start here', '   ', 'ends here"""']
    expected = 'start here\n   \nends here\n'
    assert get_object_docstring(file, 0) == expected


def test_function_with_multiple_args_with_indent_different_from_real_indent():
    file = '''
    def function(arg1, ag3, ag4
                 this_args_should_not_break
    ):
        """
        Here is my docs
        """
    '''
    file = list(map(lambda line: line[4:], get_file(file)))

    assert get_object_docstring(file, 0) == 'Here is my docs\n'
