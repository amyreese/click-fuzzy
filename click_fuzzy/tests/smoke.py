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
        self.assertEqual(result.exit_code, 0)

    def test_direct(self) -> None:
        result = self.runner.invoke(main, ["hello", "cutie"], catch_exceptions=False)
        self.assertEqual("hello cutie\n", result.stdout)
        self.assertEqual("", result.stderr)
        self.assertEqual(result.exit_code, 0)

    def test_ambiguous_prefix(self) -> None:
        result = self.runner.invoke(main, ["h"], catch_exceptions=False)
        self.assertIn("Error: 'h' is not a command", result.stderr)
        self.assertIn("Similar commands:\n  hello\n  howdy", result.stderr)
        self.assertEqual(result.exit_code, 2)

    def test_definitive_prefix(self) -> None:
        with self.subTest("he"):
            result = self.runner.invoke(main, ["he", "cutie"], catch_exceptions=False)
            self.assertIn("Warning: Assuming 'he' is short for 'hello'", result.stderr)
            self.assertIn("hello cutie", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("how"):
            result = self.runner.invoke(main, ["how"], catch_exceptions=False)
            self.assertIn("Warning: Assuming 'how' is short for 'howdy'", result.stderr)
            self.assertIn("howdy partner", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("b"):
            result = self.runner.invoke(main, ["b"], catch_exceptions=False)
            self.assertIn("Warning: Assuming 'b' is short for 'bonjour'", result.stderr)
            self.assertIn("bonjour mon ami", result.stdout)
            self.assertEqual(result.exit_code, 0)

    def test_misspelling(self) -> None:
        with self.subTest("helo"):
            result = self.runner.invoke(
                main, ["helo", "mother"], catch_exceptions=False
            )
            self.assertIn(
                "Warning: Assuming 'helo' is slang for 'hello'", result.stderr
            )
            self.assertIn("hello mother", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("helol"):
            result = self.runner.invoke(
                main, ["helol", "father"], catch_exceptions=False
            )
            self.assertIn(
                "Warning: Assuming 'helol' is slang for 'hello'", result.stderr
            )
            self.assertIn("hello father", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("rowdy"):
            result = self.runner.invoke(main, ["rowdy"], catch_exceptions=False)
            self.assertIn(
                "Warning: Assuming 'rowdy' is slang for 'howdy'", result.stderr
            )
            self.assertIn("howdy partner", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("bonjourno"):
            result = self.runner.invoke(main, ["bonjourno"], catch_exceptions=False)
            self.assertIn(
                "Warning: Assuming 'bonjourno' is slang for 'bonjour'", result.stderr
            )
            self.assertIn("bonjour mon ami", result.stdout)
            self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    main()
