# Generate makdown from .py files

Script to generate makdown files from python files.


## How to use

Paste file `generate.py` on project's **src folder** and change the following global variables:

- `SRC_FOLDER`: folder with target files to generate `.md` files. Use blank string `""` if wants folder the script is pasted.
- `SAVE_FOLDER`: folder target to save generated `.md` files.
- `DEFAULT_INDENTATION`: Integer with number of spaces used to indent python on `.py` files.

After changed, run the script from terminal command:

```bash
python3 generate.py
```

### How it works

The script _generate_ will create the markdown files from all python files inside the folder and sub folders. The Output folder
will have with same structure as the folder target with python files.

i.e:

Look ate the directory structure:
```
- core
   - file.py
   - tests
        - test_1.py
```

The Otput will be:

```       
- core
   - file.md
   - test
        - test_1.md
```

### List of Arguments
It is possible to give some arguments to script

Arg   | Explanation
--------- | ------
-v | show warning loggs
-vv | show warning and info loggs
-vvv | show all loggs: warning, info de debug
