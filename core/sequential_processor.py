from pathlib import Path

from core.analyzer import TextAnalyzer
from core.exceptions import InvalidTextInputError
from core.models import TextAnalysisResult


class SequentialTextProcessor:
    """
    @brief Послідовний процесор текстових файлів.

    Аналізує файли один за одним в одному потоці.
    Використовується як базова версія для порівняння
    з паралельною реалізацією.
    """

    def __init__(self, analyzer: TextAnalyzer | None = None):
        """
        @brief Ініціалізує послідовний процесор.
        @param analyzer Аналізатор одного файлу.
        """
        self.analyzer = analyzer or TextAnalyzer()

    def process_files(self, file_paths: list[Path]) -> TextAnalysisResult:
        """
        @brief Послідовно аналізує список файлів.
        @param file_paths Список шляхів до .txt файлів.
        @return Об'єднаний результат аналізу.
        @throws InvalidTextInputError Якщо список файлів порожній.
        """
        if not file_paths:
            raise InvalidTextInputError("File list is empty.")

        total_result = TextAnalysisResult()

        for file_path in file_paths:
            file_result = self.analyzer.analyze_file(file_path)
            total_result = total_result.merge(file_result)

        return total_result
