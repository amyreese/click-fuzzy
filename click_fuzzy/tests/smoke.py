# Copyright Amethyst Reese
# Licensed under the MIT license


from unittest import TestCase

import click
import click.testing

from click_fuzzy import FuzzyCommandGroup


@click.group(cls=FuzzyCommandGroup)
@click.version_option("1.2.3")
@click.pass_context
def main(ctx: click.Context) -> None:
    pass


@main.command("hello")
@click.argument("name", type=str)
def hello(name: str) -> None:
    click.echo(f"hello {name}")


@main.command("howdy")
def howdy() -> None:
    click.echo("howdy partner")


@main.command("bonjour")
def bonjour() -> None:
    click.echo("bonjour mon ami")


class SmokeTest(TestCase):
    def setUp(self) -> None:
        self.runner = click.testing.CliRunner(mix_stderr=False)

    def test_version(self) -> None:
        result = self.runner.invoke(main, "--version", catch_exceptions=False)
        self.assertIn("version 1.2.3", result.stdout)
        self.assertEqual("", result.stderr)

    def test_direct(self) -> None:
        result = self.runner.invoke(main, ["hello", "cutie"], catch_exceptions=False)
        self.assertEqual("hello cutie\n", result.stdout)
        self.assertEqual("", result.stderr)


if __name__ == "__main__":
    main()
