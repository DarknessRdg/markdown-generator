import generate


def test_is_python_file():
    not_py_files = [
        'a.js', '__init__.py', 'a.c'
    ]

    python_files = [
        'a.py', '_test.py', '__test__.py'
    ]

    for file in not_py_files:
        assert not generate.is_python_file(file), f'{file} should not be treated as a python file.'

    for file in python_files:
        assert generate.is_python_file(file), f'{file} should be treated as a python file.'


def test_clean_object_name():
    assert generate.clean_object_name('class MyClass:') == 'MyClass'
    assert generate.clean_object_name('class MyClass(OtherClass):') == 'MyClass(OtherClass)'

    assert generate.clean_object_name('def _my_method():') == '_my_method()'
    assert generate.clean_object_name('def _my_method(self):') == '_my_method()'
    assert generate.clean_object_name('def method(self, *args):') == 'method(*args)'
    assert generate.clean_object_name('def method(self, *args, **kwargs):') == 'method(*args, **kwargs)'


def test_get_indent():
    indent = generate.DEFAULT_INDENTATION
    assert generate.get_indent(' ' * (0*indent)) == 0
    assert generate.get_indent(' ' * (1*indent)) == 1
    assert generate.get_indent(' ' * (2*indent)) == 2
    assert generate.get_indent(' ' * (3*indent)) == 3
    assert generate.get_indent(' ' * (4*indent)) == 4
    assert generate.get_indent(' ' * (100*indent)) == 100
    assert generate.get_indent('    def class(): {}'.format(' ' * 100)) == 1
    assert generate.get_indent('    class X() {}'.format(' ' * 100)) == 1
