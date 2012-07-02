# CSV Profiler Lab

Describe a small CSV dataset: row counts, missing cells, distinct nonempty values, decimal counts, and maximum cell length.

This original small project uses **Python 3.10+ and only its standard library**.
No packages, virtual environment, service, or network access are required.

## Run

From this repository directory:

```console
python csv_profiler.py --help
python csv_profiler.py examples/sample.csv
python csv_profiler.py --check-fixtures fixtures/cases.jsonl
python -m unittest discover -s tests -v
```

Headers are trimmed and must be nonempty and unique. Cells are trimmed before profiling; distinct counts exclude empty cells. Decimal counts accept signed plain decimal notation, not exponents, NaN, or Infinity. Quoted commas and newlines use standard CSV rules. --delimiter accepts one non-newline character. The tool loads small inputs into memory; it is not a streaming analytics engine.

Output is JSON (or a fixture-check summary). Exit codes are 0 for success,
1 for file failures, and 2 for invalid input. Errors go to stderr.
For file-based tools, `-` reads stdin. Use UTF-8 input files.

## Structure and branches

- `csv_profiler_lab/core.py`: pure parsing or analysis logic.
- `csv_profiler_lab/cli.py`: command arguments and file input/output.
- `csv_profiler_lab/generate_fixtures.py`: deterministic original sample cases.
- `csv_profiler_lab/fixture_check.py`: expected-result/error validation.
- `fixtures/cases.jsonl`: 367 synthetic cases, one added per artificial dated commit.
- `tests/`: independently chosen boundary cases plus corpus validation.

`feature/core` and `feature/cli` retain the corresponding development snapshots.
`data/synthetic-fixtures` marks the completed corpus; `docs/usage` and `main` contain
the final documentation and tests. There are no copied upstream commits.

## Generate examples

```console
python generate_fixtures.py --count 20
```

This prints reproducible JSONL and **does not create or date Git commits**. The
historical-looking Git timeline is a separate, documented simulation. Many cases
vary generated values; they do not imply separate design decisions or features.

Keep contributions focused, add a regression test for changed behavior, and run
the standard-library tests. Never add real private data or credentials. Record
actual dates for new work. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
