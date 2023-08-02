# Copyright Amethyst Reese
# Licensed under the MIT license

import click
import editdistance


class FuzzyCommandGroup(click.Group):
    def get_command(self, ctx: click.Context, name: str) -> click.Command | None:
        if name in self.commands:
            return self.commands[name]

        prefixes = [c for c in self.commands if c.startswith(name)]

        if len(prefixes) == 1:
            cmd = prefixes[0]
            click.echo(f"WARNING: Assuming {name!r} is short for {cmd!r}")
            return self.commands[cmd]

        elif prefixes:
            click.echo(
                f"{ctx.info_name}: {name!r} is not a command. See --help\n\n"
                "Similar commands:",
                err=True,
            )
            for cmd in prefixes:
                click.echo(f"  {cmd}", err=True)
            ctx.exit(2)

        distances = sorted((editdistance.eval(name, c), c) for c in self.commands)
        candidates = [(d, c) for d, c in distances if d <= 2]

        if len(candidates) == 1:
            _, cmd = candidates[0]
            click.echo(f"WARNING: Assuming {name!r} is slang for {cmd!r}")
            return self.commands[cmd]

        elif candidates:
            click.echo(
                f"{ctx.info_name}: {name!r} is not a command. See --help\n\n"
                "Similar commands:",
                err=True,
            )
            for _, cmd in candidates:
                click.echo(f"  {cmd}", err=True)
            ctx.exit(2)

        return None

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        return cmd.name if cmd else cmd_name, cmd, args