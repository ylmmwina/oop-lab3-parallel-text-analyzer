from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from core.analyzer import TextAnalyzer
from core.exceptions import InvalidTextInputError
from core.models import TextAnalysisResult


class ParallelTextProcessor:
    """
    @brief Паралельний процесор текстових файлів.

    Аналізує файли у кількох потоках за допомогою ThreadPoolExecutor.
    Використовується для порівняння з послідовною реалізацією.
    """

    def __init__(self, max_workers: int = 4, analyzer: TextAnalyzer | None = None):
        """
        @brief Ініціалізує паралельний процесор.
        @param max_workers Максимальна кількість потоків.
        @param analyzer Аналізатор одного файлу.
        @throws InvalidTextInputError Якщо кількість потоків некоректна.
        """
        if max_workers < 1:
            raise InvalidTextInputError("max_workers must be at least 1.")

        self.max_workers = max_workers
        self.analyzer = analyzer or TextAnalyzer()

    def process_files(self, file_paths: list[Path]) -> TextAnalysisResult:
        """
        @brief Паралельно аналізує список файлів.
        @param file_paths Список шляхів до .txt файлів.
        @return Об'єднаний результат аналізу.
        @throws InvalidTextInputError Якщо список файлів порожній.
        """
        if not file_paths:
            raise InvalidTextInputError("File list is empty.")

        total_result = TextAnalysisResult()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            file_results = executor.map(self.analyzer.analyze_file, file_paths)

            for file_result in file_results:
                total_result = total_result.merge(file_result)

        return total_result
