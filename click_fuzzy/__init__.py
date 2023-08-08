# Copyright Amethyst Reese
# Licensed under the MIT license

"""
Fuzzy command matching and aliases for click
"""

from .__version__ import __version__
from .core import (
    AliasedCommandGroup,
    DuplicateAliasWarning,
    FuzzyCommandGroup,
    IgnoredAliasWarning,
)

__author__ = "Amethyst Reese"

__all__ = [
    "AliasedCommandGroup",
    "DuplicateAliasWarning",
    "FuzzyCommandGroup",
    "IgnoredAliasWarning",
]
