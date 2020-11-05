from indented_language import is_file


def test_is_not_file_when_do_not_have_a_dot():
    assert not is_file('my_dirpy', extension='py')
    assert not is_file('my_dir_py', extension='py')
    assert not is_file('py', extension='py')
    assert not is_file('_py', extension='_py')


def test_is_not_a_file_when_do_not_have_a_name():
    assert not is_file('.py', extension='py')


def test_file_name_allowed():
    assert is_file('name.py', extension='py')
    assert is_file('name.my_new_extension', extension='my_new_extension')


def test_default_extension():
    assert is_file('name.py')
