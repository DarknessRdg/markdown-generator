"""
File to generate markdown from braced laguage like C, C++, Java, PHP, JavaScript
"""
from utils import (
    handle_arg, is_not_hidden_folder
)
import logging
import sys
import os

SRC_FOLDER = 'example/brace'  # name to folder where src is saved
SAVE_FOLDER = 'docs'  # name to folder where .md are going to be generated

ALLOWED_EXTENSIONS = ('js', 'cpp', 'php')  # iterable with script file
# extensions allowed to generate markdown files.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def is_allowed_file(file_name: str):
    extension = file_name.split('.')[-1]
    return extension in ALLOWED_EXTENSIONS


def generate_file_md(file_path, file_name, folder_name):
    """
    Function to generate a markdown from a brace language file
    Args:
        file_path: path to file analysed
        file_name: file's name like file_name.cpp
        folder_name: string with target folder name to save
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        logging.info('len lines ' + str(len(lines)))


def generate_from_folder(folder_path, folder_name):
    """
    Function to generate .md from all script file inside a folder ended with extension
    inside global variable ALLOWED_EXTENSIONS.

    Args:
        folder_path: string with absolute path to folder
        folder_name: string with folder's name
    """
    logging.info('Generating all .md from file inside folder ' + (folder_name if folder_name else SRC_FOLDER))
    for file_name in sorted(os.listdir(folder_path)):
        logging.info('Current file ' + file_name)
        path = os.path.join(folder_path, file_name)
        if is_allowed_file(file_name):
            generate_file_md(path, file_name, folder_name)
        elif is_not_hidden_folder(file_name):
            sub_paste_path = os.path.join(folder_name, file_name)

            generate_from_folder(path, sub_paste_path)


def generate():
    files_path = os.path.join(BASE_DIR, SRC_FOLDER)
    generate_from_folder(files_path, '')


if __name__ == '__main__':
    sys.argv.pop(0)
    if sys.argv:
        handle_arg(sys.argv[0])
    generate()
