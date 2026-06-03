import re
from pathlib import Path

from core.exceptions import InvalidTextInputError
from core.models import TextAnalysisResult


class TextAnalyzer:
    """
    @brief Аналізатор одного текстового файлу.

    Клас інкапсулює логіку читання файлу та підрахунку
    рядків, слів, символів і частот слів.
    """

    WORD_PATTERN = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9']+")

    def analyze_file(self, file_path: Path) -> TextAnalysisResult:
        """
        @brief Аналізує один текстовий файл.
        @param file_path Шлях до .txt файлу.
        @return Результат аналізу файлу.
        @throws InvalidTextInputError Якщо файл некоректний.
        """
        self._validate_file(file_path)

        text = file_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        words = self._extract_words(text)

        result = TextAnalysisResult(
            file_count=1,
            line_count=len(lines),
            word_count=len(words),
            char_count=len(text),
        )

        result.word_frequencies.update(word.lower() for word in words)

        return result

    def _validate_file(self, file_path: Path) -> None:
        """
        @brief Перевіряє, що шлях веде до існуючого .txt файлу.
        @param file_path Шлях до файлу.
        @throws InvalidTextInputError Якщо файл не можна аналізувати.
        """
        if not file_path.exists():
            raise InvalidTextInputError(f"File does not exist: {file_path}")

        if not file_path.is_file():
            raise InvalidTextInputError(f"Path is not a file: {file_path}")

        if file_path.suffix.lower() != ".txt":
            raise InvalidTextInputError(f"Only .txt files are supported: {file_path}")

    def _extract_words(self, text: str) -> list[str]:
        """
        @brief Витягує слова з тексту.
        @param text Вхідний текст.
        @return Список знайдених слів.
        """
        return self.WORD_PATTERN.findall(text)
