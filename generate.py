import os
import utils.classes

SRC_FOLDER = ''


def is_python_file(file_name):
    return file_name.endswith('.py') and file_name != '__init__.py'


def is_not_hidden_folder(file_name):
    return len(file_name.split('.')) == 1 and file_name != 'venv'


def parse_python_file(file):
    data = []

    for line in file:
        if 'def' in line or 'class' in line:
            data.append(
                utils.classes.Tree(utils.classes.BaseObject())
            )



def generate_python_md(file_path):
    """Function to generate a markdown from a python file"""
    with open(file_path, 'r') as file:
        file_parsed = parse_python_file(file)
        print(file_parsed)


def generate():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    files_path = '%s/%s/' % (base_dir, SRC_FOLDER)
    for file_name in sorted(os.listdir(files_path)):

        if is_python_file(file_name):
            path = files_path + '/%s' % file_name
            generate_python_md(path)


if __name__ == '__main__':
    generate()
