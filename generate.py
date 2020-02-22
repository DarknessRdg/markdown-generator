import os
import utils.classes

SRC_FOLDER = 'example'
DEFAULT_INDENTATION = 4


def is_python_file(file_name):
    return file_name.endswith('.py') and file_name != '__init__.py'


def is_not_hidden_folder(file_name):
    return len(file_name.split('.')) == 1 and file_name != 'venv'


def get_object_doc(file, index, current_indentation=None):
    """
    Get a object's docstring
    Args:
        file: list with file rows
        index: line index witch starts docstring
        current_indentation: string with current indentation 
    """
    if current_indentation is None:
        current_indentation = ' ' * DEFAULT_INDENTATION
    docstring_lines = ['']

    line = file[index]

    is_in_docstring = '"""' in line
    while is_in_docstring:
        line = line.replace(current_indentation, '')
        docstring_lines.append(line)

        if '"""' in line:
            is_in_docstring = False
        index += 1
    return index, ''.join(docstring_lines)


def clean_object_name(line):
    line = line.strip()
    try:
        key = 'class '
        line = line.replace('self, ', '').replace('self,', '').replace('self', '')
        index = line.index(key) + len(key)
    except ValueError:
        key = 'def '
        index = line.index(key) + len(key)

    line = line[index:len(line) - 1]
    print(line)
    return line


def get_indent(line):
    cont, i = 0, 0
    while i < len(line) and line[i] == ' ':
        cont += 1
        i += 1
    # print(line, cont)
    return cont // DEFAULT_INDENTATION


def parse_python_file(file, current_line=0, current_indent=0, last_added=None, data=None):
    """"
    Function to read file and get class/functions/method and save in a class
    Args:
        file: list with all rows from file
        current_line: current line analysed
        current_indent: current ident size like 0, 1, 2 tabs
        last_added: last object added
        data: list with all objects already parsed
    """
    if data is None:
        data = []
    if current_line >= len(file):
        return data
    line = file[current_line]

    indent = ' ' * (current_indent * DEFAULT_INDENTATION)

    if line.strip().startswith('class ') or line.strip().startswith('def '):
        current_indent = get_indent(line)
        object_name = clean_object_name(line)

        new_object = utils.classes.BaseObject(object_name, last_added, current_indent)
        index, docstring = get_object_doc(file, current_line, indent)
        new_object.doc = docstring

        if current_indent == 0:  # no indentation
            data.append(new_object)
        else:  # has indentation, so it is a nested object
            if current_indent > last_added.indent:  # indentation forward
                last_added.children.append(new_object)
            else:  # indentation back
                parent = last_added
                while parent.indent >= current_indent:  # get parent
                    parent = parent.parent
                parent.children.append(new_object)

        last_added = new_object

    parse_python_file(file, current_line + 1, current_indent, last_added, data)

    return data


def generate_python_md(file_path):
    """Function to generate a markdown from a python file"""
    with open(file_path, 'r') as file:
        file_lines = [line for line in file]
    parsed = parse_python_file(file_lines)



def generate():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    files_path = '%s/%s/' % (base_dir, SRC_FOLDER)
    for file_name in sorted(os.listdir(files_path)):

        if is_python_file(file_name):
            path = files_path + '/%s' % file_name
            generate_python_md(path)


if __name__ == '__main__':
    generate()
