# Multithreading Design

This document explains how multithreading is used in Parallel Text Analyzer.

## Sequential Processing

Sequential processing is implemented in:

    core/sequential_processor.py

Class:

    SequentialTextProcessor

This version processes files one by one in a single thread.

Workflow:

    file 1 -> analyze
    file 2 -> analyze
    file 3 -> analyze
    ...
    merge results

This implementation is used as the baseline for correctness and performance comparison.

## Parallel Processing

Parallel processing is implemented in:

    core/parallel_processor.py

Class:

    ParallelTextProcessor

This version uses:

    concurrent.futures.ThreadPoolExecutor

Workflow:

    files -> ThreadPoolExecutor -> analyze files in worker threads -> merge results

Each worker thread analyzes one file at a time using the same TextAnalyzer logic.

The final result is created by merging partial results.

## Why Text Files Are Suitable for Threads

Text file analysis includes file reading, which is an I/O operation.

In Python, threads are especially useful for I/O-bound work.

For very small datasets, parallel processing may be slower because of thread overhead.

For larger datasets, parallel processing can become more useful because multiple files can be read and processed concurrently.

## Correct GUI and Thread Interaction

The GUI is implemented in:

    app/main.py

The application does not run long processing directly in the GUI thread.

Instead, it starts a background thread:

    threading.Thread

The worker thread performs the analysis and sends messages to the GUI through:

    queue.Queue

The GUI thread periodically checks the queue using:

    after()

This is important because GUI widgets should be updated only from the main GUI thread.

## GUI Message Flow

    Worker thread
       |
       v
    queue.Queue
       |
       v
    GUI thread reads messages with after()
       |
       v
    GUI updates labels, progress bar, and output box

## Compared Versions

The application compares:

- SequentialTextProcessor;
- ParallelTextProcessor.

Both processors use the same TextAnalyzer.

This makes the comparison fair because only the processing strategy is different.

## Thread Counts

The benchmark can run parallel processing with different worker counts.

Current benchmark worker counts:

    1
    2
    4

A worker count of 1 is useful because it shows the overhead of the parallel processor without real parallelism.

## Result Equality

Sequential and parallel results are compared by:

- file count;
- line count;
- word count;
- character count;
- word frequencies.

The expected result is:

    results_equal = True

If results differ, the parallel version is considered incorrect.

## Conclusion

The project demonstrates practical multithreading:

- background GUI processing;
- parallel file analysis;
- safe GUI communication through a queue;
- comparison with a sequential baseline;
- benchmark measurements with different thread counts.
