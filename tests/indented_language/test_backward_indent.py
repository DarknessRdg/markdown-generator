import contextlib

from indented_language import backward_indent
from tests.indented_language.utils import get_file


def test_backward_same_indent_to_all_next_lines():
    file = """
    Args:
        - line 1
        - line 2
            - line.line1
    """
    file = get_file(file)
    file.pop()  # empty string

    index, base_indent = -1, 0

    with contextlib.suppress(IndexError):
        backward_indent(file, index, base_indent)

    assert file == [
            'Args:',
            '    - line 1',
            '    - line 2',
            '        - line.line1',
        ]


def test_backward_only_while_indent_do_not_decrease():
    file = """
    Args:
        - arg 1
            - arg 1.1

    Decrease
        - must stop
    """

    file = get_file(file)
    file.pop()  # empty string

    index, base_indent = -1, 0

    with contextlib.suppress(IndexError):
        backward_indent(file, index, base_indent)

    assert file == [
        'Args:',
        '    - arg 1',
        '        - arg 1.1',
        '',
        '    Decrease',
        '        - must stop'
    ]
