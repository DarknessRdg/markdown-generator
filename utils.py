import contextlib
import logging


def handle_arg(arg):
    """
    Function to handle what happens with args passed thought terminal
    Args:
        arg: String with arg passed
    """
    levels = {
        '-v': logging.WARNING,
        '-vv': logging.INFO,
        '-vvv': logging.DEBUG
    }

    logging.basicConfig(level=levels[arg], format='%(name)-5s %(levelname)-8s %(message)s', )


def is_not_hidden_folder(file_name):
    return len(file_name.split('.')) == 1 and file_name != 'venv'


def get_code_string_from_doc(file, index):
    """
    Get markownd code with all indentation from file.
    i.e:
    ```json
    {
        "url": "htpps://www.github.com/"
    }
    ```

    Args:
        file: List. All
        index: int. Index of line where starts code tag

    Returns:
        Tuple(int, string):
            * index where ends code tag.
            * string with code as markdown
    """
    code_delimiter = '```'
    line = file[index]
    remove = line.index(code_delimiter)
    cont = 0
    code_lines = []
    while cont < 2:
        line = file[index]
        cont += line.count(code_delimiter)
        code_lines.append(line[remove:])

        index += 1

    return index - 1, ''.join(code_lines)


def get_md_string(object_parsed):
    """
    Function to generate a string with markdown from an object already parsed
    Args:
        object_parsed: ultis.classes.BaseObject() already parsed
    Returns:
        String with objects markdown
    """
    if object_parsed.name.startswith('__') or not object_parsed.doc:
        if not object_parsed.doc:
            logging.warning('Função/class sem docstring ' + object_parsed.name)
        return ''
    title = object_parsed.get_md_title()
    string = '### {}\n'.format(title)
    string += object_parsed.doc + '\n\n'

    object_parsed.children.sort(key=lambda obj: obj.name)
    for children in object_parsed.children:
        string += get_md_string(children)
    return string


class BaseObject:
    """
    Class to store class or function data
    Attributes:
        doc: current object's docstring
        name: objects name
        children: list of other objects that are children of current object
        parent: reference to current object parent, or None has no parent
        indent: int with objects indentation
    """
    def __init__(self, name, parent, indent):
        self.doc = ''
        self.name = name
        self.children = []
        self.parent = parent
        self.indent = indent

    def __str__(self):
        return self.name

    def get_md_title(self):
        if self.indent == 0:
            return self.name
        else:
            parent_name = self.parent.get_md_title()
            with contextlib.suppress(ValueError):
                parent_name = parent_name[:parent_name.index('(')]

            return parent_name + '.' + self.name

