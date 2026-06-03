# Benchmark Results

This document explains benchmark measurements for Parallel Text Analyzer.

## Purpose

The benchmark compares sequential and parallel text file processing.

It is required to measure execution time for different input data and different thread counts, and to compare the parallel version with the sequential version.

## Benchmark Script

Benchmark script:

    run_benchmark.py

Core benchmark logic:

    core/benchmark.py

Generated CSV file:

    results/benchmark-results.csv

## Measured Values

| Column | Meaning |
|---|---|
| dataset_name | Name of the dataset folder |
| file_count | Number of processed .txt files |
| worker_count | Number of worker threads |
| sequential_time_seconds | Execution time of sequential processing |
| parallel_time_seconds | Execution time of parallel processing |
| speedup | Sequential time divided by parallel time |
| results_equal | Whether sequential and parallel results are identical |

## Speedup Formula

    speedup = sequential_time_seconds / parallel_time_seconds

If speedup is greater than 1, the parallel version is faster.

If speedup is less than 1, the sequential version is faster.

## Current Dataset

The current benchmark uses:

    data/sample_texts/

This is a small sample dataset used for demonstration and repeatable testing.

## Important Note About Small Datasets

For small datasets, parallel processing can be slower than sequential processing.

This happens because multithreading has overhead:

- creating worker threads;
- scheduling tasks;
- collecting results;
- merging partial results.

Therefore, a speedup below 1 on a small dataset is not an error.

## Correctness Requirement

The most important correctness condition is:

    results_equal = True

This means that sequential and parallel processing produced the same analysis result.

## How to Reproduce

Run:

    python run_benchmark.py

Then open:

    results/benchmark-results.csv

## Conclusion

The benchmark provides measurable evidence that both processing modes work and produce equal results.

It also shows how execution time changes depending on the number of worker threads.
