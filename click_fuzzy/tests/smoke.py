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
@main.alias("hi")
def hello() -> None:
    """The traditional greeting"""
    click.echo("hello there")


@main.command("howdy")
def howdy() -> None:
    """Say hello the cowboy way"""
    click.echo("howdy partner")


@main.command("bonjour")
def bonjour() -> None:
    """Like you might say in French class"""
    click.echo("bonjour mon ami")


class SmokeTest(TestCase):
    def setUp(self) -> None:
        self.runner = click.testing.CliRunner(mix_stderr=False)
        FuzzyCommandGroup.WARN_ON_PREFIX_MATCH = True
        FuzzyCommandGroup.WARN_ON_FUZZY_MATCH = True

    def test_version(self) -> None:
        result = self.runner.invoke(main, "--version", catch_exceptions=False)
        self.assertIn("version 1.2.3", result.stdout)
        self.assertEqual("", result.stderr)
        self.assertEqual(result.exit_code, 0)

    def test_help(self) -> None:
        result = self.runner.invoke(main, "--help", catch_exceptions=False)
        self.assertRegex(result.stdout, r"hello, hi\s+The traditional greeting")

    def test_direct(self) -> None:
        result = self.runner.invoke(main, ["hello"], catch_exceptions=False)
        self.assertIn("hello there", result.stdout)
        self.assertEqual("", result.stderr)
        self.assertEqual(result.exit_code, 0)

    def test_ambiguous_prefix(self) -> None:
        result = self.runner.invoke(main, ["h"], catch_exceptions=False)
        self.assertIn("Error: 'h' is not a command", result.stderr)
        self.assertIn("Similar commands:\n  hello\n  hi\n  howdy", result.stderr)
        self.assertEqual(result.exit_code, 2)

    def test_definitive_prefix(self) -> None:
        with self.subTest("he"):
            result = self.runner.invoke(main, ["he"], catch_exceptions=False)
            self.assertIn("Warning: Assuming 'he' is short for 'hello'", result.stderr)
            self.assertIn("hello there", result.stdout)
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
            result = self.runner.invoke(main, ["helo"], catch_exceptions=False)
            self.assertIn(
                "Warning: Assuming 'helo' is slang for 'hello'", result.stderr
            )
            self.assertIn("hello there", result.stdout)
            self.assertEqual(result.exit_code, 0)

        with self.subTest("helol"):
            result = self.runner.invoke(main, ["helol"], catch_exceptions=False)
            self.assertIn(
                "Warning: Assuming 'helol' is slang for 'hello'", result.stderr
            )
            self.assertIn("hello there", result.stdout)
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
