# Architecture Overview

This document describes the architecture of Parallel Text Analyzer.

The project is designed as a small desktop application with a clear separation between GUI, domain logic, processing algorithms, benchmarking, and tests.

## Purpose

Parallel Text Analyzer demonstrates sequential and multithreaded processing of text files.

The same text analysis task is implemented in two versions:

- sequential processing;
- parallel multithreaded processing.

The application also includes a GUI that starts analysis in a background thread and safely receives results through a queue.

## High-Level Layers

    GUI Layer
       |
       v
    Processing Layer
       |
       v
    Text Analysis Core
       |
       v
    Data Files

## GUI Layer

**File:** app/main.py

The GUI layer is implemented with CustomTkinter.

Responsibilities:

- allow the user to select a folder;
- start sequential and parallel comparison;
- keep the interface responsive during processing;
- receive worker thread messages through queue.Queue;
- update GUI widgets only from the main GUI thread.

Important class:

    TextAnalyzerApp

## Processing Layer

The processing layer contains two implementations of the same task.

| Class | File | Responsibility |
|---|---|---|
| SequentialTextProcessor | core/sequential_processor.py | Processes files one by one |
| ParallelTextProcessor | core/parallel_processor.py | Processes files using ThreadPoolExecutor |

Both processors return the same result type:

    TextAnalysisResult

This makes it easy to compare the sequential and parallel versions.

## Text Analysis Core

**File:** core/analyzer.py

The TextAnalyzer class analyzes a single .txt file.

It calculates:

- file count;
- line count;
- word count;
- character count;
- word frequencies.

The analyzer is reused by both processors.

## Domain Model

**File:** core/models.py

Main model:

    TextAnalysisResult

This object stores analysis results and can merge multiple partial results.

The merge() method is important because each file can be analyzed separately and then combined into one final result.

## Exceptions

**File:** core/exceptions.py

Custom exceptions are used to represent invalid input.

Examples:

- missing file;
- unsupported extension;
- directory instead of file;
- empty file list;
- invalid worker count.

## Benchmark Layer

**File:** core/benchmark.py

The benchmark layer measures execution time for sequential and parallel processing.

It records:

- dataset name;
- number of files;
- worker count;
- sequential time;
- parallel time;
- speedup;
- result equality.

The script run_benchmark.py saves benchmark results to CSV.

## Testing Layer

**Directory:** tests/

The tests check both correct and incorrect input data.

They also verify that sequential and parallel processing produce equivalent results.

## Design Principles

The project follows these object-oriented design principles:

- separation of responsibilities;
- encapsulation of text analysis details;
- reusable result model;
- interchangeable sequential and parallel processors;
- testable core logic;
- GUI separated from processing details.

## Conclusion

The architecture is intentionally compact but complete enough for Lab 3.

It demonstrates object-oriented design, sequential and multithreaded algorithms, GUI interaction with background threads, testing, and benchmark measurement.
