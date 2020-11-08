import contextlib
import os
import re

# Relative path to BASE_DIR where code to be
# generated are stored
SRC_FOLDER = ''

# Relative path to BASE_DIR where all output `.md` files
# should be created
SAVE_FOLDER = ''

# Default number of spaces used to ident code
INDENT = 4

# Extension name of the file should be generated.
# ATTENTION: Remember it must be an indented language extension
FILE_EXTENSION = 'py'

# Base directory to relative all other folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Regex of folders names to ignore and not generate file markdowns
IGNORE_FOLDERS = [

]

# Regex of file names to ignore and not generate file markdowns
IGNORE_FILES_NAME = [
    r'^__.*__$',  # python files
    r'^_.*',  # private files
]

# Docstring delimiter
DOCSTRING = '"""'


def clear_line(line):
    """
    Change this function in order to perform extra customization
    on line that you want it to appear on the markdown.

    Args:
        line: String that is the current line in the file being processed
            at the moment. This line can be changed as you wish.

    Returns:
        String: The new string processed to replace older string.
    """
    line = clear_docstring_keywords(line)
    return line


def clear_docstring_keywords(line):
    def black(word):
        return '\n**%s**\n\n' % word

    keywords = {
        'Args:': black,
        'Returns:': black,
        'Raises:': black
    }
    with contextlib.suppress(KeyError):
        parser = keywords[line]
        return parser(line)
    return line


def is_file(file_name, extension=FILE_EXTENSION):
    parts = file_name.split('.')
    if len(parts) == 2:
        name, file_ext = parts
        return name and file_ext == extension
    return False


def is_allowed_files(file_name, ignore=None):
    if ignore is None:
        ignore = IGNORE_FILES_NAME

    if not is_file(file_name):
        return False

    file_name, _ = file_name.split('.')

    for regex in map(re.compile, ignore):
        print(regex)
        if regex.match(file_name):
            return False
    return True


def get_indent(file, function_index):
    index = function_index + 1

    while not file[index].strip():
        index += 1

    line = file[index]

    count_white_spaces = 0
    while line[count_white_spaces] == ' ':
        count_white_spaces += 1
    return count_white_spaces


def get_docstring_range(file, function_index):
    index = function_index + 1

    while not file[index].strip():
        index += 1

    line = file[index]

    if not line.strip().startswith(DOCSTRING):
        return range(0)

    count = line.count(DOCSTRING)
    start, end = index, index
    while count == 1:
        index += 1
        line = file[index]
        count += line.count(DOCSTRING)
        end = index

    return range(start, end+1)


def get_object_docstring(file, function_index):
    docs = []
    indented_spaces = get_indent(file, function_index)

    for index in get_docstring_range(file, function_index):
        line = file[index]
        line = line[indented_spaces:]
        line = line.replace(DOCSTRING, '')

        # parse line as user wishes.
        # Read `clear_line` docstring to understand how to use it
        line = clear_line(line)

        if line:
            docs.append(line)

    return '\n'.join(docs) + '\n'
