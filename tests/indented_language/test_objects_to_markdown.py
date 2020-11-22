from indented_language import objects_to_markdown, Object


def test_return_empty_string_when_no_docstring():
    objects = [
        Object('def function()', '')
    ]
    assert objects_to_markdown(objects) == ''


def test_return_empty_string_when_empty_list():
    objects = []
    assert objects_to_markdown(objects) == ''


def test_double_linebreaks_between_name_and_docs():
    objects = [Object('def function():', 'my docs')]
    assert objects_to_markdown(objects) == (
        '### def function()\n\n'
        'my docs'
    )


def test_join_all_lines_with_single_linebreak():
    objects = [
        Object('def function():', 'my function docs'),
        Object('class MyClass:', 'my class')
    ]
    assert objects_to_markdown(objects) == (
        '### def function()\n\n'
        'my function docs\n'
        '### class MyClass\n\n'
        'my class'
    )
