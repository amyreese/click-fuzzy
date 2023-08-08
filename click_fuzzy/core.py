# Copyright Amethyst Reese
# Licensed under the MIT license

from gettext import gettext
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple
from warnings import warn

import click
import editdistance
from click.decorators import FC


class DuplicateAliasWarning(Warning):
    pass


class IgnoredAliasWarning(Warning):
    pass


class AliasedCommandGroup(click.Group):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.aliases: Dict[str, click.Command] = {}

    def alias(self, *names: str) -> Callable[[FC], FC]:
        def decorator(f: FC) -> FC:
            if not hasattr(f, "__click_aliases__"):
                f.__click_aliases__ = []  # type: ignore
            for name in names:
                if isinstance(name, str):
                    f.__click_aliases__.append(name)  # type: ignore
                else:
                    raise ValueError(b"aliases must be strings ({name=!r})")
            return f

        return decorator

    def add_command(self, cmd: click.Command, name: Optional[str] = None) -> None:
        callback = cmd.callback
        name = name or cmd.name

        for alias in getattr(callback, "__click_aliases__", ()):
            if alias in self.commands:
                warn(
                    f"Ignoring {name!r} alias {alias!r}, "
                    "command with same name already defined",
                    IgnoredAliasWarning,
                    stacklevel=3,
                )
            elif alias in self.aliases:
                other = self.aliases[alias]
                warn(
                    f"Duplicate alias {alias!r} already defined for {other}",
                    DuplicateAliasWarning,
                    stacklevel=3,
                )
            else:
                self.aliases[alias] = cmd

        return super().add_command(cmd, name)

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        if cmd_name in self.commands:
            return self.commands[cmd_name]

        if cmd_name in self.aliases:
            return self.aliases[cmd_name]

        return super().get_command(ctx, cmd_name)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            aliases = [a for a, c in self.aliases.items() if c == cmd]
            subcommand = ", ".join([subcommand] + sorted(aliases))
            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section(gettext("Commands")):
                    formatter.write_dl(rows)


class FuzzyCommandGroup(AliasedCommandGroup):
    WARN_ON_PREFIX_MATCH: bool = False
    WARN_ON_FUZZY_MATCH: bool = True

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        if name in self.commands:
            return self.commands[name]

        if name in self.aliases:
            return self.aliases[name]

        commands = sorted(
            (name, cmd)
            for name, cmd in chain(self.commands.items(), self.aliases.items())
        )
        prefixes = [(n, c) for n, c in commands if n.startswith(name)]

        if len(prefixes) == 1:
            n, cmd = prefixes[0]
            if self.WARN_ON_PREFIX_MATCH:
                click.echo(f"Warning: Assuming {name!r} is short for {n!r}", err=True)
            return cmd

        elif prefixes:
            click.echo(
                f"Error: {name!r} is not a command. See --help\n\n" "Similar commands:",
                err=True,
            )
            for n, _ in prefixes:
                click.echo(f"  {n}", err=True)
            ctx.exit(2)

        distances = sorted((editdistance.eval(name, n), n, c) for n, c in commands)
        candidates = [(d, n, c) for d, n, c in distances if d <= 2]

        if len(candidates) == 1:
            _, n, cmd = candidates[0]
            if self.WARN_ON_FUZZY_MATCH:
                click.echo(f"Warning: Assuming {name!r} is slang for {n!r}", err=True)
            return cmd

        click.echo(
            f"Error: {name!r} is not a command. See --help\n\n" "Similar commands:",
            err=True,
        )
        for d, n, cmd in distances[:6]:
            click.echo(f"  {n} ({d})", err=True)
        ctx.exit(2)

    def resolve_command(
        self, ctx: click.Context, args: List[str]
    ) -> Tuple[Optional[str], Optional[click.Command], List[str]]:
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        return cmd.name if cmd else cmd_name, cmd, args
