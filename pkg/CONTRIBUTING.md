# Contributing

Issues and pull requests are welcome at
https://github.com/foikwuogu/tsa-nist-cpg-semantic-crosswalk

## Development setup

```bash
git clone https://github.com/foikwuogu/tsa-nist-cpg-semantic-crosswalk
cd tsa-nist-cpg-semantic-crosswalk/pkg
pip install -e ".[dev]"
python -m unittest discover -s tests -v
```

## Guidelines

- Keep the scorer's design principle intact: every score must be
  reproducible from the two input CSVs alone (no network calls, no model
  downloads) — see the README's "Why TF-IDF" section before proposing an
  embedding-based scorer; that's welcome as an *additional*, opt-in mode,
  not a silent replacement.
- Add a test with a small, hand-checkable fixture for any new scoring or
  adjudication-queue logic — see `tests/fixtures/`.
- Update `CHANGELOG.md` for any user-facing change.
