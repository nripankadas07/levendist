"""levendist — string distance metrics."""

from __future__ import annotations

from ._core import (
    LevenDistError,
    damerau_levenshtein,
    hamming,
    jaro,
    jaro_winkler,
    lcs,
    levenshtein,
    similarity,
)

__all__ = [
    "LevenDistError",
    "damerau_levenshtein",
    "hamming",
    "jaro",
    "jaro_winkler",
    "lcs",
    "levenshtein",
    "similarity",
]
__version__ = "0.1.0"
