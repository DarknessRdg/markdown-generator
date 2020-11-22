import contextlib
import logging
import pathlib
import os
import re
import sys

# Relative path to BASE_DIR where code to be
# generated are stored
SRC_FOLDER = 'example'

# Relative path to BASE_DIR where all output `.md` files
# should be created
SAVE_FOLDER = 'docs'

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

# Language reserved word that can have a docstring
# like class, function or method
LANGUAGE_KEYWORDS = [
    'class',
    'def',
]


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


class TypeOfObject:
    CLASS = 1
    METHOD = 2
    FUNCTION = 3


class Object(object):
    def __init__(self, line, docstring, parent=None, indent=0):
        line = line.strip()
        self.parent = parent
        self.docstring = docstring
        self.indent = indent

        self.token = self._get_token(line)
        self._name = self._get_name(line)

    def _get_token(self, line):
        return line.split()[0]

    def _get_name(self, line):
        end = len(line)
        start = line.index(' ') + 1

        with contextlib.suppress(ValueError):
            end_token = ')' if ')' in line else ':'
            end = line.index(end_token)

            if end_token == ')':
                end += 1

        line = line[start:end]
        if self.type == TypeOfObject.METHOD:
            with contextlib.suppress(ValueError):
                _self = 'self'
                self_start = line.index(_self)
                self_end = self_start + len(_self)

                while self_start > 0 and line[self_start-1] == ' ':
                    self_start -= 1
                while self_end < len(line)-1 and line[self_end+1] in (',', ' '):
                    self_end += 1

                line = list(line)
                for index in range(self_start, self_end+1):
                    line.pop(self_start)
                line = ''.join(line)

        return line

    @property
    def type(self):
        if self.token == 'class':
            return TypeOfObject.CLASS
        else:
            parent = self.parent
            while parent is not None and parent.token != 'class':
                parent = parent.parent

            if parent is not None:
                return TypeOfObject.METHOD
            return TypeOfObject.FUNCTION

    @property
    def name(self):
        parent_name = ''
        if self.parent:
            parent_name = self.parent.name

            parent_name = parent_name.split('.')
            for index in range(len(parent_name)):
                _name = parent_name[index]
                with contextlib.suppress(ValueError):
                    _name = _name[:_name.index('(')]
                    parent_name[index] = _name

            parent_name = '.'.join(parent_name) + '.'

        return parent_name + self._name

    def __str__(self):
        return '### %s %s' % (self.token, self.name)

    def __eq__(self, other):
        if isinstance(other, Object):
            _self = self.parent, self.name
            other = other.parent, other.name
            return _self == other
        return False

    def __repr__(self):
        return '<Object %s>' % self.name


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
        if regex.match(file_name):
            return False
    return True


def is_allowed_folder(folder_name, ignore=None):
    if ignore is None:
        ignore = IGNORE_FOLDERS

    return all([
        not regex.match(folder_name)
        for regex in map(re.compile, ignore)
    ])


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
    while not file[function_index].strip().endswith(':'):
        function_index += 1

    index = function_index + 1

    while not file[index].strip():
        index += 1

    line = file[index]

    if not line.strip().startswith(DOCSTRING):
        return range(function_index+1, function_index+1)

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

        if line.strip():
            docs.append(line)

    return '\n'.join(docs) + '\n'


def get_docstring_objects(file, index=0, parent=None):
    objects = []
    last_indent = 0 if parent is None else parent.indent

    while index < len(file):
        line = file[index]

        has_docs = any([
            line.strip().startswith(token) for token in LANGUAGE_KEYWORDS
        ])

        if has_docs:
            indent = get_indent(file, index)

            docs = get_object_docstring(file, index)
            docs_range = get_docstring_range(file, index)

            function_name = [
                file[i].strip()
                for i in range(index+1, docs_range.start)
            ]
            line += ' '.join(function_name)

            index = docs_range.stop
            while indent <= last_indent and parent is not None:
                parent = parent.parent
                if parent:
                    last_indent = parent.indent

            obj = Object(line, docs, parent, indent)
            objects.append(obj)

            if indent > last_indent:
                last_indent = indent
                nested_objects, index = get_docstring_objects(file, index, obj)
                objects += nested_objects

                if not nested_objects:  # roll back to current line
                    index -= 1
            elif indent < last_indent:
                return objects, index

        index += 1

    return objects, index


def objects_to_markdown(objects) -> str:
    md_lines = []
    for obj in objects:
        if obj.docstring:
            md_lines.append('%s\n' % str(obj))
            md_lines.append(obj.docstring)
    return '\n'.join(md_lines)


def convert_path_to_posix(path):
    return pathlib.Path(path).as_posix()


def create_file_markdown(file_path, folder_path):
    posix_path = convert_path_to_posix(file_path)
    logging.info('creating markdown for file %s' % posix_path)
    with open(file_path) as file_read:
        file = list(map(str.strip, file_read.readlines()))

    file_objects, _ = get_docstring_objects(file, 0)

    file_name = posix_path.split('/')[-1]
    md_name = file_name.replace('.%s' % FILE_EXTENSION, '.md')
    save_path = os.path.join(BASE_DIR, folder_path, md_name)
    with open(save_path, 'w') as file_write:
        file_write.write(objects_to_markdown(file_objects))


def create_folder_files_markdown(path, relative_save_path):
    def sort_files(entry):
        return entry.name

    posix_path = convert_path_to_posix(path)
    current_folder_name = posix_path.split('/')[-1]
    if not is_allowed_folder(current_folder_name):
        return

    logging.info('creating markdown for folder %s' % posix_path)
    for path_entry in sorted(os.scandir(path), key=sort_files):

        if path_entry.is_file() and is_allowed_files(path_entry.name):
            create_file_markdown(path_entry.path, relative_save_path)

        elif path_entry.is_dir():
            create_folder_files_markdown(
                path_entry.path,
                os.path.join(relative_save_path, path_entry.name)
            )


def main():
    """Main function to generate .md files from python files"""
    files_path = os.path.join(BASE_DIR, SRC_FOLDER)
    create_folder_files_markdown(files_path, SAVE_FOLDER)


def handle_arg(arg):
    """
    Function to handle what happens with args passed thought terminal
    Args:`
        arg: String with arg passed
    """
    levels = {
        '-v': logging.WARNING,
        '-vv': logging.INFO,
        '-vvv': logging.DEBUG
    }

    try:
        logging.basicConfig(
            level=levels[arg],
            format='%(name)-5s %(levelname)-8s %(message)s'
        )
    except KeyError:
        raise ValueError(
            'Argument invalid. The options are : %s'
            % str(list(levels.keys()))
        )


if __name__ == '__main__':
    sys.argv.pop(0)
    if sys.argv:
        pass
        handle_arg(sys.argv[0])
    main()
