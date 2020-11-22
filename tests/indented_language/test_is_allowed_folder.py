from indented_language import is_allowed_folder, IGNORE_FOLDERS


def test_ignore_with_regex():
    assert is_allowed_folder('name', ['other_name'])
    assert not is_allowed_folder('name', [''])
    assert not is_allowed_folder('name', ['^n'])


def test_default_ignore_is_empty():
    assert len(IGNORE_FOLDERS) == 0
