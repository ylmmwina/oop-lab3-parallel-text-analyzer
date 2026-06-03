from collections import Counter
from dataclasses import dataclass, field


@dataclass
class TextAnalysisResult:
    """
    @brief Результат аналізу одного або кількох текстових файлів.

    Об'єкт зберігає кількість файлів, рядків, слів, символів
    і частоти знайдених слів.
    """

    file_count: int = 0
    line_count: int = 0
    word_count: int = 0
    char_count: int = 0
    word_frequencies: Counter = field(default_factory=Counter)

    def merge(self, other: "TextAnalysisResult") -> "TextAnalysisResult":
        """
        @brief Об'єднує два результати аналізу.
        @param other Інший результат аналізу.
        @return Новий об'єднаний результат.
        """
        return TextAnalysisResult(
            file_count=self.file_count + other.file_count,
            line_count=self.line_count + other.line_count,
            word_count=self.word_count + other.word_count,
            char_count=self.char_count + other.char_count,
            word_frequencies=self.word_frequencies + other.word_frequencies,
        )

    def top_words(self, limit: int = 10) -> list[tuple[str, int]]:
        """
        @brief Повертає найчастіші слова.
        @param limit Максимальна кількість слів у результаті.
        @return Список пар слово-кількість.
        """
        return self.word_frequencies.most_common(limit)
