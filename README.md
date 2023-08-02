# Fuzzy Commands for Click

Fuzzy subcommand matching for click

[![version](https://img.shields.io/pypi/v/click-fuzzy.svg)](https://pypi.org/project/click-fuzzy)
[![license](https://img.shields.io/pypi/l/click-fuzzy.svg)](https://github.com/amyreese/click-fuzzy/blob/main/LICENSE)


Allows use of automatic short aliases and matching small typos:

```shell-session
$ command h
WARNING: Assuming 'h' is short for 'hello'
Hello world!

$ command helol
WARNING: Assuming 'helol' is slang for 'hello'
Hello world!
```


Install
-------

```shell-session
$ pip install click-fuzzy
```


Usage
-----

```py
from click_fuzzy import FuzzyCommandGroup

@click.group(cls=FuzzyCommandGroup)
def main(...):
    ...
```

That's it.


License
-------

Fuzzy Commands is copyright Amethyst Reese, and licensed under the MIT license.