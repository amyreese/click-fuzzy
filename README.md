# Fuzzy Commands for Click

Fuzzy command matching and aliases for click

[![version](https://img.shields.io/pypi/v/click-fuzzy.svg)](https://pypi.org/project/click-fuzzy)
[![license](https://img.shields.io/pypi/l/click-fuzzy.svg)](https://github.com/amyreese/click-fuzzy/blob/main/LICENSE)


Allows use of automatic prefix aliases and matching small typos:

```shell-session
$ command h
WARNING: Assuming 'h' is short for 'hello'
Hello world!

$ command helol
WARNING: Assuming 'helol' is slang for 'hello'
Hello world!
```

Explicit aliases can also be defined:

```shell-session
$ command --help
Usage: command [OPTIONS] COMMAND [ARGS]...

Commands:
  hello, hi  The traditional greeting

$ command hi --help
Usage: command hello [OPTIONS]
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

@main.command("hello")
@main.alias("hi")
def hello():
    ...
```

That's it.  Everything else happens automatically.

If you only want explicit aliases, and don't want automatic prefix or fuzzy
matching, use `AliasedCommandGroup` instead of `FuzzyCommandGroup`:


License
-------

Fuzzy Commands is copyright Amethyst Reese, and licensed under the MIT license.