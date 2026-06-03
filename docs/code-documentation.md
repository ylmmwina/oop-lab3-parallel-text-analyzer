# Code Documentation

This project uses Doxygen-style docstrings for Python code documentation.

## Purpose

The purpose of code documentation is to explain the responsibilities of the main classes and methods.

This is important because the project demonstrates:

- object-oriented design;
- sequential text processing;
- multithreaded text processing;
- GUI interaction with background threads;
- benchmark measurement;
- unit testing.

## Documentation Style

Python classes and methods use docstrings with Doxygen tags.

Common tags:

| Tag | Meaning |
|---|---|
| @brief | Short description |
| @param | Method parameter |
| @return | Return value |
| @throws | Possible exception |

## Documented Source Files

| File | Documentation Focus |
|---|---|
| app/main.py | GUI application and safe thread communication |
| core/analyzer.py | Single-file text analysis |
| core/models.py | Analysis result model |
| core/exceptions.py | Custom exceptions |
| core/sequential_processor.py | Sequential algorithm version |
| core/parallel_processor.py | Multithreaded algorithm version |
| core/benchmark.py | Benchmark runner and CSV result generation |
| tests/test_analyzer.py | Analyzer tests |
| tests/test_processors.py | Sequential and parallel processor tests |
| tests/test_benchmark.py | Benchmark tests |

## How to Generate HTML Documentation

Doxygen must be installed separately.

Run:

    doxygen Doxyfile

Generated documentation will be placed in:

    docs/api/html/

## Why Generated HTML Is Ignored

The repository contains:

- source code;
- docstrings;
- Doxyfile.

Generated HTML documentation is ignored because it is a build artifact and can be regenerated locally.
