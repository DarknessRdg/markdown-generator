from indented_language import clear_docstring_keywords


def test_keywords():
    assert clear_docstring_keywords('Args:') == '\n**Args:**\n\n'
    assert clear_docstring_keywords('Returns:') == '\n**Returns:**\n\n'
    assert clear_docstring_keywords('Raises:') == '\n**Raises:**\n\n'


def test_not_change_line_when_keywords_changes_any_letter():
    assert clear_docstring_keywords('args:') == 'args:'
    assert clear_docstring_keywords('Args') == 'Args'

    assert clear_docstring_keywords(' Args:') == ' Args:'
    assert clear_docstring_keywords('Args: ') == 'Args: '
