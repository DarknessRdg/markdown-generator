from utils import (
    BaseObject, get_code_string_from_doc, get_md_string,
    is_not_hidden_folder, handle_arg
)
import os
import contextlib
import logging
import sys


SRC_FOLDER = 'example'  # name to folder where src is saved
SAVE_FOLDER = 'docs'  # name to folder where .md are going to be generated
DEFAULT_INDENTATION = 4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def is_python_file(file_name):
    return file_name.endswith('.py') and file_name != '__init__.py'


def get_object_doc(file, index):
    """
    Get a object's docstring
    Args:
        file: list with file rows
        index: line index witch starts function
    Returns:
        tuple(index, docstring):
            index: last line with docstring
            docstring: String with with object's docstring
    """
    docstring_delimiter = '"""'
    if not file or docstring_delimiter not in file[index + 1]:
        return 0, ''

    index += 1
    docstring_lines = ['']
    line = file[index]

    cont_delimiters = 0
    if cont_delimiters == 2:  # docstring inline, ex: """docs"""
        docstring_lines.append(line.replace('"""', ''))

    while cont_delimiters < 2:
        line = file[index].strip() + '\n'
        cont_delimiters += line.count(docstring_delimiter)

        subtitles = ['Args:', 'Returns:', 'Yields:', 'Attributes:', 'Raises:']
        for sub in subtitles:
            if sub in line:
                line = '\n{}\n'.format(line)
                break

        if '```' in line:
            index, line = get_code_string_from_doc(file, index)

        docstring_lines.append(line)
        index += 1

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

        new_object = BaseObject(object_name, last_added, current_indent)
        index, docstring = get_object_doc(file, current_line)
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


def generate_python_md(file_path, file_name, folder=''):
    """
    Function to generate a markdown from a python file
    Args:
        file_path: path to .py analysed
        file_name: file's like file_name.py
        folder: string with target folder name to save
    """
    logging.info('Generating .md from python files fom file: ' + file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()
        logging.debug(f'File lines: {file_lines}')

    if file_lines and file_lines[0].startswith('#!'):
        start = 0
    else:
        start = -1
    index, file_docstring = get_object_doc(file_lines, start)
    parsed = parse_python_file(file_lines)

    file_name = file_name.replace('.py', '.md')
    save_folder_dir = os.path.join(BASE_DIR, SAVE_FOLDER, folder)
    path = os.path.join(save_folder_dir, file_name)

    logging.debug(f'Folder path to save: {save_folder_dir}')
    with contextlib.suppress(FileExistsError):
        os.makedirs(save_folder_dir)
    wrote_something = False

    parsed.sort(key=lambda obj: obj.name)
    logging.debug(f'File path to save: {path}')
    with open(path, 'w+') as output_file:
        if file_docstring:
            output_file.write(file_docstring + '\n\n')
        for object_parsed in parsed:
            string = get_md_string(object_parsed)
            if string:
                wrote_something = True
            output_file.write(string)
    if not wrote_something:
        os.remove(path)
        logging.debug(f'Nothing wrote on file: {path}')

        if not os.listdir(save_folder_dir):
            os.rmdir(save_folder_dir)
            logging.debug(f'Delete empty folder: {save_folder_dir}')


def generate_from_folder(folder_path, folder_name):
    """
    Function to generate .md from all .py file inside a folder
    Args:
        folder_path: string with absolute path to folder
        folder_name: string with folder's name
    """

    logging.info('Generating all .md from file inside folder ' + folder_name)
    for file_name in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, file_name)
        if is_python_file(file_name):
            generate_python_md(path, file_name, folder_name)
        elif is_not_hidden_folder(file_name):
            sub_paste_path = os.path.join(folder_name, file_name)

            generate_from_folder(path, sub_paste_path)


def generate():
    """Main function to generate .md files from python files"""
    files_path = os.path.join(BASE_DIR, SRC_FOLDER)
    generate_from_folder(files_path, '')


if __name__ == '__main__':
    sys.argv.pop(0)
    if sys.argv:
        handle_arg(sys.argv[0])
    generate()
