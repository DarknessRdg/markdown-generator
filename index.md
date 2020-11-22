# Markdown Generator


##### What is it?


This is a script that generates a markdown for you script files. It extracts the docstrings from your classes, functions, method and even from you file docstring.

This module was designed to extract docstring from python scripts. But if you language the following rules to fit this script, than you are fine to use it:

1. Uses `(` and `)` to delimiter function declaration.
2. Uses `:` do delimiter to start function os class indented scope (important one).
3. Uses a single token to delimiter start and end of code docstring, in python: `"""` marks start and end of docstring.
4. Is an indented based language

##### How it works

This script will read your script file and look for all docstring in it.

##### What is a docstring.

Well, it is all comment in your file code that has the purpose to document your function, class, method, or file. We call it `docstring` because in python we have an especial toke for string that is used with purpose to document.

Checkout the example bellow:
```py
def my_function():
    """
    This is an string in python,
    But since it is just after function declaration,
    then this is an escpecial string, this is a: docstring
    """
    pass
``` 


### Settings

Well, let's take a look at what settings you can do to customize de generation. All the settings are in the beginning of the script. When you get you copy, you will see your the following code:

```py
SRC_FOLDER = 'example'

SAVE_FOLDER = 'docs'

FILE_EXTENSION = 'py'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORE_FOLDERS = [

]

IGNORE_FILES_NAME = [
    r'^__.*__$',  # python files
    r'^_.*',  # private files
]

DOCSTRING = '"""'

LANGUAGE_KEYWORDS = [
    'class',
    'def',
]


def clear_line(line):
    line = clear_docstring_keywords(line)
    return line
``` 

Directory settings:

- **BASE_DIR**: Full path to the project file. Default value is the *current dir* where the generator is pasted.
- **SRC_FOLDER**: Relative path to `BASE_DIR` where your source code with `.extension` files with docstring are stored. The default value is `src/` folder. If empty, source folder is same as `BASE_DIR`
- **SAVE_FOLDER**: Relative path to `BASE_DIR` where your `.md` file with code docstring are going to be stored. The default value is `docs/` folder. If empty, save folder is same as  `BASE_DIR`.
- **IGNORE_FOLDERS**: List of regex strings of *folder names* that should not generate markdown from. An example of folder you might want to ignore is your python virtualenv, commonly in `venv` folder.

File settings:

- **FILE_EXTENSION**: Name of your language script extension without dot (`.`). The default value is `py` that is the extension of python files.

