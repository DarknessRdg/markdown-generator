import os
import utils.classes
import contextlib


SRC_FOLDER = 'example'  # name to folder where src is saved
SAVE_FOLDER = 'docs'  # name to folder where .md are going to be generated
DEFAULT_INDENTATION = 4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def is_python_file(file_name):
    return file_name.endswith('.py') and file_name != '__init__.py'


def is_not_hidden_folder(file_name):
    return len(file_name.split('.')) == 1 and file_name != 'venv'


def get_object_doc(file, index, current_indentation=None):
    """
    Get a object's docstring
    Args:
        file: list with file rows
        index: line index witch starts function
        current_indentation: int with current indentation level ex: 1, 2
    Returns:
        tuple with:
            index: last line with docstring
            docstring: String with with object's docstring
    """
    docstring_delimiter = '"""'
    index += 1
    remove = current_indentation * DEFAULT_INDENTATION

    docstring_lines = ['']
    line = file[index]

    cont_delimiters = line.count(docstring_delimiter)
    if cont_delimiters == 2:  # docstring inline, ex: """docs"""
        docstring_lines.append(line.replace('"""', ''))

    while 0 < cont_delimiters < 2:
        line = line[remove:]
        line = line.strip() + '\n'

        subtitles = ['**Args:**', '**Returns:**', '**Yields:**']
        line_lower = line.lower()
        for sub in subtitles:
            if sub.lower() in line_lower:
                line += '\n'
                break

        docstring_lines.append(line)
        index += 1
        line = file[index]
        cont_delimiters += line.count(docstring_delimiter)

    docstring = ''.join(docstring_lines)
    docstring = docstring.strip().replace(docstring_delimiter, '')  # clear possible trashes

    return index, docstring


def clean_object_name(line):
    """
    Function to clean an object name
    Args:
        line: String with object name read from file
    Returns:
        String with name cleaned
    """
    line = line.strip()
    try:
        key = 'class '
        line = line.replace('self, ', '').replace('self,', '').replace('self', '')
        index = line.index(key) + len(key)
    except ValueError:
        key = 'def '
        index = line.index(key) + len(key)

    line = line[index:len(line) - 1]
    return line


def get_indent(line):
    """
    Function to get current line indentation
    Args:
        line: String with line not striped
    Returns:
        Integer with current indentation level (0, 1, 2, ...)
    """
    cont, i = 0, 0
    while i < len(line) and line[i] == ' ':
        cont += 1
        i += 1
    return cont // DEFAULT_INDENTATION


def parse_python_file(file, current_line=0, current_indent=0, last_added=None, data=None):
    """"
    Function to read file and get class/functions/method and save in a class
    Args:
        file: list with all rows from file
        current_line: current line analysed
        current_indent: current ident size like 0, 1, 2 tabs
        last_added: last object added (used on recursion)
        data: list with all objects already parsed (used on recursion)
    Returns:
        List() with all objects data parsed
    """
    if current_line == 0:
        data = []
    if current_line >= len(file):
        return data
    line = file[current_line]

    if line.strip().startswith('class ') or line.strip().startswith('def '):
        current_indent = get_indent(line)
        object_name = clean_object_name(line)

        new_object = utils.classes.BaseObject(object_name, last_added, current_indent)
        index, docstring = get_object_doc(file, current_line, current_indent)
        new_object.doc = docstring

        if current_indent == 0:  # no indentation
            data.append(new_object)
        else:  # has indentation, so it is a nested object
            if current_indent > last_added.indent:  # indentation forward
                last_added.children.append(new_object)
            else:  # indentation back or same
                parent = last_added
                while parent.indent >= current_indent:  # get parent
                    parent = parent.parent
                parent.children.append(new_object)
                new_object.parent = parent
        last_added = new_object

    parse_python_file(file, current_line + 1, current_indent, last_added, data)

    return data


def get_md_string(object_parsed):
    """
    Function to generate a string with markdown from an object already parsed
    Args:
        object_parsed: ultis.classes.BaseObject() already parsed
    Returns:
        String with objects markdown
    """
    if object_parsed.name.startswith('__') or not object_parsed.doc:
        return ''
    title = object_parsed.get_md_title()
    string = '### {}\n'.format(title)
    string += object_parsed.doc + '\n\n'

    object_parsed.children.sort(key=lambda obj: obj.name)
    for children in object_parsed.children:
        string += get_md_string(children)
    return string


def generate_python_md(file_path, file_name, folder=''):
    """Function to generate a markdown from a python file"""
    with open(file_path, 'r') as file:
        file_lines = [line for line in file]
    index, file_docstring = get_object_doc(file_lines, -1, 0)
    parsed = parse_python_file(file_lines)

    file_name = file_name.replace('.py', '.md')
    save_folder_dir = os.path.join(BASE_DIR, SAVE_FOLDER, folder)
    path = os.path.join(save_folder_dir, file_name)

    with contextlib.suppress(FileExistsError):
        os.makedirs(save_folder_dir)

    parsed.sort(key=lambda obj: obj.name)
    with open(path, 'w+') as output_file:
        output_file.write(file_docstring)
        for object_parsed in parsed:
            string = get_md_string(object_parsed)
            output_file.write(string)


def generate():
    """Main function to generate .md files from python files"""
    files_path = os.path.join(BASE_DIR, SRC_FOLDER)
    for file_name in sorted(os.listdir(files_path)):
        if is_python_file(file_name):
            path = os.path.join(files_path, file_name)
            generate_python_md(path, file_name)


if __name__ == '__main__':
    generate()
