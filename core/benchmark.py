import csv
import time
from dataclasses import dataclass
from pathlib import Path

from core.parallel_processor import ParallelTextProcessor
from core.sequential_processor import SequentialTextProcessor


@dataclass
class BenchmarkRow:
    """
    @brief Один рядок результатів benchmark-вимірювання.
    """

    dataset_name: str
    file_count: int
    worker_count: int
    sequential_time: float
    parallel_time: float
    speedup: float
    results_equal: bool


class BenchmarkRunner:
    """
    @brief Запускає вимірювання часу для sequential і parallel обробки.

    Клас використовується для перевірки продуктивності на різних
    наборах файлів і з різною кількістю потоків.
    """

    def __init__(self, worker_counts: list[int] | None = None):
        """
        @brief Ініціалізує benchmark runner.
        @param worker_counts Список кількостей потоків для перевірки.
        """
        self.worker_counts = worker_counts or [1, 2, 4, 8]

    def run_for_dataset(self, dataset_path: Path) -> list[BenchmarkRow]:
        """
        @brief Запускає benchmark для однієї папки з .txt файлами.
        @param dataset_path Папка з текстовими файлами.
        @return Список результатів benchmark.
        """
        files = sorted(dataset_path.glob("*.txt"))

        if not files:
            raise ValueError(f"Dataset does not contain .txt files: {dataset_path}")

        sequential_processor = SequentialTextProcessor()

        sequential_start = time.perf_counter()
        sequential_result = sequential_processor.process_files(files)
        sequential_time = time.perf_counter() - sequential_start

        rows = []

        for worker_count in self.worker_counts:
            parallel_processor = ParallelTextProcessor(max_workers=worker_count)

            parallel_start = time.perf_counter()
            parallel_result = parallel_processor.process_files(files)
            parallel_time = time.perf_counter() - parallel_start

            results_equal = (
                sequential_result.file_count == parallel_result.file_count
                and sequential_result.line_count == parallel_result.line_count
                and sequential_result.word_count == parallel_result.word_count
                and sequential_result.char_count == parallel_result.char_count
                and sequential_result.word_frequencies == parallel_result.word_frequencies
            )

            speedup = sequential_time / parallel_time if parallel_time > 0 else 0

            rows.append(
                BenchmarkRow(
                    dataset_name=dataset_path.name,
                    file_count=len(files),
                    worker_count=worker_count,
                    sequential_time=sequential_time,
                    parallel_time=parallel_time,
                    speedup=speedup,
                    results_equal=results_equal,
                )
            )

        return rows

    def save_csv(self, rows: list[BenchmarkRow], output_path: Path) -> None:
        """
        @brief Зберігає benchmark-результати у CSV-файл.
        @param rows Результати вимірювань.
        @param output_path Шлях до CSV-файлу.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    "dataset_name",
                    "file_count",
                    "worker_count",
                    "sequential_time_seconds",
                    "parallel_time_seconds",
                    "speedup",
                    "results_equal",
                ]
            )

            for row in rows:
                writer.writerow(
                    [
                        row.dataset_name,
                        row.file_count,
                        row.worker_count,
                        f"{row.sequential_time:.8f}",
                        f"{row.parallel_time:.8f}",
                        f"{row.speedup:.4f}",
                        row.results_equal,
                    ]
                )
