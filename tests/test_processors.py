from pathlib import Path

import pytest

from core.exceptions import InvalidTextInputError
from core.parallel_processor import ParallelTextProcessor
from core.sequential_processor import SequentialTextProcessor


def create_text_files(directory: Path) -> list[Path]:
    """
    @brief Створює набір тестових текстових файлів.
    @param directory Тимчасова директорія.
    @return Список шляхів до створених файлів.
    """
    file1 = directory / "one.txt"
    file2 = directory / "two.txt"
    file3 = directory / "three.txt"

    file1.write_text("Python Python threads", encoding="utf-8")
    file2.write_text("Sequential processing is simple", encoding="utf-8")
    file3.write_text("Parallel processing can process files", encoding="utf-8")

    return [file1, file2, file3]


def test_sequential_and_parallel_results_are_equal(tmp_path):
    """
    @brief Перевіряє, що послідовна і паралельна версії дають однаковий результат.
    """
    files = create_text_files(tmp_path)

    sequential_result = SequentialTextProcessor().process_files(files)
    parallel_result = ParallelTextProcessor(max_workers=2).process_files(files)

    assert sequential_result.file_count == parallel_result.file_count
    assert sequential_result.line_count == parallel_result.line_count
    assert sequential_result.word_count == parallel_result.word_count
    assert sequential_result.char_count == parallel_result.char_count
    assert sequential_result.word_frequencies == parallel_result.word_frequencies


def test_parallel_result_is_equal_for_different_thread_counts(tmp_path):
    """
    @brief Перевіряє стабільність результатів для різної кількості потоків.
    """
    files = create_text_files(tmp_path)

    baseline = SequentialTextProcessor().process_files(files)

    for workers in [1, 2, 4]:
        parallel_result = ParallelTextProcessor(max_workers=workers).process_files(files)
        assert parallel_result.word_count == baseline.word_count
        assert parallel_result.word_frequencies == baseline.word_frequencies


def test_empty_file_list_raises_error():
    """
    @brief Перевіряє помилку для порожнього списку файлів.
    """
    with pytest.raises(InvalidTextInputError):
        SequentialTextProcessor().process_files([])

    with pytest.raises(InvalidTextInputError):
        ParallelTextProcessor(max_workers=2).process_files([])


def test_invalid_worker_count_raises_error():
    """
    @brief Перевіряє помилку для некоректної кількості потоків.
    """
    with pytest.raises(InvalidTextInputError):
        ParallelTextProcessor(max_workers=0)
