"""levendist — string distance metrics."""
from __future__ import annotations

from typing import Tuple

__all__ = ["LevenDistError", "damerau_levenshtein", "hamming", "jaro", "jaro_winkler", "lcs", "levenshtein", "similarity"]
__version__ = "0.1.0"


class LevenDistError(ValueError):
    """Raised on invalid input."""


def _require_str(*args):
    for a in args:
        if not isinstance(a, str):
            raise LevenDistError(f"argument must be str, got {type(a).__name__}")


def levenshtein(a: str, b: str) -> int:
    """Standard Levenshtein edit distance (insertions, deletions, substitutions)."""
    _require_str(a, b)
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    if len(a) > len(b):
        a, b = b, a
    prev = list(range(len(a) + 1))
    for j, cb in enumerate(b, 1):
        cur = [j]
        for i, ca in enumerate(a, 1):
            cost = 0 if ca == cb else 1
            cur.append(min(cur[-1] + 1, prev[i] + 1, prev[i-1] + cost))
        prev = cur
    return prev[-1]


def damerau_levenshtein(a: str, b: str) -> int:
    """Damerau-Levenshtein with adjacent transposition."""
    _require_str(a, b)
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if not la:
        return lb
    if not lb:
        return la
    d = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la+1):
        d[i][0] = i
    for j in range(lb+1):
        d[0][j] = j
    for i in range(1, la+1):
        for j in range(1, lb+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + cost)
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2] + 1)
    return d[la][lb]


def hamming(a: str, b: str) -> int:
    """Hamming distance — strings must be equal length."""
    _require_str(a, b)
    if len(a) != len(b):
        raise LevenDistError(f"hamming requires equal-length strings, got {len(a)} vs {len(b)}")
    return sum(1 for ca, cb in zip(a, b) if ca != cb)


def jaro(a: str, b: str) -> float:
    """Jaro similarity in [0.0, 1.0]."""
    _require_str(a, b)
    if a == b:
        return 1.0 if a else 0.0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 0.0
    match_distance = max(la, lb) // 2 - 1
    a_matches = [False] * la
    b_matches = [False] * lb
    matches = 0
    for i in range(la):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, lb)
        for j in range(start, end):
            if b_matches[j] or a[i] != b[j]:
                continue
            a_matches[i] = True
            b_matches[j] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    transpositions = 0
    k = 0
    for i in range(la):
        if not a_matches[i]:
            continue
        while not b_matches[k]:
            k += 1
        if a[i] != b[k]:
            transpositions += 1
        k += 1
    return (matches / la + matches / lb + (matches - transpositions/2) / matches) / 3


def jaro_winkler(a: str, b: str, *, prefix_scale: float = 0.1, max_prefix: int = 4) -> float:
    """Jaro-Winkler with common-prefix bonus."""
    _require_str(a, b)
    if not isinstance(prefix_scale, (int, float)) or not 0 <= prefix_scale <= 0.25:
        raise LevenDistError("prefix_scale must be in [0, 0.25]")
    j = jaro(a, b)
    prefix = 0
    for i in range(min(len(a), len(b), max_prefix)):
        if a[i] == b[i]:
            prefix += 1
        else:
            break
    return j + prefix * prefix_scale * (1 - j)


def lcs(a: str, b: str) -> int:
    """Longest common subsequence length."""
    _require_str(a, b)
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 0
    if la < lb:
        a, b = b, a
        la, lb = lb, la
    prev = [0] * (lb + 1)
    for i in range(1, la + 1):
        cur = [0]
        for j in range(1, lb + 1):
            if a[i-1] == b[j-1]:
                cur.append(prev[j-1] + 1)
            else:
                cur.append(max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def similarity(a: str, b: str) -> float:
    """Levenshtein-based similarity in [0.0, 1.0]: 1 - dist/max_len."""
    _require_str(a, b)
    m = max(len(a), len(b))
    if m == 0:
        return 1.0
    return 1.0 - levenshtein(a, b) / m
