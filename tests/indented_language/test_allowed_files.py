import pytest

from indented_language import is_allowed_files

IS_FILE_FUNCTION = 'indented_language.is_file'


@pytest.fixture()
def is_file(mocker):
    mocker.patch(IS_FILE_FUNCTION, return_value=True)


@pytest.fixture()
def is_not_file(mocker):
    mocker.patch(IS_FILE_FUNCTION, return_value=False)


def test_ignores_with_custom_regex_expression(is_file):
    assert not is_allowed_files('name.py', ignore=['name'])

    # word
    assert not is_allowed_files('name.py', ignore=[r'\w+'])
    # starts with 'n'
    assert not is_allowed_files('name.py', ignore=[r'^n'])
    # ends with 'e'
    assert not is_allowed_files('name.py', ignore=[r'.*e$'])


def test_default_ignored(is_file):
    assert not is_allowed_files('__init__.py')
    assert not is_allowed_files('__py_file__.py')
    assert not is_allowed_files('_my_private_file.py')


def test_not_allows_when_is_not_file(is_not_file):
    assert not is_allowed_files('not_a_file')


def test_allows_when_is_a_file(is_file):
    assert is_allowed_files('not_a_file.py', ignore=[])
