# levendist

Zero-dependency string distance metrics for Python: Levenshtein, Damerau-Levenshtein, Hamming, Jaro, Jaro-Winkler, Longest-Common-Subsequence.

## Install

```bash
python -m pip install -e .
```

Requires Python 3.10+. No runtime dependencies.

## Quick example

```python
from levendist import (
    levenshtein, damerau_levenshtein,
    hamming, jaro, jaro_winkler, lcs, similarity,
)

levenshtein("kitten", "sitting")           # 3
damerau_levenshtein("ca", "ac")            # 1 (transposition)
hamming("karolin", "kathrin")              # 3 (length must match)
jaro("MARTHA", "MARHTA")                   # ~0.944
jaro_winkler("DWAYNE", "DUANE")            # ~0.84
lcs("ABCBDAB", "BDCAB")                    # 4
similarity("hello", "hallo")               # 0.8
```

## API

### `levenshtein(a, b) -> int`
Classic edit distance.

### `damerau_levenshtein(a, b) -> int`
Levenshtein + adjacent transposition.

### `hamming(a, b) -> int`
Hamming distance (raises if lengths differ).

### `jaro(a, b) -> float`
Jaro similarity in `[0.0, 1.0]`.

### `jaro_winkler(a, b, *, prefix_scale=0.1, max_prefix=4) -> float`
Jaro with common-prefix bonus.

### `lcs(a, b) -> int`
Longest common subsequence length.

### `similarity(a, b) -> float`
Levenshtein-based similarity, `1 - dist/max_len`.

### `LevenDistError`
Subclass of `ValueError`.

## License

MIT
