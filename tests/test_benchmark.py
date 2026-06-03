from pathlib import Path

import pytest

from core.benchmark import BenchmarkRunner


def create_dataset(directory: Path) -> Path:
    """
    @brief Створює тимчасовий набір текстових файлів для benchmark.
    @param directory Тимчасова директорія pytest.
    @return Шлях до директорії з dataset.
    """
    dataset = directory / "dataset"
    dataset.mkdir()

    (dataset / "one.txt").write_text(
        "Python threads process files.",
        encoding="utf-8",
    )
    (dataset / "two.txt").write_text(
        "Sequential and parallel results must match.",
        encoding="utf-8",
    )

    return dataset


def test_benchmark_runner_creates_rows(tmp_path):
    """
    @brief Перевіряє, що BenchmarkRunner створює рядки результатів.
    """
    dataset = create_dataset(tmp_path)
    runner = BenchmarkRunner(worker_counts=[1, 2])

    rows = runner.run_for_dataset(dataset)

    assert len(rows) == 2
    assert rows[0].dataset_name == "dataset"
    assert rows[0].file_count == 2
    assert rows[0].results_equal is True
    assert rows[1].worker_count == 2
    assert rows[1].results_equal is True


def test_benchmark_runner_saves_csv(tmp_path):
    """
    @brief Перевіряє збереження benchmark-результатів у CSV-файл.
    """
    dataset = create_dataset(tmp_path)
    output_path = tmp_path / "results" / "benchmark.csv"

    runner = BenchmarkRunner(worker_counts=[1])
    rows = runner.run_for_dataset(dataset)
    runner.save_csv(rows, output_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "dataset_name,file_count,worker_count" in content
    assert "dataset,2,1" in content
    assert "True" in content


def test_benchmark_runner_rejects_empty_dataset(tmp_path):
    """
    @brief Перевіряє помилку для dataset без .txt файлів.
    """
    empty_dataset = tmp_path / "empty"
    empty_dataset.mkdir()

    runner = BenchmarkRunner(worker_counts=[1])

    with pytest.raises(ValueError):
        runner.run_for_dataset(empty_dataset)
