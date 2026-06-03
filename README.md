# Parallel Text Analyzer

Parallel Text Analyzer is a desktop application for Object-Oriented Design Laboratory Work 3.

The project covers both parts of Lab 3:

- Lab 3a: sequential and multithreaded versions of the same algorithm;
- Lab 3b: a GUI application that uses multithreading correctly.

## Project Idea

The application analyzes text files and compares sequential and parallel processing.

It calculates:

- number of processed files;
- number of lines;
- number of words;
- number of characters;
- most frequent words;
- sequential execution time;
- parallel execution time;
- speedup of parallel processing;
- equality of sequential and parallel results.

## Laboratory Requirements Coverage

| Requirement | Status | Implementation |
|---|---|---|
| Sequential algorithm version | Done | `core/sequential_processor.py` |
| Multithreaded algorithm version | Done | `core/parallel_processor.py` |
| Result comparison | Done | tests and GUI comparison |
| Different thread counts | Done | benchmark runner with worker counts |
| Execution time measurement | Done | `core/benchmark.py`, `run_benchmark.py` |
| GUI application | Done | `app/main.py`, CustomTkinter |
| Correct GUI/thread interaction | Done | background thread + `queue.Queue` + `after()` |
| Object-oriented design | Done | separate analyzer, processors, models, benchmark classes |
| Unit tests | Done | `tests/` |
| Code documentation | Done | Doxygen-style docstrings and `Doxyfile` |
| Report/documentation | Done | `docs/` |

## Technologies

- Python
- CustomTkinter
- ThreadPoolExecutor
- threading
- queue.Queue
- pytest
- Doxygen
- Git and GitHub

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   └── main.py
├── core/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── benchmark.py
│   ├── exceptions.py
│   ├── models.py
│   ├── parallel_processor.py
│   └── sequential_processor.py
├── data/
│   └── sample_texts/
├──docs/
│   ├── architecture.md
│   ├── benchmark-results.md
│   ├── code-documentation.md
│   ├── multithreading.md
│   ├── testing.md
│   └── uml/
│       ├── README.md
│       ├── images/
│       └── source/
├── results/
│   └── benchmark-results.csv
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_benchmark.py
│   └── test_processors.py
├── run_benchmark.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## How to Run the GUI Application

```powershell
python app/main.py
```

In the application:

1. click `Select folder`;
2. choose a folder with `.txt` files, for example `data/sample_texts`;
3. click `Run comparison`;
4. check the sequential time, parallel time, speedup, and result equality.

## How to Run Tests

```powershell
python -m pytest
```

The tests check:

- valid text analysis;
- invalid file paths;
- invalid file extensions;
- directory passed instead of file;
- empty file list;
- invalid worker count;
- equality of sequential and parallel results;
- equality of parallel results for different thread counts;
- benchmark row generation;
- benchmark CSV saving;
- empty dataset handling.

## How to Run Benchmark

Generate benchmark datasets:

```powershell
python generate_datasets.py
```

Run benchmark:

```powershell
python run_benchmark.py
```

The benchmark writes results to:

```text
results/benchmark-results.csv
```

The benchmark uses three generated datasets:

| Dataset | File Count |
|---|---:|
| small | 5 |
| medium | 25 |
| large | 60 |

For each dataset, the parallel processor is tested with:

```text
1, 2, 4, 8 worker threads
```

## Documentation

Project documentation is stored in the `docs/` directory.

| Document | Purpose |
|---|---|
| `docs/architecture.md` | Describes the object-oriented architecture |
| `docs/multithreading.md` | Explains sequential and multithreaded processing |
| `docs/benchmark-results.md` | Explains benchmark measurements and CSV results |
| `docs/testing.md` | Describes the testing strategy |
| `docs/code-documentation.md` | Explains Doxygen-style code documentation |
| `docs/uml/README.md` | Lists UML diagrams and their purpose |

## UML Diagrams

UML diagrams are stored in:

```text
docs/uml/
```

PlantUML source files are stored in:

```text
docs/uml/source/
```

Generated PNG images are stored in:

```text
docs/uml/images/
```

The repository includes both `.puml` source files and `.png` images.

Implemented UML diagrams:

- Class diagram;
- Component diagram;
- Sequence diagram;
- Activity diagram;
- Deployment diagram.

## Code Documentation

The project uses Doxygen-style Python docstrings.

Doxygen configuration file:

```text
Doxyfile
```

To generate HTML documentation locally, run:

```powershell
doxygen Doxyfile
```

Generated documentation will be placed in:

```text
docs/api/html/
```

Generated HTML files are ignored by Git because they are build artifacts.
## Notes

For small input datasets, the parallel version may be slower than the sequential version because thread creation and scheduling add overhead.

This is expected and is explained in the benchmark documentation.