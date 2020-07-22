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

