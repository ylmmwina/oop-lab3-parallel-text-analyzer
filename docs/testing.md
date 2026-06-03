# Testing Strategy

This document describes the testing approach for Parallel Text Analyzer.

## Testing Framework

The project uses:

    pytest

Run all tests:

    python -m pytest

## Tested Components

| Test File | Component |
|---|---|
| tests/test_analyzer.py | Single-file text analysis |
| tests/test_processors.py | Sequential and parallel processors |
| tests/test_benchmark.py | Benchmark runner and CSV output |

## Correct Input Tests

The tests verify that the analyzer correctly handles valid .txt files.

Checked values include:

- file count;
- line count;
- word count;
- character count;
- word frequencies.

## Incorrect Input Tests

The tests also check invalid input cases:

- missing file;
- unsupported file extension;
- directory instead of file;
- empty file list;
- invalid worker count;
- empty benchmark dataset.

## Sequential vs Parallel Comparison

The tests verify that:

    SequentialTextProcessor result == ParallelTextProcessor result

The comparison includes:

- file count;
- line count;
- word count;
- character count;
- word frequencies.

## Different Thread Counts

The tests also check that parallel processing produces the same result with different worker counts:

    1
    2
    4

## Benchmark Tests

Benchmark tests check that:

- benchmark rows are created;
- CSV output is saved;
- empty datasets are rejected.

## GUI Testing

Automated GUI tests are not included.

The GUI is tested manually by running:

    python app/main.py

Manual GUI checks:

1. select a folder with .txt files;
2. run comparison;
3. verify that the interface stays responsive;
4. verify that the output contains Results equal: True.

## Conclusion

The tests cover the core functionality required for Lab 3:

- correct data processing;
- invalid input handling;
- sequential and parallel result comparison;
- benchmark CSV generation.
